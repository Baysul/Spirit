import logging
from time import time
from math import floor
import xml.etree.ElementTree as ET

from sqlalchemy.exc import InvalidRequestError

from twisted.protocols.basic import LineReceiver

from Crypto import Crypto
from Data.User import User

class Spheniscidae(LineReceiver, object):

	delimiter = "\x00"

	def __init__(self, session, spirit):
		self.logger = logging.getLogger("Spirit")
		self.session = session
		self.spirit = spirit

		# Defined once the client requests it (see handleRandomKey)
		self.randomKey = None

		self.xmlHandlers = {
			"verChk": self.handleVersionCheck,
			"rndK": self.handleRandomKey,
			"login": self.handleLogin
		}

	def sendErrorAndDisconnect(self, error):
		self.sendError(error)
		self.transport.loseConnection()

	def sendError(self, error):
		self.sendLine("%xt%e%-1%{0}%".format(error))

	def handleLogin(self, data):
		username = data[0][0].text
		clientHash = data[0][1].text

		self.logger.info("{0} is attempting to login".format(username))

		user = self.session.query(User).filter_by(Username=username).first()

		if user is None:
			return self.sendErrorAndDisconnect(101)

		databasePassword = user.Password

		loginHash = Crypto.getLoginHash(databasePassword, self.randomKey)

		if clientHash == loginHash:
			confirmationHash = Crypto.hash(self.randomKey)
			friendsKey = Crypto.hash(user.Id)

			self.session.add(user)

			user.ConfirmationHash = confirmationHash
			user.LoginKey = Crypto.hash(self.randomKey)

			loginTime = time()

			loginPacket = "%xt%l%-1%{0}|{1}|{2}|{3}|1|45|2|false|true|{4}%{5}%{6}%101,1%spirit@solero.me%" \
				.format(user.Id, user.Swid, user.Username, user.LoginKey, floor(loginTime), confirmationHash, friendsKey)

			self.sendLine(loginPacket)

		else:
			self.sendErrorAndDisconnect(101)

	def handleRandomKey(self, data):
		self.logger.debug("Received random key request")

		randomKey = Crypto.generateRandomKey()
		self.randomKey = randomKey

		self.logger.debug("Generated random key " + randomKey)

		self.sendLine("<msg t='sys'><body action='rndK' r='-1'><k>" + self.randomKey + "</k></body></msg>")

	def handleVersionCheck(self, data):
		bodyTag = data[0]
		apiVersion = bodyTag.get("v")

		self.logger.debug("Received version check")

		if apiVersion == "153":
			self.logger.debug("API versions match")

			self.sendLine("<msg t='sys'><body action='apiOK' r='0'></body></msg>")
		elif apiVersion!= "153":
			self.logger.debug("API versions don't match (client checked for version " + apiVersion + ")")

			self.sendLine("<msg t='sys'><body action='apiKO' r='0'></body></msg>")
		else:
			self.logger.error("Received a version-check packet from a client without a version attribute")
			self.loseConnection()

	def lineReceived(self, data):
		self.logger.debug("Received data: {0}".format(data))

		if data.startswith("<"):
			self.handleXmlData(data)
		else:
			self.handleWorldData(data)

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

				if action in self.xmlHandlers:
					self.xmlHandlers[action](bodyTag)

				else:
					self.logger.warn("Packet did not contain a valid action attribute!")

			except IndexError:
				self.logger.warn("Received invalid XML data (didn't contain a body tag)")
		else:
			self.logger.warn("Received invalid XML data!")

	def handleWorldData(self, data):
		self.logger.debug("Received XT data: {0}".format(data))

		# First and last elements are blank
		parsedData = data.split("%")[1:-1]

		packetId = parsedData[2]

		if packetId in self.worldHandlers:
			worldHandler = self.worldHandlers[packetId]
			worldHandlerMethod = getattr(self, worldHandler)

			worldHandlerMethod(parsedData)

		else:
			self.logger.warn("Received unknown packet! {0}".format(packetId))

	def connectionLost(self, reason):
		self.logger.info("Client disconnected")

		try:
			self.session.commit()

		except InvalidRequestError:
			self.logger.info("There aren't any transactions in progress")

		finally:
			self.session.close()