from shapely.geometry import Point, mapping
import fiona
from fiona.crs import from_string
from math import ceil

increment = 0.01

xMin = -97.1
xMax = -96.5
yMin = 32.8
yMax = 33.3

xCount = ceil((xMax-xMin)/increment)
yCount = ceil((yMax-yMin)/increment)

points = []

for x in range(1, xCount):
    for y in range(1, yCount):
        points.append(Point(xMin + (x*increment), yMin + (y*increment)))

crs = from_string("+datum=WGS84 +ellps=WGS84 +no_defs +proj=longlat")

schema = {
    'geometry' : 'Point',
    'properties' : {
        'id' : 'int',
        'TravelTime' : 'float'
    }
}

id=1

with fiona.open('C:\\gitrepos\Commute\\LatLonPoints.shp','w',driver='ESRI Shapefile',crs=crs, schema=schema) as sf:
    for point in points:
        sf.write({'geometry': mapping(point), 'properties':{'id':id, 'TravelTime':None}})
        id += 1