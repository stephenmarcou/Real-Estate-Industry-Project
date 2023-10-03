import pandas as pd
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import time

hospital_curated = pd.read_csv("data/raw/hospital_data/hospital_data_raw.csv")

hospital_curated[
    ["formal name", "emergency capable", "location address", "suburb", "category", "agency type"]] = hospital_curated[
        ["formal name", "emergency capable", "location address", "suburb", "category", "agency type"]]\
            .apply(lambda x: x.str.lower())

hospital_curated = hospital_curated.drop(["other name", "access point"], axis=1)

# only keep hospital
keep_rows = hospital_curated["agency type"].str.contains("hospital")
hospital_curated = hospital_curated[keep_rows]

def address_to_coordinate(row):
    address = row["location address"] + " " + str(row["postcode"]) + " " + row["suburb"]
    print(address)
    while True:
        try:
            geolocator = Nominatim(user_agent="my_request")
        
            #applying geocode method to get the location
            location = geolocator.geocode(address)
            try:
                return tuple([float(location.latitude), float(location.longitude)])
            except AttributeError:
                print("error")
                return None
        
        except GeocoderUnavailable:
            print("GeocoderUnavailable: Retrying in 5 seconds...")
            time.sleep(5)

    
hospital_curated["coordinate"] = hospital_curated.apply(address_to_coordinate, axis=1)

# drop hospitals without coordinate
hospital_curated = hospital_curated.dropna(subset=["coordinate"])

hospital_curated_dir = "data/curated/hospital_data/"
if not os.path.exists(hospital_curated_dir):
    os.makedirs(hospital_curated_dir)
    
hospital_curated.to_csv(hospital_curated_dir + "hospital_data_curated.csv")
