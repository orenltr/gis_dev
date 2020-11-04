import os
import geopandas as gpd
import numpy as np
import pandas as pd
import descartes
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import nearest_points
from geopandas.tools import reverse_geocode
import geopandas as gpd
from geopandas.tools.geocoding import geocode
import matplotlib.pyplot as plt

file_path = r'C:\Users\Dell\OneDrive - Technion\טכניון\סמסטר ז\סדנא בפיתוח ממג\code\data\some_posts.csv'
df = pd.read_csv(file_path)


#%% md

# creating points from the data and insert to dataframe

#%%

# for index, row in df.iterrows() :
#     geometry = Point(row['lat'], row['lon'])

geometry = gpd.points_from_xy(df.lon,df.lat)
df['geometry'] = geometry

print(df.shape)
df.head()


#%% md

# Convert DataFrame into a GeoDataFrame and export to shapefile

#%%

gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
gdf.crs

# save to shp
# gdf.to_file("Kruger_posts.shp")

#%% md

# get map and plot points

#%%

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.crs

# #%%
# world = world.to_crs(epsg=4326)
# world.crs

# restrict to Africa.
ax = world[world.continent == 'Africa'].plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
# restrict to South Africa.
# ax = world[world.name == 'South Africa'].plot(figsize=(10, 10), alpha=0.5, edgecolor='k')

gdf.plot(ax=ax,color='red')
plt.show

#%% md

#### part 2

# Reproject into EPSG:32735

#%%

world = world.to_crs(epsg=32735)
world.crs

#%%

grouped = gdf.groupby('userid')
grouped.count()

#%%

movements = gpd.geodataframe
movements.columns = ['userid', 'geometry']
# Aggregate these points with the GroupBy
# movements = df.groupby(['userid'])['geometry'].apply(lambda x: LineString(x.tolist()))
# movements = gpd.geodataframe(movements, geometry=df['geometry'])
# movements = gdf[['userid','geometry']].copy()
# movements = movements.groupby('userid')
#%%
# grouped.apply(lambda x: x.sort_values(by='timestamp'))
movements = grouped['geometry'].apply(lambda x: LineString(x.tolist()) if x.size>1 else x)
movements = gpd.GeoDataFrame({'userid': movements['userid'], geometry: 'geometry'})
x=1
# for key, values in grouped:
#     values.sort_values(by='timestamp')
#     if values.size > 1:
#         values['geometry'].apply(lambda x: LineString(x.tolist()) if x.size>1 else None)
#         # movementsline = LineString(values['geometry'])
#         movements.append({'userid': key, 'geometry':movementsline}, ignore_index=True)
#     else:
#         movements.append({'userid': key, 'geometry':values['geometry']}, ignore_index=True)

#%%
#%%

file_path = r'C:\Users\Dell\OneDrive - Technion\טכניון\סמסטר ז\סדנא בפיתוח ממג\code\data\activity_locations.txt'
activity_locations = pd.read_csv(file_path, sep=';')
activity_locations.head()

#%%

# Geocode addresses with Nominatim backend
geo = geocode(activity_locations['addr'])
# print(geo.crs)
geo.crs = {'init': 'epsg:4326'}
# geo = geo.to_crs(epsg=4326)
# geo.crs="EPSG:4326"
geo.head(2)

#%%


ax = world[world.continent == 'Asia'].plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
geo.plot(ax=ax,color='red')
plt.show()

#%%
# reading bus stops shapefile

bus_stops_file_path = r"C:\Users\Dell\OneDrive - Technion\טכניון\סמסטר ז\סדנא בפיתוח ממג\code\data\Bus_Stops.shp"
bus_stops = gpd.read_file(bus_stops_file_path)
bus_stops.head()

#%%
# find nearest bus stops

pts = bus_stops.geometry.unary_union
nearest = nearest_points(activity_locations.loc[0]['geometry'],pts)[5]
print(nearest)