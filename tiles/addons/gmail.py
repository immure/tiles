import dateutil.parser
import feedparser
import urllib2
import cherrypy
from tiles.addons.plugin import TileSource
from tiles.obj.tile import Tile
from time import mktime
from datetime import datetime


def get_unread_msgs_atom(user, passwd):
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='New mail feed',
        uri='https://mail.google.com',
        user='%s' % user,
        passwd=passwd
    )
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    feed = urllib2.urlopen('https://mail.google.com/mail/feed/atom/important')
    return feed.read()


class GMail(TileSource):

	
	def __init__(self):
		self.module = "GMail"

	def get_tiles(self):
		user = self.get_prop('username')
		password = self.get_prop('password')
		rawfeed = get_unread_msgs_atom(user, password)
		f = feedparser.parse(rawfeed)
		tiles = []
		for entry in f.entries:
			t = Tile()
			t.title = entry.title.encode("utf-8").decode("utf-8")
			t.module = self.module
			t.text = entry.summary.encode("utf-8").decode("utf-8")
			t.link = entry.link.encode("utf-8").decode("utf-8")
			t.date = datetime.fromtimestamp(mktime(entry.issued_parsed))
			tiles.append(t)
		return tiles

