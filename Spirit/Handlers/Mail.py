from ..Events import Events
events = Events()

@events.on("l#mst")
def handleStartMailEngine(self, data):
	# TODO: Implement actual mail system
	self.sendXt("mst", 0, 0)
