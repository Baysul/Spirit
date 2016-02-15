import Login

from Spirit.Events import Events
from Spirit.Data.User import User
from Spirit.Crypto import Crypto

events = Events()
events.off("login", Login.handleLogin)

@events.on("login")
def handleLogin(self, data):
	try:
		playerData = data[0][0].text.split("|")

		playerId = playerData[0]
		playerSwid = playerData[1]
		username = playerData[2]

		playerHashes = data[0][1].text.split("#")
		clientHash, confirmationHash = playerHashes

		self.logger.info("{0} is attempting to login".format(username))

		user = self.session.query(User).filter_by(Username=username).first()

		if user is None:
			return self.sendErrorAndDisconnect(101)

		if int(playerId) != user.Id:
			self.logger.warn("User sent an invalid player id in the login request")
			self.transport.loseConnection()

		if playerSwid != user.Swid:
			self.logger.warn("User sent an invalid swid value in the login request")
			self.transport.loseConnection()

		loginKey = user.LoginKey

		encryptedPassword = Crypto.encryptPassword(loginKey + self.randomKey) + loginKey

		if clientHash != encryptedPassword:
			self.logger.debug("Comparing {0} to {1}".format(clientHash, encryptedPassword))
			self.sendErrorAndDisconnect(101)

		elif confirmationHash != user.ConfirmationHash:
			self.sendErrorAndDisconnect(101)

		else:
			self.session.add(user)
			self.user = user

			self.user.ConfirmationHash = None

			# Commit for security
			self.session.commit()

			self.sendXt("l")

	except IndexError:
		self.logger.warn("Client sent invalid login packet")
		self.transport.loseConnection()