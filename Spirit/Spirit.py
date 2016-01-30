import logging
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twisted.internet import reactor
from twisted.internet.protocol import Factory

from Spheniscidae import Spheniscidae
from Penguin import Penguin

class Spirit(Factory, object):

	def __init__(self, *kw, **kwargs):
		self.logger = logging.getLogger("Spirit")

		configFile = kw[0]
		with open(configFile, "r") as fileHandle:
			self.config = json.load(fileHandle, "utf-8")

		serverName = kwargs["server"]
		self.server = self.config["Servers"][serverName]

		self.protocol = Penguin if self.server["World"] else Spheniscidae

		# TODO - make the engine string retrieve the values from the configuration attribute
		self.databaseEngine = create_engine('mysql://root@localhost/spirit')
		self.createSession = sessionmaker(bind=self.databaseEngine)

		self.logger.info("Spirit module initialized")

	def buildProtocol(self, addr):
		session = self.createSession()

		player = Spheniscidae(session)

		return player

	def start(self):
		self.logger.info("Starting server..")

		port = int(self.server["Port"])

		self.logger.info("Listening on port {0}".format(port))

		reactor.listenTCP(port, self)
		reactor.run()