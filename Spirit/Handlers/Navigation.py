from ..Events import Events
events = Events()

@events.on("j#js")
def handleJoinWorld(self, data):
	print "Handling joinWorld request"

	from time import time

	playerId = data[4]
	loginKey = data[5]

	if self.user.Id != int(playerId):
		self.logger.warn("User sent an invalid player id!")
		self.transport.loseConnection()

	if self.user.LoginKey != loginKey:
		self.logger.warn("User sent invalid login key in joinWorld request!")

	self.user.LoginKey = None
	self.session.commit()

	self.sendLine("%xt%js%-1%1%0%{0}%1%".format("1" if self.user.Moderator else "0"))

	playerString = self.getPlayerString()
	loginTime = time()

	# TODO - update?
	loadPlayer = "{0}|%{1}%0%1440%{2}%{3}%0%7521%%7%1%0%211843".format(playerString, self.user.Coins, str(loginTime),
	                                                                   self.age)
	self.sendLine("%xt%lp%-1%{0}%".format(loadPlayer))

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
