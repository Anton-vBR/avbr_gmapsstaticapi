
# coding: utf-8

# Google
# -------
# https://developers.google.com/maps/documentation/javascript/maptypes
# https://developers.google.com/maps/documentation/javascript/examples/map-coordinates
# 
# Stack overflow
# ----------------
# https://stackoverflow.com/questions/12507274/how-to-get-bounds-of-a-google-static-map

import os
import math
import io
from PIL import Image, ImageDraw
from urllib import request

class Point :
    def __init__(self,lt,ln):
        self.lat = lt
        self.lng = ln

class staticMapImage:
    
    def __init__(self, point, zoom = 10, mapHeight = 640, mapWidth = 640, gmapskey = None):
        
        self.TILE_SIZE = 256
        self.scale = 2
        self.mapHeight = mapHeight
        self.mapWidth = mapWidth
        self.zoom = zoom
        self.centerCoord = point
        self.centerCoord_mercator = self.project(point)
        self.limens_mercator, self.limens = self.getLimens()
        self.gmapskey = gmapskey
        if gmapskey:
            self.url = self.getUrl()
            self.img = self.getImg()   
        self.PositionFunction = self.getPositionFunction()
    
    def project(self,latLng):
        siny = math.sin(latLng.lat * math.pi / 180);

        # Truncating to 0.9999 effectively limits latitude to 89.189. This is
        # about a third of a tile past the edge of the world tile.
        siny = min(max(siny, -0.9999), 0.9999);

        return {
            'x' : self.TILE_SIZE * (0.5 + latLng.lng / 360),
            'y' : self.TILE_SIZE * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi))
        }
    
    def getUrl(self):
        return "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom={}&scale={}&size={}x{}&key={}".format(
            self.centerCoord.lat,
            self.centerCoord.lng,
            self.zoom,
            self.scale,
            self.mapWidth,
            self.mapHeight,
            self.gmapskey)
    
    def getImg(self):
        buffer = io.BytesIO(request.urlopen(self.url).read())
        return buffer
    
    def openImg(self, markers = []):
        img = Image.open(self.img).convert("RGB") # Open image in RGB
        draw = ImageDraw.Draw(img, 'RGBA') # Create a draw object
        
        x=10
        # Add markers to map (circles)
        for marker in markers:
            
            point = Point(marker[0],marker[1])
            XY = self.getPosition(point)
            if XY != "Either Lat or Lng outside bbox":
                a = XY[0]
                b = XY[1]
                if len(marker) > 2:
                    draw.ellipse((a-x,b-x,a+x,b+x), fill=marker[2], outline=(0,0,0))
                else:
                    draw.ellipse((a-x,b-x,a+x,b+x), fill=(100,100,100,100), outline=(0,0,0))
                 
        del draw # delete draw object
        return img

    def unproject_lng(self,x):
        # Calculate lng
        lng = ( x / self.TILE_SIZE  - 0.5) * 360 
        return lng

    def unproject_lat(self,y):
        # Calculate lat
        latRadians = ( y- self.TILE_SIZE / 2) / - (self.TILE_SIZE / (2 * math.pi))
        lat = ( 2 * math.atan(math.exp(latRadians)) - math.pi / 2 ) / (math.pi / 180) 
        return lat

    def getLimens(self):

        x = self.centerCoord_mercator["x"]
        y = self.centerCoord_mercator["y"]

        scale = 2**self.zoom

        N = y-(self.mapHeight/2)/scale
        E = x+(self.mapWidth/2)/scale
        S = y+(self.mapHeight/2)/scale
        W = x-(self.mapWidth/2)/scale

        return ({
            'N' : N,
            'E' : E,
            'S' : S,
            'W' : W,
        },
        {
            'N' : self.unproject_lat(N),
            'E' : self.unproject_lng(E),
            'S' : self.unproject_lat(S),
            'W' : self.unproject_lng(W)    
        })

    def getPosition(self, latlng):
        
        # Convert WGS84 to Mercator
        coord = self.project(latlng)
        
        # Calculate positions 
        Pixel_XY = self.PositionFunction(coord["x"],coord["y"])
        
        return Pixel_XY
        
    def getPositionFunction(self):
    
        # Get positions
        N = self.limens_mercator["N"]
        E = self.limens_mercator["E"]
        S = self.limens_mercator["S"]
        W = self.limens_mercator["W"]
        
        # calc lat-function constants (a+bx)      
        b = self.mapHeight / (S-N)
        a = 0 - b * N
        
        # calc lng-function constants (c+dx)
        d = self.mapWidth / (E-W)
        c = 0 - d * W
        
        # Define return function
        def returnPositionFunction(X_mercator, Y_mercator):
            
            # Check if projection is inside bounds
            if X_mercator > E or X_mercator < W:
                return "Either Lat or Lng outside bbox"
            if Y_mercator > S or Y_mercator < N:
                return "Either Lat or Lng outside bbox"
            
            # Calc X and Y position on image
            Pixel_X = self.scale * (d * X_mercator + c)
            Pixel_Y = self.scale * (b * Y_mercator + a)
            
            return (Pixel_X, Pixel_Y)
        
        return returnPositionFunction