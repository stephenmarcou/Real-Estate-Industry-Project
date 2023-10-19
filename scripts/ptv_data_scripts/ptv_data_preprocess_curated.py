import pandas as pd
import math

rent_data = pd.read_csv("../data/curated/rental_data.csv")
metro_stations_data = pd.read_csv("../data/curated/PTV/stations_with_postcodes.csv")
regional_stations_data = pd.read_csv("../data/curated/PTV/stations_with_postcodes.csv")

stations_data = metro_stations_data.append(regional_stations_data, ignore_index=True)

# 'coordinates' column in rent_data contains lists of [latitude, longitude]
rent_data['latitude'] = rent_data['coordinates'].apply(lambda x: float(x.split(',')[0].strip('[ ]')))
rent_data['longitude'] = rent_data['coordinates'].apply(lambda x: float(x.split(',')[1].strip('[ ]')))

# Function to calculate Haversine distance between two sets of coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
    """ Calculates the haversine distance between 2 coordinates in terms of lattitude and longitude
        and returns the distance in kms"""
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance

# Create an empty list to store the minimum distances
min_distances = []

# Iterate over each house in rent_data
for house_idx, house_row in rent_data.iterrows():
    house_lat = house_row['latitude']
    house_lon = house_row['longitude']
    nearest_distance = float('inf')

    # Iterate over each train station in station data
    for station_idx, station_row in stations_data.iterrows():
        station_lat = station_row['LATITUDE']
        station_lon = station_row['LONGITUDE']

        # Calculate Haversine distance
        distance = haversine_distance(house_lat, house_lon, station_lat, station_lon)

        # If this distance is smaller than the previously recorded nearest_distance,
        if distance < nearest_distance:
            nearest_distance = distance

    min_distances.append(nearest_distance)

# Add the minimum distances and corresponding postcodes to the rent_data DataFrame
rent_data['nearest train station'] = min_distances

# Save the updated DataFrame to a CSV file
rent_data.to_csv("../data/curated/rental_data_train_station.csv", index=False)