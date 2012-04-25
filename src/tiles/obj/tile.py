import datetime
import json

class Tile:

	def __init__(self):
		self.title = ""
		self.module = ""
		self.text = ""
		self.link = ""
		self.date = ""
		self.thumbs = []
		self.mainimage = ""

	def __str__(self):
		return self.module + " Tile: " + self.title

	def get_time_since(self):
		now = datetime.datetime.now()
		d = now - self.date
		return d

	def get_time_since_str(self):
		return pretty_date(self.date)
	
	def json(self):
#		objs = {}
#		objs['title'] = self.title
#		objs['module'] = self.module
#		objs['text'] = self.text
#		objs['link'] = self.link
#		#objs['date'] = self.date
#		objs['thumbs'] = self.thumbs
#		objs['mainimage'] = self.mainimage
		self.date = 'None'
		return json.dumps(self, default=json_encode_tile)
	
def json_encode_tile(tile):
	if not isinstance(tile, Tile):
		raise TypeError("%r is not JSON serializable" % (tile,))
	
	tile.date = None
	return tile.__dict__
	
def pretty_date(time=False):
	"""
	Get a datetime object or a int() Epoch timestamp and return a
	pretty string like 'an hour ago', 'Yesterday', '3 months ago',
	'just now', etc
	"""
	from datetime import datetime
	now = datetime.now()
	if type(time) is int:
		diff = now - datetime.fromtimestamp(time)
	elif isinstance(time, datetime):
		diff = now - time 
	elif not time:
		diff = now - now
	second_diff = diff.seconds
	day_diff = diff.days

	if day_diff < 0:
		return 'just now'

	if day_diff == 0:
		if second_diff < 10:
			return "just now"
		if second_diff < 60:
			return str(second_diff) + " seconds ago"
		if second_diff < 120:
			return  "a minute ago"
		if second_diff < 3600:
			return str(second_diff / 60) + " minutes ago"
		if second_diff < 7200:
			return "an hour ago"
		if second_diff < 86400:
			return str(second_diff / 3600) + " hours ago"
	if day_diff == 1:
		return "Yesterday"
	if day_diff < 7:
		return str(day_diff) + " days ago"
	if day_diff < 31:
		return str(day_diff / 7) + " weeks ago"
	if day_diff < 365:
		return str(day_diff / 30) + " months ago"
	return str(day_diff / 365) + " years ago"
