import fiona
import geopandas as gpd
from shapely.geometry import shape
import polyline
import googlemaps
from datetime import datetime, timedelta
import json
import pickle

gmaps = googlemaps.Client(key='apikey')

originalPoints = gpd.read_file('C:\\gitrepos\Commute\\LatLonPoints.shp')

#this fails if shapefile has no records so copy schema from other shapefile
try:
    alreadyQueriedPoints = gpd.read_file('C:\\gitrepos\Commute\\TrafficData.shp')
except:
    alreadyQueriedPoints = gpd.GeoDataFrame(columns=originalPoints.columns)

#tilde inverses resultset, so we get points not containd in alreadyQueriedPoints
pointsToQuery = originalPoints[~originalPoints.contains(alreadyQueriedPoints)].geometry
print(pointsToQuery.head())

pointIndex = 0

destination = 'commute destination'

#set departure time to next monday at 7:30 am
departureTime = datetime.now() + timedelta(days=(7-datetime.now().weekday()))
departureTime = departureTime.replace(hour=7, minute=30, second=0, microsecond=0)

try:
    while pointIndex < 500:    
        
        origin = '{0},{1}'.format(pointsToQuery.iloc[pointIndex].y,pointsToQuery.iloc[pointIndex].x)
        print(origin)
        
        directions_result = gmaps.directions(origin=origin, destination=destination, departure_time=departureTime)

        travel_time = directions_result[0]['legs'][0]['duration_in_traffic']['value'] / 60
        alreadyQueriedPoints.loc[len(alreadyQueriedPoints)+1] = [len(alreadyQueriedPoints)+1,travel_time,pointsToQuery.iloc[pointIndex]]

        pointIndex += 1    
finally:
    print(alreadyQueriedPoints.head())
    alreadyQueriedPoints.to_file('C:\\gitrepos\Commute\\TrafficData.shp')
