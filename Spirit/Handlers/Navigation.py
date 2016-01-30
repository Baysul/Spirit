worldHandlers = {
	"j#js": "handleJoinWorld",
	"j#jr": "handleJoinRoom"
}

# TODO: Verify user id
def handleJoinWorld(self, data):
	self.logger.debug("Received joinWorld request")

	playerId = data[4]
	loginKey = data[5]

	if self.user.LoginKey == loginKey:
		self.logger.debug("User's login key is valid!")

	else:
		self.logger.warn("User sent invalid login key in joinWorld request!")

	self.user.LoginKey = None
	self.session.commit()

def handleJoinRoom(self, data):
	self.logger.debug("Received joinRoom request")