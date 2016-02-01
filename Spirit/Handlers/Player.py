worldHandlers = {
	"u#sp": "handleSendPlayerMove",
	"u#h": "handleSendHeartbeat",
	"u#pbi": "handleGetPlayerInfoById"
}

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
			playerModel = self.session.query(User).options(load_only("Username", "Swid"))\
				.filter_by(Id=playerId).first()

			if playerModel is None:
				return

			username = playerModel.Username
			playerSwid = playerModel.Swid

		playerInfoById = "%xt%pbi%{0}%{1}%{2}%{3}%".format(self.room.internalId, playerSwid, playerId, username)
		self.sendLine(playerInfoById)

def handleSendHeartbeat(self, data):
	self.sendLine("%xt%h%-1%")

def handleSendPlayerMove(self, data):
	x, y = data[4:6]

	if x.isdigit() and y.isdigit():
		self.x = int(x)
		self.y = int(y)

		playerMovement = "%xt%sp%{0}%{1}%{2}%{3}%".format(self.room.internalId, self.user.Id, self.x, self.y)
		self.room.send(playerMovement)