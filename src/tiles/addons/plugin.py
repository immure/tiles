import cherrypy


class PluginMount(type):
	def __init__(cls, name, bases, attrs):
		if not hasattr(cls, 'plugins'):
			# This branch only executes when processing the mount point itself.
			# So, since this is a new plugin type, not an implementation, this
			# class shouldn't be registered as a plugin. Instead, it sets up a
			# list where plugins can be registered later.
			cls.plugins = []
		else:
			# This must be a plugin implementation, which should be registered.
			# Simply appending it to the list is all that's needed to keep
			# track of it later.
			cls.plugins.append(cls)

class TileSource:
	__metaclass__ = PluginMount

	def get_prop(self, name):
		return cherrypy.config['addons.' + self.__class__.__name__ + '.' + name]		
	
	def get_enabled(self):
		return cherrypy.config['addons.' + self.__class__.__name__ + '.enabled']

	def set_enabled(self, enabled):
		cherrypy.config.update({'addons.' + self.__class__.__name__ + '.enabled' : enabled})

	def set_prop(self, name, value): 
		cherrypy.config.update({'addons.' + self.__class__.__name__ + '.' + name : value})

	def disable(self):
		self.set_enabled(False)

	def enable(self):
		self.set_enabled(True)
