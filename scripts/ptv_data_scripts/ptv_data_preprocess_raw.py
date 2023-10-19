from pyspark.sql import SparkSession, functions as F
import sys; sys.executable
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
from pyspark.sql.functions import col, when
import json

# Create a spark session (which will run spark jobs)
spark = (
    SparkSession.builder.appName("MAST30034 Assignment 2")
    .config("spark.sql.repl.eagerEval.enabled", True)
    .config("spark.sql.parquet.cacheMetadata", "true")
    .config("spark.sql.session.timeZone", "Etc/UTC")
    .config('spark.driver.memory', '4g')
    .config('spark.executor.memory', '2g')
    .getOrCreate()
)

gdf_train_station = gpd.read_file('../data/landing/PTV/PTV_METRO_TRAIN_STATION.shp')
gdf_regional_train_station = gpd.read_file('../data/landing/PTV/PTV_REGIONAL_TRAIN_STATION.shp')
gdf_postcode = gpd.read_file('../data/landing/PTV/POSTCODE_POLYGON.shp')

# Drop columns "STOP_ID" and "ROUTEUSSP" from the GeoDataFrame
gdf_train_station = gdf_train_station.drop(columns=["STOP_ID", "ROUTEUSSP"])
gdf_regional_train_station = gdf_regional_train_station.drop(columns=["STOP_ID"])

# Drop unneeded columns from the postcode data
gdf_postcode = gdf_postcode.drop(columns=["UFI", "PFI", "PFI_CR", "UFI_CR", "TASK_ID", "UFI_OLD"])

# Perform a spatial join to assign postal codes to stations
stations_with_postcodes = gpd.sjoin(gdf_train_station, gdf_postcode, how="left", op="within")
regional_stations_with_postcodes = gpd.sjoin(gdf_regional_train_station, gdf_postcode, how="left", op="within")

stations_with_postcodes = stations_with_postcodes.drop(columns=["index_right"])
regional_stations_with_postcodes = regional_stations_with_postcodes.drop(columns=["index_right"])

# Define the file paths for saving the GeoDataFrames in the data folder
data_folder = '../../data/curated/ptv/'

# Save the GeoDataFrames to files in the data folder
gdf_train_station.to_file(data_folder + 'PTV_METRO_TRAIN_STATION.geojson', driver='GeoJSON')
gdf_regional_train_station.to_file(data_folder + 'PTV_REGIONAL_TRAIN_STATION.geojson', driver='GeoJSON')

gdf_postcode.to_file(data_folder + 'POSTCODE.geojson', driver='GeoJSON')

stations_with_postcodes.to_file(data_folder + 'PTV_TRAIN_STATION_POSTCODE.geojson', driver='GeoJSON')