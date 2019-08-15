# -*- coding: utf-8 -*-
"""
GBA Map

Created on Thu Aug 15 10:42:34 2019

@author: Maciej Holowko mholowko@gmail.com
"""
import pandas as pd
import geopandas
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from shapely.geometry import Point

#Load the World Map, unify the color to white for all countries, remove Antarctica
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world['Unification'] = pd.DataFrame([1] * 177)
world = world[(world.name!="Antarctica")]

#Create the GeoDataFrame for the BioFoundry points
biofoundries = pd.read_excel('BioFoundries.xlsx')
geometry = [Point(xy) for xy in zip(biofoundries.Latitude, biofoundries.Longitude)]
crs = {'init': 'epsg:2263'} #http://www.spatialreference.org/ref/epsg/2263/
geo_biofoundries = GeoDataFrame(biofoundries, crs=crs, geometry=geometry)
biofoundries['geometry'] = list(zip(biofoundries.Longitude, biofoundries.Latitude))
biofoundries['geometry'] = biofoundries['geometry'].apply(Point)

#Automatic labeling function, works properly, but resutls in clumping
#geo_biofoundries['coords'] = geo_biofoundries['geometry'].apply(lambda x: x.representative_point().coords[:])
#geo_biofoundries['coords'] = [coords[0] for coords in geo_biofoundries['coords']]

#Plot the map
fig = world.plot(cmap='Greys',column='Unification',figsize=(30, 20),edgecolor='black')
geo_biofoundries.plot(ax=fig, marker='o', color='red', markersize=20)

#Required for autolabelling
#for idx, row in geo_biofoundries.iterrows():
#    plt.annotate(s=row['Number'], xy=row['coords'], 
#                 horizontalalignment='left',verticalalignment='bottom',color='blue',size='20')

plt.axis('off')
plt.show()
fig.figure.savefig('GBAmap.png', dpi=600)