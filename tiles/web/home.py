import cherrypy 
import datetime 
import pprint
from jinja2 import Environment, FileSystemLoader
from tiles.obj.tile import Tile
from tiles.addons.gmail import GMail
from tiles.addons.sabnzbd import SABnzbd
from tiles.addons.facebook import Facebook
from tiles.addons.plugin import TileSource

def get_date(tile):
	return tile.date


env = Environment(loader=FileSystemLoader('tiles/web/templates'))
class Root:
	@cherrypy.expose
	def index(self):

		tiles = []
		plugins = []

		# Load modules manually for now

		for plugin in TileSource.plugins:
			t = plugin().get_tiles()
			plugins.append({'name' : plugin.__name__, 'enabled' : plugin().get_enabled()})
			for i in t:
				tiles.append(i)

		tiles = sorted(tiles, key=get_date, reverse=True)	


		tmpl = env.get_template('index.html')
		return tmpl.render(tiles_i=tiles,msg='',menu_link=get_module_menu_link,plugins=plugins)

def get_module_menu_link(module):
	name = module['name']
	enabled = module['enabled']
	link= "<img src='img/" + name + ".png' width=16 height=16 />"
	link=link+"<input type='checkbox' name='" + name + "' value='" + name + "'"
	if (enabled):
		link=link+" checked='yes'"
	link=link+"'/>" + name
	return link

