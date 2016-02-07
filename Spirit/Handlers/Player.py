from ..Events import Events
events = Events()

@events.on("u#pbi")
def handleGetPlayerInfoById(self, data):
	from sqlalchemy.orm import load_only
	from ..Data.User import User

	playerId = data[4]

	if playerId.isdigit():
		playerId = int(playerId)

		if playerId == self.user.Id:
			playerSwid = self.user.Swid
			username = self.user.Username

		else:
			playerModel = self.session.query(User).options(load_only("Username", "Swid")) \
				.filter_by(Id=playerId).first()

			if playerModel is None:
				return

			username = playerModel.Username
			playerSwid = playerModel.Swid

		self.sendXt("pbi", playerSwid, playerId, username)

@events.on("u#h")
def handleSendHeartbeat(self, data):
	self.sendXt("h")

@events.on("u#sp")
def handleSendPlayerMove(self, data):
	x, y = data[4:6]

	if x.isdigit() and y.isdigit():
		self.x = int(x)
		self.y = int(y)

		self.room.sendXt("sp", self.user.Id, self.x, self.y)
