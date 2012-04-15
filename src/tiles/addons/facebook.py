import dateutil.parser
import feedparser
import urllib2
import pprint
import cherrypy
from tiles.addons.plugin import TileSource
from tiles.obj.tile import Tile
from time import mktime
from datetime import datetime

# https://graph.facebook.com/fql?q={"query1":"SELECT sender_id, created_time, title_text, href from notification where recipient_id=me()","query2":"SELECT name, uid, pic_square from user where uid in (select sender_id from #query1)"}&accesstoken=

class Facebook(TileSource):

	def get_feed(self):
		feed = urllib2.urlopen(self.get_prop('notifications.rss'))
		return feed.read()
	
	def __init__(self):
		self.module = "Facebook"

	def get_tiles(self):
		rawfeed = self.get_feed()
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
