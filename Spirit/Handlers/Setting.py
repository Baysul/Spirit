from ..Events import Events
events = Events()

@events.on("s#upc")
def handleSendUpdatePlayerColour(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Color = int(itemId)
		self.room.send("%xt%upc%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#uph")
def handleSendUpdatePlayerHead(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Head = int(itemId)
		self.room.send("%xt%uph%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upf")
def handleSendUpdatePlayerFace(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Face = int(itemId)
		self.room.send("%xt%upf%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upn")
def handleSendUpdatePlayerNeck(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Neck = int(itemId)
		self.room.send("%xt%upn%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upb")
def handleSendUpdatePlayerBody(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Body = int(itemId)
		self.room.send("%xt%upb%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upa")
def handleSendUpdatePlayerHand(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Hands = int(itemId)
		self.room.send("%xt%upa%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upe")
def handleSendUpdatePlayerFeet(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Feet = int(itemId)
		self.room.send("%xt%upe%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upl")
def handleSendUpdatePlayerFlag(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Pin = int(itemId)
		self.room.send("%xt%upl%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))

@events.on("s#upp")
def handleSendUpdatePlayerPhoto(self, data):
	itemId = data[4]

	if itemId.isdigit():
		self.user.Photo = int(itemId)
		self.room.send("%xt%upp%{0}%{1}%{2}%".format(self.room.internalId, self.user.Id, itemId))
