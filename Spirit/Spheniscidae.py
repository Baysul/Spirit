import logging
import xml.etree.ElementTree as ET

from sqlalchemy.exc import InvalidRequestError
from twisted.protocols.basic import LineReceiver

from Events import Events

class Spheniscidae(LineReceiver, object):

	delimiter = "\x00"

	def __init__(self, session, spirit):
		self.logger = logging.getLogger("Spirit")

		self.session = session
		self.spirit = spirit
		self.room = None

		self.spirit.players.append(self)

		# Defined once the client requests it (see handleRandomKey)
		self.randomKey = None

		self.event = Events()

	def sendErrorAndDisconnect(self, error):
		self.sendError(error)
		self.transport.loseConnection()

	def sendError(self, error):
		self.sendXt("e", error)

	# TODO: Replace * with actual port
	def sendPolicyFile(self):
		self.sendLine("<cross-domain-policy><allow-access-from domain='*' to-ports='*' /></cross-domain-policy>")

	def handleXmlData(self, data):
		self.logger.debug("Received XML data: {0}".format(data))

		elementTree = ET.fromstring(data)

		if elementTree.tag == "policy-file-request":
			self.sendPolicyFile()

		elif elementTree.tag == "msg":
			self.logger.debug("Received valid XML data")

			try:
				bodyTag = elementTree[0]
				action = bodyTag.get("action")

				if self.event.exists(action):
					self.event.emit(action, bodyTag)

				else:
					self.logger.warn("Packet did not contain a valid action attribute!")

			except IndexError:
				self.logger.warn("Received invalid XML data (didn't contain a body tag)")
		else:
			self.logger.warn("Received invalid XML data!")

		self.event.emit("received-xml", elementTree)

	def handleWorldData(self, data):
		self.logger.debug("Received XT data: {0}".format(data))

		# First and last elements are blank
		parsedData = data.split("%")[1:-1]

		packetId = parsedData[2]

		if self.event.exists(packetId):
			self.event.emit(packetId, self, parsedData)

		else:
			self.logger.debug("Handler for {0} doesn't exist!".format(packetId))

		self.event.emit("received-world", self, data)

	# TODO: Clean
	def sendXt(self, *data):
		data = list(data)

		handlerId = data.pop(0)
		internalId = self.room.internalId if self.room is not None else -1
		mappedData = map(str, data)

		xtData = "%".join(mappedData)

		line = "%xt%{0}%{1}%{2}%".format(handlerId, internalId, xtData)
		self.sendLine(line)

	def sendLine(self, line):
		super(Spheniscidae, self).sendLine(line)

		self.event.emit("sent", self, line)

		self.logger.debug("Outgoing data: {0}".format(line))

	def lineReceived(self, data):
		self.event.emit("received", self, data)

		if data.startswith("<"):
			self.handleXmlData(data)
		else:
			self.handleWorldData(data)

	def connectionLost(self, reason):
		self.logger.info("Client disconnected")

		self.spirit.players.remove(self)

		try:
			self.session.commit()

			if hasattr(self, "room") and self.room is not None:
				self.room.remove(self)

			if hasattr(self, "user"):
				self.session.expunge(self.user)

		except InvalidRequestError:
			self.logger.info("There aren't any transactions in progress")

		finally:
			self.session.close()

		self.event.emit("disconnected", self, reason)