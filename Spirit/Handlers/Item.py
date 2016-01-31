worldHandlers = {
	"i#gi": "handleGetInventoryList"
}

def handleGetInventoryList(self, data):
	self.logger.debug("Handling inventory list request")

	self.sendLine("%xt%gi%-1%" + self.user.Inventory + "%")