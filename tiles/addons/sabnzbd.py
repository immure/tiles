import dateutil.parser
import feedparser
import urllib2
import pprint
import cherrypy
from tiles.obj.tile import Tile
from time import mktime
from datetime import datetime



def get_feed():
		host = cherrypy.config['addons.sabnzbd.host']
		apikey = cherrypy.config['addons.sabnzbd.apikey']
		feed = urllib2.urlopen(host + '/sabnzbd/rss?mode=history&apikey=' + apikey)
		return feed.read()


class SABnzbd:
	
	def __init__(self):
		self.module = "SABnzbd"

	def get_tiles(self):
		rawfeed = get_feed()
		f = feedparser.parse(rawfeed)
		tiles = []
		for i in f.entries:
			t = Tile()
			t.title = i.title
			t.module = self.module
			t.text = ""
			t.link = host
			t.date = datetime.fromtimestamp(mktime(i.published_parsed))
			tiles.append(t)
		return tiles

