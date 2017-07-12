# gmapsstaticapi

gmapsstaticapi is based on the [Static Maps API] module. 
The main purpose is to simplify the extraction of maps.
Sample usage:

```py
from avbr_gmapsstaticapi import Point, staticMapImage

pos = Point(40.7473,-73.9875)
mymap = staticMapImage(pos, zoom = 14, mapWidth = 640, mapHeight=640, gmapskey="#Yourkey")

markers = [
    (40.74738701268981, -73.98759841918945),
    (40.76559148640381, -73.97884368896484),
    (40.72098167171645,-73.99755477905273)
    ]

print(mymap.limens)
print(mymap.getPosition(markers[0]))

img = mymap.openImg(markers)
img.show()

```

   [Static Maps API]: <https://developers.google.com/maps/documentation/static-maps/>

### Installation

This module requires PILLOW library. "pip install pillow"
Install the module by running "pip install ." in terminal/cmd.

```
cd directoryofpackage
pip install .
```


### Todos

 - Add more functionality


License
----

MIT

**Free Software, Hell Yeah!**
