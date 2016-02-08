import importlib
import pkgutil
import json
import os

import logging
from logging.handlers import RotatingFileHandler

from collections import deque

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twisted.internet import reactor, defer
from twisted.web.client import getPage
from twisted.internet.protocol import Factory

import Handlers, Plugins
from Spheniscidae import Spheniscidae
from Penguin import Penguin
from Room import Room

class Spirit(Factory, object):

	def __init__(self, *kw, **kwargs):
		self.logger = logging.getLogger("Spirit")

		configFile = kw[0]
		with open(configFile, "r") as fileHandle:
			self.config = json.load(fileHandle, "utf-8")

		serverName = kwargs["server"]
		self.server = self.config["Servers"][serverName]

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

		engineString = "mysql://{0}:{1}@{2}/{3}".format(self.config["Database"]["Username"],
		                                                self.config["Database"]["Password"],
		                                                self.config["Database"]["Address"],
		                                                self.config["Database"]["Name"])

		self.databaseEngine = create_engine(engineString, pool_recycle=3600)
		self.createSession = sessionmaker(bind=self.databaseEngine)

		self.players = deque()

		self.logger.info("Spirit module initialized")

		self.loadPlugins()

		if self.server["World"]:
			self.protocol = Penguin

			self.loadHandlerModules()

			self.loadRooms()

			self.loadItems()

			self.logger.info("Running world server")
		else:
			self.protocol = Spheniscidae

			self.logger.info("Running login server")

	def loadPlugins(self):
		if not hasattr(self, "plugins"):
			self.plugins = {}

		pluginModules = self.getPackageModules(Plugins)

		for pluginModule in pluginModules:
			self.loadPlugin(pluginModule)

	def loadPlugin(self, pluginName):
		packageName = "Spirit.Plugins.{0}".format(pluginName)
		pluginModule = importlib.import_module(packageName, package=packageName)

		pluginObject = getattr(pluginModule, pluginName)()

		if Plugins.Plugin.providedBy(pluginObject):
			self.plugins[pluginName] = pluginObject

			pluginObject.ready()

		else:
			self.logger.warn("{0} plugin object doesn't provide the plugin interface".format(pluginName))

	def getPackageModules(self, package):
		for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
			yield modname

	def downloadCrumbs(self, url):
		deferredDownload = defer.Deferred()

		def handleRequestComplete(resultData):
			if not os.path.exists("crumbs"):
				os.mkdir("crumbs")

			crumbsFile = "crumbs/" + os.path.basename(url)

			with open(crumbsFile, "w") as fileHandler:
				fileHandler.write(resultData)

			deferredDownload.callback(None)

		getPage(url).addCallback(handleRequestComplete)

		return deferredDownload

	def loadItems(self):
		if not hasattr(self, "items"):
			self.items = {}

		def parseItemCrumbs(downloadResult=None):
			with open("crumbs/paper_items.json", "r") as fileHandle:
				items = json.load(fileHandle)

				for item in items:
					itemId = item["paper_item_id"]
					self.items[itemId] = item["cost"]

			self.logger.info("{0} items loaded".format(len(self.items)))

		if not os.path.exists("crumbs/items.json"):
			self.downloadCrumbs("http://cdn.clubpenguin.com/play/en/web_service/game_configs/paper_items.json")\
				.addCallback(parseItemCrumbs)

		else:
			parseItemCrumbs()

	def loadRooms(self):
		if not hasattr(self, "rooms"):
			self.rooms = {}

		def parseRoomCrumbs(downloadResult=None):
			with open("crumbs/rooms.json", "r") as fileHandle:
				rooms = json.load(fileHandle).values()

				internalId = 0

				for room in rooms:
					externalId = room["room_id"]
					internalId += 1

					if not externalId in self.rooms:
						self.rooms[externalId] = Room(externalId, internalId)

			self.logger.info("{0} rooms loaded".format(len(self.rooms)))

		if not os.path.exists("crumbs/rooms.json"):
			self.downloadCrumbs("http://cdn.clubpenguin.com/play/en/web_service/game_configs/rooms.json")\
				.addCallback(parseRoomCrumbs)

		else:
			parseRoomCrumbs()

	def loadHandlerModules(self):
		for handlerModule in self.getPackageModules(Handlers):
			importlib.import_module("Spirit.Handlers." + handlerModule, package="Spirit.Handlers")

		self.logger.info("Handler modules loaded")

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