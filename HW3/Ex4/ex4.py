
#%% import
# used to handle data
import pandas as pd

# used to handle geo data
from shapely.ops import transform, Point
from geopandas.tools import reverse_geocode
import geopandas as gpd

# used for manipulating directory paths
import os

# Scientific and vector computation for python
import numpy as np

# Optimization module in scipy
from scipy import optimize

# # library written for this exercise providing additional functions for assignment submission, and others
# import utils

# Plotting library
from matplotlib import pyplot as plt

import folium

import subprocess
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from sklearn.cluster import KMeans, DBSCAN, MiniBatchKMeans

import plotly.express as px
#%%
# read data
NYU_POIs = gpd.read_file('NYC_POIs.shp')
NYU_POIs = gpd.GeoDataFrame(NYU_POIs,crs={'init': 'epsg:4326'})
central_park_polygon = gpd.read_file('central_park_polygon.shp')  # digitized in qgis
flickr = pd.read_csv('flickr_output.txt')

flickr['point'] = list(zip(flickr.X, flickr.Y))
flickr['geometry'] = flickr['point'].apply(Point)
flickr.head()

# 'point' column is no longer needed
flickr = flickr.drop('point',1)
# turn the data frame into geodataframe
flickr = gpd.GeoDataFrame(flickr, geometry='geometry', crs={'init': 'epsg:4326'})

#%%
# getting only the points inside central park
pip = NYU_POIs.within((central_park_polygon.loc[0,'geometry']))
NYU_POIs = NYU_POIs.loc[pip]
pip = flickr.within((central_park_polygon.loc[0,'geometry']))
flickr = flickr.loc[pip]

#%%
plt.figure()
ax = flickr.plot(color='red',alpha=0.5, markersize=0.01)

central_park_polygon.plot(ax=ax,color='green',alpha=0.5, markersize=0.01)

NYU_POIs.plot(ax=ax,color='blue',alpha=0.5, markersize=0.5)
plt.show
#%%
flickr_small = flickr.sample(frac = 0.01)

# NYU_POIs = NYU_POIs.to_crs({'init': 'epsg:32116'})
flickr_small = flickr_small.to_crs({'init': 'epsg:32116'})
flickr_small['X'] = flickr_small.geometry.values.x
flickr_small['Y'] = flickr_small.geometry.values.y

#%%
# finding optimal number of cluster using the knee method
ssd = []
for i in range(2, 100):
    km = KMeans(n_clusters=i)
    km.fit_predict(flickr_small[['X','Y']])
    ssd.append(km.inertia_)


plt.plot(range(2,100), ssd)
plt.show()

#%%

km = KMeans(n_clusters=100)
km.fit_predict(flickr[['X','Y']])

flickr_small['cluster'] = km.labels_
plt.figure(figsize=(12,8))
ax = flickr.plot(c=km.labels_, markersize=0.1)

plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='blue',marker= 'X', s=5)
NYU_POIs.plot(ax=ax,color='red',marker= 'x', markersize=5)
plt.show()
