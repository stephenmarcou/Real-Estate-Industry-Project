import pandas as pd
import json
import os

folder_path = 'data/landing/'

json_data_list = []

# opening all the json files
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            json_data_list.append(json_data)

#concatenating all the dataframes to make a single dataframe.
dfs = [pd.DataFrame.from_dict(json_data, orient='index') for json_data in json_data_list]
rental_df = pd.concat(dfs)

# Save the DataFrame to a CSV file
rental_df.to_csv('data/raw/rental_data.csv', index=False)