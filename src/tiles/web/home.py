import cherrypy 
import pprint
import json
from jinja2 import Environment, FileSystemLoader
from tiles.addons.plugin import TileSource
from tiles.addons import * #@UnusedWildImport
from tiles.services.tile_service import TileService
from pprint import PrettyPrinter
from datetime import datetime





env = Environment(loader=FileSystemLoader('tiles/web/templates'))
class Root:
	
	service = TileService()
	pprint = PrettyPrinter()
	
	@cherrypy.expose
	def index(self):

		service_results = self.service.get_tiles()

		
		plugins = service_results['plugins']	
		tiles = service_results['tiles']

		tmpl = env.get_template('index.html')
		return tmpl.render(tiles_i=tiles,msg='',menu_link=get_module_menu_link,plugins=plugins)
	
	@cherrypy.expose
	def json(self, jsoncallback, _):
		timestamp = int(_)/1000
		print datetime.fromtimestamp(timestamp)
		service_results = self.service.get_tiles(True)
		plugins = service_results['plugins']
		tiles = []
		for t in service_results['tiles']:
			t.date = ''
			tiles.append(t.__dict__)
		j = pprint.pformat({ 'plugins' : plugins, 'tiles' : tiles })
		
		return jsoncallback + '(' + json.dumps(tiles) + ')'
	
	@cherrypy.expose
	def ajax(self):
		plugins = self.service.get_plugins(True);
		for plugin_d in plugins:
			plugin = plugin_d['plugin']
			if plugin.get_enabled() and not plugin.is_logged_in():
				plugin.log_in()
		tmpl = env.get_template('ajaxy.html')
		return tmpl.render(menu_link=get_module_menu_link,plugins=plugins)
		
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

