import importlib
import pkgutil
import json
import os

import logging
from logging.handlers import RotatingFileHandler

from collections import deque

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twisted.internet import reactor
from twisted.internet.protocol import Factory

import Handlers
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

		if self.server["World"]:
			self.protocol = Penguin

			self.loadHandlerModules()

			self.logger.info("Running world server")
		else:
			self.protocol = Spheniscidae

			self.logger.info("Running login server")

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

		self.players = deque()
		self.rooms = {}

		self.logger.info("Spirit module initialized")

	def getHandlerModules(self):
		for importer, modname, ispkg in pkgutil.iter_modules(Handlers.__path__):
			yield modname

	def loadHandlerModules(self):
		self.logger.info("Loading handler modules")

		for handlerModule in self.getHandlerModules():
			self.logger.info("Loading " + handlerModule)

			handlerModuleObject = importlib.import_module("Spirit.Handlers." + handlerModule, package="Spirit.Handlers")

			# Exclude the worldHandlers variable at the end
			handlerModuleMethods = dir(handlerModuleObject)[5:-1]

			handlerModuleHandlers = getattr(handlerModuleObject, "worldHandlers")
			inverseModuleHandlers = dict((v, k) for k, v in handlerModuleHandlers.iteritems())

			for handlerModuleMethod in handlerModuleMethods:
				handlerId = inverseModuleHandlers[handlerModuleMethod]
				handlerModuleMethodObject = getattr(handlerModuleObject, handlerModuleMethod)

				setattr(Penguin, handlerModuleMethod, handlerModuleMethodObject)
				Penguin.worldHandlers[handlerId] = handlerModuleMethod

	def buildProtocol(self, addr):
		session = self.createSession()

		player = self.protocol(session, self)

		return player

	def start(self):
		self.logger.info("Starting server..")

		port = int(self.server["Port"])

		self.logger.info("Listening on port {0}".format(port))

		reactor.listenTCP(port, self)
		reactor.run()