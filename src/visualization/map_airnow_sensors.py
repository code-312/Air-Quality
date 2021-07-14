from datetime import datetime
import os
os.chdir('../../')

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from src.config import EPA_KEY
from src.data import pull_airnow_sensor_data

# pull sensor data from AirNow
sensor_data = pull_airnow_sensor_data(
    api_key=EPA_KEY,
    start_date='2021-06-30', 
    end_date='2021-06-30', 
    measures=['OZONE','PM25','CO'],
    bbox=[-87.912584,41.587576,-87.522570,42.109292]
)

# pull unique monitor locations
monitors = sensor_data[['Latitude','Longitude']].drop_duplicates()

# convert monitor locations to geodataframe
gdf = gpd.GeoDataFrame(
    monitors,
    crs='EPSG:4326',
    geometry=gpd.points_from_xy(monitors.Longitude, monitors.Latitude), 
).to_crs('EPSG:3857')

# create point for approx center of McKinley Park
mck_park = Point(-87.6805366, 41.8310785)
gdf_mck = gpd.GeoSeries([mck_park], crs='EPSG:4326')
gdf_mck = gdf_mck.to_crs('EPSG:3857') # convert CRS projection


# create map of sensors
ax = gdf.plot(
    figsize=(10, 15), 
    alpha=0.7, 
    color='red'
)

# plot McKinley Park area
gdf_mck.plot(
    ax=ax, 
    alpha=0.7,
    marker='s',
    markersize=500
)

# label McKinley Park
an2 = ax.annotate(
    "McKinley Park", xy=(gdf_mck.geometry.x[0], gdf_mck.geometry.y[0]-1000),
    textcoords="offset points",xytext=(-50,-30), 
    arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=90")
)

# add background map
ctx.add_basemap(ax)

ax.set_axis_off()

plt.savefig('figures/chicago_airnow_radar_map.png', bbox_inches='tight')