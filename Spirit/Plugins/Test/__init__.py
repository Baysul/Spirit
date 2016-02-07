import logging

import zope.interface

from .. import Plugin
from ...Events import Events

class Test(object):
	zope.interface.implements(Plugin)

	author = "Spirit Team"
	version = 1.0
	description = "A plugin to verify plugin system functionality"

	def __init__(self):
		self.logger = logging.getLogger("Spirit")

		self.events = Events()

		self.events.on("j#js", self.handleJoinWorld)

	def handleJoinWorld(self, player, data):
		self.logger.info("[Test] Received joinWorld data")
		print data

	def ready(self):
		self.logger.info("Test plugin is ready!")
