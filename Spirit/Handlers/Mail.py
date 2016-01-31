worldHandlers = {
	"l#mst": "handleStartMailEngine"
}

# TODO: Implement actual mail system
def handleStartMailEngine(self, data):
	self.sendLine("%xt%mst%-1%0%0%")
