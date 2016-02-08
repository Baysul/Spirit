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


