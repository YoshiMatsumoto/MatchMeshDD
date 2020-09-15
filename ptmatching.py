import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree

# Shapely
from shapely.ops import nearest_points

# PostgreSQL
import psycopg2

# reading files
# df_building = pd.read_csv("Building.csv")
# gdf_building = gpd.GeoDataFrame(df_building, geometry=gpd.points_from_xy(df_building.X, df_building.Y))
gdf_building = gpd.read_file("Building.shp")
gdf_road = gpd.read_file("Road.shp")


# find nearest pt
def ckdnearest(gd_building, gd_road):
    n_building = np.array(list(gd_building.geometry.apply(lambda x: (x.x, x.y))))
    n_road = np.array(list(gd_road.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(n_road)
    dist, idx = btree.query(n_building, k=1)
    gdf = pd.concat(
        [gd_building.reset_index(drop=True), gd_road.loc[idx, gd_road.columns != 'geometry'].reset_index(drop=True),
          pd.Series(dist, name='dist')], axis=1)
    return gdf

# nearest ID
gdf_result = ckdnearest(gdf_building, gdf_road)

gdf_result.to_file("result.shp")


# PostgreSQL
connection = psycopg2.connect("host=192.168.24.97 port=9403 dbname=sampledb user=user password=password")
cur = connection.cursor()
cur.execute("SELECT ")