import pandas as pd 
import os

hospital_df = pd.read_csv("data/landing/hospital_data/hospital_data.csv")

# lowercase column names
hospital_df.columns = hospital_df.columns.str.lower()

hospital_columns = list(hospital_df.columns)

# lower case string columns
hospital_df[
    ["formal name", "emergency capable", "location address", "suburb", "category", "agency type"]] = hospital_df[
        ["formal name", "emergency capable", "location address", "suburb", "category", "agency type"]]\
            .apply(lambda x: x.str.lower())

# save raw hospital data
hospital_raw_dir = "data/raw/hospital_data/"
if not os.path.exists(hospital_raw_dir):
    os.makedirs(hospital_raw_dir)
    
hospital_df.to_csv(hospital_raw_dir + "hospital_data_raw.csv", index=False)