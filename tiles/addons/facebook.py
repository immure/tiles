import dateutil.parser
import feedparser
import urllib2
import pprint
from tiles.obj.tile import Tile
from time import mktime
from datetime import datetime

def get_feed():
    feed = urllib2.urlopen(cherrypy.config['addons.facebook.notifications.rss'])
    return feed.read()


class Facebook:
	
	def __init__(self):
		self.module = "Facebook"

	def get_tiles(self):
		rawfeed = get_feed()
		f = feedparser.parse(rawfeed)
		tiles = []
		for entry in f.entries:
			t = Tile()
			t.title = entry.title.encode("utf-8").decode("utf-8")
			t.module = self.module
			t.text = entry.summary.encode("utf-8").decode("utf-8")
			t.link = entry.link.encode("utf-8").decode("utf-8")
			t.date = datetime.fromtimestamp(mktime(entry.published_parsed))
			tiles.append(t)
		return tiles

#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(feedparser.parse(get_feed()))
