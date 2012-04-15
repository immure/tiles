import dateutil.parser
import feedparser
import urllib2
import pprint
import cherrypy
from tiles.addons.plugin import TileSource
from tiles.obj.tile import Tile
from time import mktime
from datetime import datetime



class SABnzbd(TileSource):

	def get_feed(self):
		host = self.get_prop('host')
		apikey = self.get_prop('apikey')
		feed = urllib2.urlopen(host + '/sabnzbd/rss?mode=history&apikey=' + apikey)
		return feed.read()
	
	def __init__(self):
		self.module = "SABnzbd"

	def get_tiles(self):
		rawfeed = self.get_feed()
		f = feedparser.parse(rawfeed)
		tiles = []
		for i in f.entries:
			t = Tile()
			t.title = i.title
			t.module = self.module
			t.text = ""
			t.link = self.get_prop('host')
			t.date = datetime.fromtimestamp(mktime(i.published_parsed))
			tiles.append(t)
		return tiles

