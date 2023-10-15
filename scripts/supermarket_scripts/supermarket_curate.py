import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def supermarket_curate():
    """
    Curates supermarket data from a CSV file, organizes it, and saves it in a new CSV file.
    """

    # List of major supermarket names
    major_supermarkets = ['coles', 'woolworths', 'foodworks', 'iga', 'aldi', 'ritchies', 'safeway']

    # Read the raw data from a CSV file
    lines = pd.read_csv('../data/landing/supermarket_raw_data.csv', header=None)
    
    # Initialize an empty list to store curated data
    lst = []
    prev = None

    for i in range(len(lines.values)):
        # Flag to alternate between lines, if we have dud data
        swap = False

        line = lines.values[i][0]

        # Check if we need to swap the order of 'prev' and 'line'
        if not swap:
            if i % 2 == 0:
                prev = line
            else:
                # Extract last four numbers (Postcode) and town name (the rest)
                pscd = line[-4:]
                town = line[:-5]
                if pscd[0] == '3':
                    # Append the data if we have a valid postcode (i.e. it starts with 3)
                    lst.append([prev, town, int(pscd)])
                else:
                    # If we have dud data, swap
                    swap = True

        # As above but if flagged
        if swap:
            if i % 2 == 1:
                prev = line
            else:
                pscd = line[-4:]
                town = line[:-5]
                if pscd[0] == '3':
                    lst.append([prev, town, int(pscd)])
                else:
                    swap = False

    # Create a DataFrame from the curated list
    df = pd.DataFrame(lst, columns=['Supermarket', 'Town', 'Postcode'])
    df = df.drop_duplicates().reset_index(drop=True)

    # Create a new column 'Major' indicating if the supermarket is a major one
    df['Major'] = df['Supermarket'].str.contains('|'.join(major_supermarkets))

    # Group the data by 'Postcode' and calculate the total number of supermarkets and major supermarkets
    gb = df.groupby(['Postcode']).agg(
            Total_Supermarkets=('Supermarket', 'count'),
            Major_Supermarkets=('Major', 'sum'),
        )

    gb.to_csv('../data/curated/supermarket_data.csv')

if __name__ == "__main__":
    # Call the function when this file is run
    supermarket_curate()

