# gmapsstaticapi

gmapsstaticapi is based on the [Static Maps API] module. 
The main purpose is to simplify the extraction of maps.
Sample usage:

```py
from avbr_gmapsstaticapi import Point, staticMapImage

markers = [
    (40.74738701268981, -73.98759841918945),
    (40.76559148640381, -73.97884368896484),
    (40.72098167171645,-73.99755477905273)
    ]

pos = Point(markers[0])
mymap = staticMapImage(pos, zoom = 14, mapWidth = 640, mapHeight=640, gmapskey="#Yourkey")
```

Extract limens:

```
print(mymap.limens)
```

Get position of marker 1:
```
print(mymap.getPosition(Point(markers[0])))
```

Create map with markers:
```
img = mymap.openImg(markers=markers)
img.show()
```

### Docs

http://avbr-gmapsstaticapi.readthedocs.io/en/latest/overview.html


### Installation

To get the latest version, simply do:

```
pip install https://github.com/Anton-vBR/avbr_gmapsstaticapi/archive/master.zip --upgrade
```


### Todos

 - Add more functionality


License
----

MIT

**Free Software, Hell Yeah!**


[Static Maps API]: <https://developers.google.com/maps/documentation/static-maps/>