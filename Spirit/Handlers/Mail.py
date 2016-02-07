from ..Events import Events
events = Events()

@events.on("l#mst")
def handleStartMailEngine(self, data):
	# TODO: Implement actual mail system
	self.sendLine("%xt%mst%-1%0%0%")
