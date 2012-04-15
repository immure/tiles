from tiles.tile import Tile
import datetime


t = Tile()
t.title = "Hello"
t.module = "GMail"
t.text = "Text"
t.link = "http://mail.google.com/"
t.date = datetime.datetime.now()


print t.title
print t.module
print t.text
print t.link
print t.date
