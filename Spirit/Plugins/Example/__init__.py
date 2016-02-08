import logging

import zope.interface

from .. import Plugin
from ...Events import Events

class Example(object):
	zope.interface.implements(Plugin)

	author = "Spirit Team"
	version = 1.0
	description = "A plugin to verify plugin system functionality and demonstrate implementation"

	def __init__(self):
		self.logger = logging.getLogger("Spirit")

		self.events = Events()

		self.events.on("j#js", self.handleJoinWorld)

	def handleJoinWorld(self, player, data):
		self.logger.info("[Example] Received joinWorld data")
		print data

	def ready(self):
		self.logger.info("Example plugin is ready!")
