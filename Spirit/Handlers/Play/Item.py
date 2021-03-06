from Spirit.Events import Events

events = Events()

@events.on("i#ai")
def handleBuyInventory(self, data):
	itemId = data[4]

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

	self.addItem(itemId, itemCost)

@events.on("i#gi")
def handleGetInventoryList(self, data):
	inventoryArray = self.user.Inventory.split("%")

	try:
		inventoryArray = map(int, inventoryArray)
		self.inventory = inventoryArray

	except ValueError:
		self.inventory = []

	finally:
		self.sendXt("gi", self.user.Inventory)