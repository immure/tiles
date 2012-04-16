import cherrypy 
import pprint
import sys
import traceback
from jinja2 import Environment, FileSystemLoader
from tiles.addons.plugin import TileSource
from tiles.addons import * #@UnusedWildImport


def get_date(tile):
	return tile.date


env = Environment(loader=FileSystemLoader('tiles/web/templates'))
class Root:
	@cherrypy.expose
	def index(self):

		tiles = []
		plugins = []

		# Load modules manually for now

		for plugin in TileSource.plugins: #@UndefinedVariable
			plugin_data = {'name' : plugin.__name__, 'enabled' : plugin().get_enabled(), 'errors' : []}

			if (plugin().get_enabled()):
				try:
					t = plugin().get_tiles()
					for i in t:
						tiles.append(i)
				except:
					print "Unexpected error:", sys.exc_info()[0]
					traceback.print_exc()
					plugin_data.get('errors').append(sys.exc_info()[0])
			plugins.append(plugin_data)

		tiles = sorted(tiles, key=get_date, reverse=True)	


		tmpl = env.get_template('index.html')
		return tmpl.render(tiles_i=tiles,msg='',menu_link=get_module_menu_link,plugins=plugins)

	@cherrypy.expose
	@cherrypy.tools.allow(methods=['POST'])
	def select_modules(self, **post_vars):
		pprint.PrettyPrinter().pprint(post_vars)
		for plugin in TileSource.plugins: #@UndefinedVariable
			name = plugin.__name__
			if (name not in post_vars and plugin().get_enabled()):
				print 'Disabling ' + name
				plugin().disable()
			if (name in post_vars and not plugin().get_enabled()):
				print 'Enabling ' + name
				plugin().enable()
		raise cherrypy.HTTPRedirect("/")


def get_module_menu_link(module):
	name = module['name']
	enabled = module['enabled']
	link= "<img src='img/" + name + ".png' width=16 height=16 />"
	link=link+"<input type='checkbox' name='" + name + "' value='" + name + "'"
	if (enabled):
		link=link+" checked='yes'"
	link=link+"'/>"
	if (module['errors'].__len__() > 0):
		link = link + "<span class='error'>" + name + "</span>"
	else:
		link = link + name
	return link

