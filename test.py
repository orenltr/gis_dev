import os
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point, Polygon
from geopandas.tools import reverse_geocode
import geopandas as gpd
from geopandas.tools.geocoding import geocode

file_path = r'C:\Users\Dell\OneDrive - Technion\טכניון\סמסטר ז\סדנא בפיתוח ממג\code\data\some_posts.csv'
data = pd.read_csv(file_path)
data.head()

data['geometry'] = data.index

for index, row in data.iterrows() :
    row['geometry'] = Point(row['lat'], row['lon'])

print(data)

