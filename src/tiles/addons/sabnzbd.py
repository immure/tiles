import feedparser
import urllib2
from tiles.addons.plugin import TileSource
from tiles.obj.tile import Tile
from time import mktime
from datetime import datetime

MAX_TILES = 20

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
		count = 0
		for i in f.entries:
			count = count + 1
			if (count < MAX_TILES):
				t = Tile()
				t.title = "Download Complete"
				t.module = self.module
				t.text = i.title
				t.link = self.get_prop('host')
				t.date = datetime.fromtimestamp(mktime(i.published_parsed))
				print i.title + " - " + str(i.published_parsed)
				tiles.append(t)
		return tiles

