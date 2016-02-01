from collections import deque

class Room(object):

	def __init__(self, *room):
		self.externalId, self.internalId = room

		self.players = deque()

	def send(self, data):
		for player in self.players:
			player.sendLine(data)

	def generateRoomString(self):
		roomString = "%".join([player.getPlayerString() for player in self.players])

		return roomString

	def add(self, player):
		self.players.append(player)

		joinRoom = "%xt%jr%{0}%{1}%{2}%".format(self.internalId, self.externalId, self.generateRoomString())
		addPlayer = "%xt%ap%{0}%{1}%".format(self.internalId, player.getPlayerString())

		player.sendLine(joinRoom)

		self.send(addPlayer)

		player.room = self

	def remove(self, player):
		self.players.remove(player)

		self.send("%xt%rp%-1%{0}%".format(player.user.Id))
