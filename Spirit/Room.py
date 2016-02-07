from collections import deque

class Room(object):

	def __init__(self, *room):
		self.externalId, self.internalId = room

		self.players = deque()

	def send(self, data):
		for player in self.players:
			player.sendLine(data)

	def sendXt(self, *data):
		for player in self.players:
			player.sendXt(*data)

	def generateRoomString(self):
		roomString = "%".join([player.getPlayerString() for player in self.players])

		return roomString

	def add(self, player):
		self.players.append(player)

		player.sendXt("jr", self.externalId, self.generateRoomString())
		self.sendXt("ap", player.getPlayerString())

		player.room = self

	def remove(self, player):
		self.players.remove(player)

		self.sendXt("rp", player.user.Id)
