from time import time

from ..Events import Events
events = Events()

@events.on("j#js")
def handleJoinWorld(self, data):
	playerId = data[4]
	loginKey = data[5]

	if self.user.Id != int(playerId):
		self.logger.warn("User sent an invalid player id!")
		self.transport.loseConnection()

	if self.user.LoginKey != loginKey:
		self.logger.warn("User sent invalid login key in joinWorld request!")

	self.user.LoginKey = None
	self.session.commit()

	isModerator = 1 if self.user.Moderator else 0

	self.sendXt("js", 1, 0, isModerator, 1)

	loginTime = time()

	self.sendXt("lp", self.getPlayerString(), self.user.Coins, 0, 1440,
	            loginTime, self.age, 0, 7521, "", 7, 1, 0, 211843)

	self.spirit.rooms[100].add(self)

@events.on("j#jr")
def handleJoinRoom(self, data):
	roomId = int(data[4])

	if roomId in self.spirit.rooms:
		x, y = data[5:7]

		if x.isdigit() and y.isdigit():
			self.x = int(x)
			self.y = int(y)
			self.frame = 1

			self.room.remove(self)
			self.spirit.rooms[roomId].add(self)
