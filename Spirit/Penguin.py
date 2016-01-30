from Spheniscidae import Spheniscidae
from Data.User import User
from Crypto import Crypto

class Penguin(Spheniscidae):

	worldHandlers = {}

	def __init__(self, session):
		super(Penguin, self).__init__(session)

		# Defined in handleLogin if authentication is successful
		self.user = None

		self.logger.info("Penguin class instantiated")

	# TODO: Validate data sent by the client
	def handleLogin(self, data):
		try:
			playerData = data[0][0].text.split("|")
			username = playerData[2]

			playerHashes = data[0][1].text.split("#")
			clientHash, confirmationHash = playerHashes

			self.logger.info("{0} is attempting to login".format(username))

			user = self.session.query(User).filter_by(Username=username).first()

			if user is None:
				return self.sendErrorAndDisconnect(101)

			dbConfirmationHash = user.ConfirmationHash
			loginKey = user.LoginKey

			encryptedPassword = Crypto.encryptPassword(loginKey + self.randomKey) + loginKey

			if clientHash != encryptedPassword:
				self.logger.debug("Comparing {0} to {1}".format(clientHash, encryptedPassword))
				self.sendErrorAndDisconnect(101)

			elif confirmationHash != dbConfirmationHash:
				self.logger.debug("Comparing {0} to {1}".format(confirmationHash, dbConfirmationHash))
				self.sendErrorAndDisconnect(101)

			else:
				self.logger.debug("Everything looks good.")

				self.session.add(user)
				self.user = user

				self.user.ConfirmationHash = None

				# Commit for security
				self.session.commit()

				self.sendLine("%xt%l%-1%")

		except IndexError:
			self.logger.warn("Client sent invalid login packet")
			self.transport.loseConnection()
