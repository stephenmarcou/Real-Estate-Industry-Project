
import pandas as pd
import os

def preprocess_all_towns():
    """
    Helper function that preprocesses town data stored in separate CSV files. It combines these individual town data files into a single DataFrame, removes duplicates and
    unnecessary columns, and then saves the combined data to a new CSV file.
    """


    folder = '../data/landing/all_towns_lat_long/'

    # Get a list of files that are not hidden files
    files = [file for file in os.listdir(folder) if not file.startswith('.')]
    df = pd.DataFrame()

    # Loop through files and concatenate them to the main dataframe
    for file in files:
        current_data = pd.read_csv(folder + "/" + file ,  encoding = "ISO-8859-1")  
        df = pd.concat([df, current_data])

    df = df.drop_duplicates().reset_index().drop(columns=['Unnamed: 0', 'index'])

    # Save the main dataframe
    df.to_csv('../data/raw/all_town_data.csv')

if __name__ == "__main__":
    preprocess_all_towns()

