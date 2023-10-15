
import pandas as pd
import numpy as np

def merge_supermarket_and_town_data():
    """
    This function merges rental data, supermarket data, and town data and creates a new DataFrame.
    Then it is saved to a CSV file.
    """

    # Get the rental data, the supermarket data and the town data from the curated folder and read it in.
    rental_data = pd.read_csv('../data/curated/rental_data_sf.csv')
    supermarket_data = pd.read_csv('../data/curated/supermarket_data.csv')
    town_data = pd.read_csv('../data/curated/town_distance_data.csv')

    # Merge each of the dataframes to the rental data, one by one, and save the data.
    df = pd.merge(rental_data, supermarket_data, how='left', on='Postcode')
    df = pd.merge(df, town_data, how='left', left_on='Postcode', right_on='postalcode')
    df = df.drop(columns=['lat', 'long', 'postalcode'])
    df.to_csv('../data/curated/rental_data_town_join.csv')

if __name__ == "__main__":
    merge_supermarket_and_town_data()





