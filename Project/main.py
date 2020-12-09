import pandas as pd
import numpy as np
import sqlite3
from pprint import pprint
import folium
from folium import plugins
from folium.plugins import HeatMap

import matplotlib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
# import pygeohash as pgh
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#%%
# source of the data is https://www.kaggle.com/rtatman/188-million-us-wildfires
# conn = sqlite3.connect("FPA_FOD_20170508.sqlite")
pd.set_option('display.float_format', lambda x: '%.2f' % x)
conn = sqlite3.connect("FPA_FOD_20170508.sqlite")
# df = pd.read_sql_query("SELECT LATITUDE, LONGITUDE, FIRE_YEAR, CONT_DATE,DISCOVERY_DATE, CONT_TIME, FIRE_SIZE, STAT_CAUSE_DESCR FROM Fires;", conn)
df = pd.read_sql_query("SELECT * FROM Fires LIMIT 10;", conn)
df.head()

#%%
heat_df = df[["LATITUDE","LONGITUDE", "FIRE_YEAR", "FIRE_SIZE"]]
# limit number of points, to get a processible result
heat_df = heat_df[heat_df["FIRE_SIZE"] > 1800]
heat_df = heat_df.dropna(axis=0, subset=["LATITUDE","LONGITUDE"])

# List comprehension to make out list of lists
heat_data = [[row["LATITUDE"],row["LONGITUDE"]] for index, row in heat_df.iterrows()]
del heat_df

#%%
map_ = folium.Map(location=[df["LATITUDE"].mean(), df["LONGITUDE"].mean()],
                    tiles = "Stamen Terrain",
                    zoom_start = 3)

# Plot it on the map
HeatMap(heat_data, min_opacity=.4, max_val=.8).add_to(map_)

# Display the map
map_