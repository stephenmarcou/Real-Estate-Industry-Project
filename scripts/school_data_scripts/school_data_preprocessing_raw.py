import pandas as pd
import re
import os
# preprocess school_location.csv

school_loc_df = pd.read_csv("data/landing/school_data/school_locations.csv", encoding="latin1")
school_loc_df.columns =  school_loc_df.columns.str.lower()

# lowercase relevant string columns
school_loc_df[["school_name", "education_sector", "school_type", "address_state"]] = school_loc_df[
    ["school_name", "education_sector", "school_type", "address_state"]].apply(lambda x: x.str.lower())

# remove non-alphabetical characters from school name
school_loc_df["school_name"] = school_loc_df["school_name"].apply(lambda x: re.sub("[^a-zA-Z\s]","", x).strip())

# remove school from name
school_loc_df["school_name"] = school_loc_df["school_name"].apply(lambda x: x.replace("school", "").strip())

# add coordinate column
def combine_x_y(row):
    return tuple([float(row["y"]), float(row["x"])])
school_loc_df["coordinate"] = school_loc_df.apply(combine_x_y, axis=1)

raw_dir_school_data = "data/raw/school_data/"
if not os.path.exists(raw_dir_school_data):
    os.makedirs(raw_dir_school_data)

school_loc_df.to_csv(raw_dir_school_data + "school_locations_raw.csv", index=False)


# --- preprocess vce_results.csv ---
vce_results_df = pd.read_csv("data/landing/school_data/vce_results.csv", encoding="latin1")
vce_results_df.columns =  vce_results_df.columns.str.lower()
vce_results_df["school"] = vce_results_df["school"].apply(lambda x: x.lower())
# remove non-alphabetical characters from school name
vce_results_df["school"] = vce_results_df["school"].apply(lambda x: re.sub("[^a-zA-Z\s]","", x).strip())

# remove school from name
vce_results_df["school"] = vce_results_df["school"].apply(lambda x: x.replace("school", "").strip())


vce_results_df.to_csv(raw_dir_school_data + "vce_results_raw.csv", index=False)


# --- preprocess universities_locations_2018.csv ---
university_df = pd.read_csv("data/landing/school_data/universities_locations_2018.csv")
university_df.columns = university_df.columns.str.lower()

# lowercase relevant string columns
university_df[["institution", "campus_name", "address2", "suburb", "state"]] = university_df[
    ["institution", "campus_name", "address2", "suburb", "state"]].apply(lambda x: x.str.lower())

def combine_long_lat(row):
    return tuple([float(row["latitude"]), float(row["longitude"])])
university_df["coordinate"] = university_df.apply(combine_long_lat, axis=1)
university_df.to_csv(raw_dir_school_data + "university_location_raw.csv", index=False)
