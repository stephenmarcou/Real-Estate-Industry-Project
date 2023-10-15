
import pandas as pd
import geopy.distance
import numpy as np

def create_town_dataframe():
    """
    Reads and processes town data from CSV files and creates a new DataFrame,
    which includes information about town locations, their proximity to city centres,
    and whether they are coastal towns.
        The resulting DataFrame is saved as a CSV file.
    """

    # Read in the town data, proximity data
    df = pd.read_csv('../data/raw/all_town_data.csv', index_col=[0])
    df = df.replace(to_replace='Ballarat Central', value='Ballarat')

    # Read in the city centre data
    city_centres = pd.read_csv('../data/landing/city_centres.csv', index_col=[0])
    city_centres.columns = ['name']
    city_centres['city_centre'] = [True for i in range(city_centres.shape[0])]

    # Read in the coastal town data
    coastal_towns = pd.read_csv('../data/raw/coastal_towns.csv')
    coastal_towns['coastal_towns'] = [True for i in range(coastal_towns.shape[0])]
    coastal_towns.columns = ['name', "coastal"]


    # Merge the main dataframe with city centres
    df = pd.merge(city_centres, df, on='name', how='outer')
    df['city_centre'] = df['city_centre'].fillna(value=False)

    # Merge the main dataframe with coastal towns
    df = pd.merge(df, coastal_towns, on='name', how='left')
    df['coastal'] = df['coastal'].fillna(value=False)

    # Calculate the nearest city centre for each town and their distances.
    melb_coords = (-37.81302, 144.96111)
    closest_city_centre = []
    closest_cc_dist = []
    dist_to_melb = []

    for _, row in df.iterrows():
        
        # Find distance to melbourne and save
        p = geopy.distance.geodesic(melb_coords, (row['lat'], row['lng'])).km
        dist_to_melb.append(p) 

        # Find the closest city centre and save
        if row['city_centre']:
            closest_city_centre.append(row['name'])
            closest_cc_dist.append(0)
            continue
        
        q = df[df['city_centre'] == True].copy()
        
        min_dist = np.inf
        closest = None
        for name, qlat, qlong in zip(q['name'], q['lat'], q['lng']):
            curr = geopy.distance.geodesic((qlat, qlong), (row['lat'], row['lng'])).km
            if curr < min_dist:
                min_dist = curr
                closest = name

        closest_city_centre.append(closest)
        closest_cc_dist.append(min_dist)

    # Add these values to the dataframe
    df['closest_city_centre'] = closest_city_centre
    df['closest_cc_dist'] = closest_cc_dist
    df['dist_to_melb'] = dist_to_melb
    df = df.drop_duplicates().reset_index(drop=True)

    # Here we are creating a dataframe that converts from postcode to town (and vice-versa)
    new_df = df[['name', 'postalcode']]
    new_df.rename(columns={'name': 'town', 'postalcode': 'postcode'}, inplace=True)
    new_df.to_csv('../data/curated/postcode_to_town.csv')

    # Groupby postcode and agreegrate information, then save the dataframe 
    gb = df.groupby(['postalcode']).agg(
        lat=('lat', 'mean'),
        long=('lat', 'mean'),
        city_centre=('city_centre', 'first'),
        closest_city_centre=('closest_city_centre', 'first'), 
        coastal=('coastal', 'first'),
        closest_cc_dist=('closest_cc_dist', 'mean'),
        dist_to_melb=('dist_to_melb', 'mean'),
    )

    gb.to_csv('../data/curated/town_distance_data.csv')

if __name__ == "__main__":
    create_town_dataframe()

