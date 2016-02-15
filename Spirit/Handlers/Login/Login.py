from time import time

from Spirit.Events import Events
from Spirit.Crypto import Crypto
from Spirit.Data.User import User

events = Events()

@events.on("login")
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

			userData = "{0}|{1}|{2}|{3}|1|45|2|false|true|{4}".format(user.Id, user.Swid, user.Username,
			                                                          user.LoginKey, loginTime)

			self.sendXt("l", userData, confirmationHash, friendsKey, "101,1", "spirit@solero.me")

		else:
			self.sendErrorAndDisconnect(101)

@events.on("rndK")
def handleRandomKey(self, data):
	self.logger.debug("Received random key request")

	randomKey = Crypto.generateRandomKey()
	self.randomKey = randomKey

	self.logger.debug("Generated random key " + randomKey)

	self.sendLine("<msg t='sys'><body action='rndK' r='-1'><k>" + self.randomKey + "</k></body></msg>")

@events.on("verChk")
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