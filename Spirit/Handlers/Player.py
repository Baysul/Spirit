worldHandlers = {
	"u#sp": "handleSendPlayerMove",
	"u#h": "handleSendHeartbeat"
}

def handleSendHeartbeat(self, data):
	self.sendLine("%xt%h%-1%")

def handleSendPlayerMove(self, data):
	x, y = data[4:6]

	if x.isdigit() and y.isdigit():
		self.x = int(x)
		self.y = int(y)

		playerMovement = "%xt%sp%{0}%{1}%{2}%{3}%".format(self.room.internalId, self.user.Id, self.x, self.y)
		self.room.send(playerMovement)