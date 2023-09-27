import pandas as pd
import geopandas as gpd
import os
import json

sf = gpd.read_file("data/landing/sa2/SA2_2021_AUST_GDA2020.shp")
postcode_sa2_df = pd.read_excel("data/landing/sa2/CG_POSTCODE_2021_SA2_2021.xlsx")


# convert sa2 codes to numeric
sf["SA2_CODE21"] = pd.to_numeric(sf["SA2_CODE21"], errors="coerce")
sf = sf.dropna(subset=["SA2_CODE21"])

# only keep victoria records
sf = sf[sf["STE_NAME21"] == "Victoria"]
postcode_sa2_df = postcode_sa2_df.dropna(subset=["POSTCODE"])

gdf = gpd.GeoDataFrame(pd.merge(postcode_sa2_df, sf, left_on = "SA2_CODE_2021", right_on="SA2_CODE21", how="inner"))


# save as geoJSON
geojson_output_dir = "data/curated/geojson/"
if not os.path.exists(geojson_output_dir):
    os.makedirs(geojson_output_dir)

gdf.to_file(geojson_output_dir + "shapefile.geojson", driver="GeoJSON")


# preprocess sa2 to postcode excel file
sa2_postcode_data = pd.read_excel("data/landing/sa2/CG_POSTCODE_2021_SA2_2021.xlsx")
sa2_postcode_data.columns = sa2_postcode_data.columns.str.lower()
sa2_postcode_data = sa2_postcode_data[["postcode", "sa2_code_2021", "sa2_name_2021"]]
sa2_postcode_data = sa2_postcode_data.dropna(subset=["postcode", "sa2_code_2021"])


sa2_output_dir = "data/curated/sa2_to_postcode/"
if not os.path.exists(sa2_output_dir):
    os.makedirs(sa2_output_dir)

sa2_postcode_data.to_csv(sa2_output_dir + "sa2_to_postcode.csv", index=False)


