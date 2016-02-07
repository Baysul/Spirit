import zope.interface

class Plugin(zope.interface.Interface):
	"""
	Plugin interface which all plugins *must* implement.
	"""

	author = zope.interface.Attribute("""The plugin's author which is usually a nickname and an e-mail address.""")
	version = zope.interface.Attribute("""The version of the plugin.""")
	description = zope.interface.Attribute("""Short summary of the plugin's intended purpose.""")

	def ready():
		"""
		Called when the plugin is ready to function.
		:return:
		"""