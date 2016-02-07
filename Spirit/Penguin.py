from Spheniscidae import Spheniscidae
from Data.User import User
from Crypto import Crypto

class Penguin(Spheniscidae):

	worldHandlers = {}

	# TODO: Calculate actual age
	age = 45
	frame = 1
	x, y = (0, 0)

	def __init__(self, session, spirit):
		super(Penguin, self).__init__(session, spirit)

		# Defined in handleLogin if authentication is successful
		self.user = None

		self.logger.info("Penguin class instantiated")

	def addItem(self, itemId, itemCost=0):
		if itemId in self.inventory:
			return False

		self.inventory.append(itemId)

		stringifiedInventory = map(str, self.inventory)
		self.user.Inventory = "%".join(stringifiedInventory)

		self.user.Coins -= itemCost

		self.sendXt("ai", itemId, self.user.Coins)

	# TODO: Puffle values
	# TODO: Cache string to avoid unnecessary re-generation
	def getPlayerString(self):
		playerArray = (
			self.user.Id,
			self.user.Username,
			45,
			self.user.Color,
			self.user.Head,
			self.user.Face,
			self.user.Neck,
			self.user.Body,
			self.user.Hands,
			self.user.Feet,
			self.user.Pin,
			self.user.Photo,
			self.x,
			self.y,
			self.frame,
			1,
			1, # Membership days
			self.user.Avatar,
			0,
			self.user.AvatarAttributes
		)

		playerString = map(str, playerArray)
		return "|".join(playerString)

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
