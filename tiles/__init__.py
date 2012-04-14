#!python
import cherrypy
import os.path

from tiles.web.home import Root as Root

current_dir = os.path.dirname(os.path.abspath(__file__))


#from jinja2 import Environment, FileSystemLoader
#from tiles.obj.tile import Tile
#from tiles.addons.gmail import GMail
#
#env = Environment(loader=FileSystemLoader('tiles/web/templates'))
#
#
#class Root:
#	@cherrypy.expose
#	def index(self):
#		g = GMail()
#		t = g.get_tiles()
#		tmpl = env.get_template('index.html')
#		return tmpl.render(tiles=t)

#cherrypy.quickstart(Home())

