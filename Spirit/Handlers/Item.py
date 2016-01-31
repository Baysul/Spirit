worldHandlers = {
	"i#gi": "handleGetInventoryList",
	"i#ai": "handleBuyInventory"
}

def handleBuyInventory(self, data):
	itemId = data[4]

	self.logger.debug("Purchasing item {0}".format(itemId))

	if not itemId.isdigit():
		return self.sendError(402)

	itemId = int(itemId)

	if itemId not in self.spirit.items:
		return self.sendError(402)

	elif itemId in self.inventory:
		return self.sendError(400)

	itemCost = self.spirit.items[itemId]

	if self.user.Coins < itemCost:
		return self.sendError(401)

	self.addItem(itemId)


def handleGetInventoryList(self, data):
	inventoryArray = self.user.Inventory.split("%")

	try:
		inventoryArray = map(int, inventoryArray)
		self.inventory = inventoryArray

	except ValueError:
		self.logger.debug("Empty inventory string (?)")
		self.inventory = []

	finally:
		self.sendLine("%xt%gi%-1%" + self.user.Inventory + "%")