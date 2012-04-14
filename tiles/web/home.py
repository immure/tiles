import cherrypy
import datetime
from jinja2 import Environment, FileSystemLoader
from tiles.obj.tile import Tile
from tiles.addons.gmail import GMail
from tiles.addons.sabnzbd import SABnzbd
from tiles.addons.facebook import Facebook

def get_date(tile):
	return tile.date


env = Environment(loader=FileSystemLoader('tiles/web/templates'))
class Root:
	@cherrypy.expose
	def index(self):

		tiles = []

		# Load modules manually for now
		g = GMail()
		t = g.get_tiles()
		for i in t:
			tiles.append(i)

		s = SABnzbd()
		for i in s.get_tiles():
			tiles.append(i)

		f = Facebook()
		for i in f.get_tiles():
			tiles.append(i)

		tiles = sorted(tiles, key=get_date, reverse=True)	


		tmpl = env.get_template('index.html')
		return tmpl.render(tiles_i=tiles,msg='',menu_link=get_module_menu_link)

def get_module_menu_link(module):
	return "<img src='img/" + module + ".png' width=16 height=16 /><input type='checkbox' name='" + module + "' value='" + module + "'/>" + module

