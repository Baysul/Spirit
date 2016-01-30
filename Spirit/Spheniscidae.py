import logging
import xml.etree.ElementTree as ET

from twisted.protocols.basic import LineReceiver

from Crypto import Crypto

class Spheniscidae(LineReceiver):

	delimiter = "\x00"

	def __init__(self, session):
		self.logger = logging.getLogger("Spirit")
		self.session = session

		self.xmlHandlers = {
			"verChk": self.handleVersionCheck,
			"rndK": self.handleRandomKey,
			"login": self.handleLogin
		}

	def handleLogin(self, data):
		username = data[0][0].text
		password = data[0][1].text

		self.logger.info("{0} is attempting to login".format(username))

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

			# TODO: try/except?
			bodyTag = elementTree[0]
			action = bodyTag.get("action")

			if action in self.xmlHandlers:
				self.xmlHandlers[action](bodyTag)

			else:
				self.logger.warn("Packet did not contain a valid action attribute!")
		else:
			self.logger.warn("Received invalid XML data!")

	def handleWorldData(self, data):
		self.logger.debug("Received XT data: {0}".format(data))
