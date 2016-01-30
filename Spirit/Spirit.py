import logging
from logging.handlers import RotatingFileHandler

import json
import os

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

		# Set up logging
		generalLogDirectory = os.path.dirname(self.server["Logging"]["General"])
		errorsLogDirectory = os.path.dirname(self.server["Logging"]["Errors"])

		if not os.path.exists(generalLogDirectory):
			os.mkdir(generalLogDirectory)

		if not os.path.exists(errorsLogDirectory):
			os.mkdir(errorsLogDirectory)

		universalHandler = RotatingFileHandler(self.server["Logging"]["General"],
		                                       maxBytes=2097152, backupCount=3, encoding="utf-8")
		self.logger.addHandler(universalHandler)

		errorHandler = logging.FileHandler(self.server["Logging"]["Errors"])
		errorHandler.setLevel(logging.ERROR)
		self.logger.addHandler(errorHandler)

		# TODO - make the engine string retrieve the values from the configuration attribute
		self.databaseEngine = create_engine('mysql://root@localhost/spirit', pool_recycle=3600)
		self.createSession = sessionmaker(bind=self.databaseEngine)

		self.logger.info("Spirit module initialized")

	def buildProtocol(self, addr):
		session = self.createSession()

		player = self.protocol(session)

		return player

	def start(self):
		self.logger.info("Starting server..")

		port = int(self.server["Port"])

		self.logger.info("Listening on port {0}".format(port))

		reactor.listenTCP(port, self)
		reactor.run()