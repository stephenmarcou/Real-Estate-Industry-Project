import pandas as pd
import os

school_location_raw = pd.read_csv("data/raw/school_data/school_locations_raw.csv")
vce_results_raw = pd.read_csv("data/raw/school_data/vce_results_raw.csv")

school_location_raw = school_location_raw[["education_sector", "school_name", "school_type", "address_postcode", 
                                           "lga_name", "coordinate"]]

vce_results_raw = vce_results_raw[["school", "2022 ranking", "median vce score"]]

merged_school_data = pd.merge(school_location_raw, vce_results_raw, 
                              left_on="school_name", right_on="school", how="left")
merged_school_data = merged_school_data.drop(["school"], axis=1)

# ensure that only secondary schools got vce score
columns_vce_results = list(vce_results_raw.columns)
null_value_list = [None for i in range(len(columns_vce_results))]

merged_school_data.loc[merged_school_data["school_type"] == "primary", columns_vce_results] = null_value_list


school_data_curated_dir = "data/curated/school_data/"
if not os.path.exists(school_data_curated_dir):
    os.makedirs(school_data_curated_dir)
    
merged_school_data.to_csv(school_data_curated_dir + "school_data.csv", index=False)

# merge sa2 codes with school_data
sa2_postcode_data = pd.read_csv("data/curated/sa2_to_postcode/sa2_to_postcode.csv")
school_data_s2 = pd.merge(merged_school_data, sa2_postcode_data, left_on="address_postcode", right_on="postcode")
school_data_s2 = school_data_s2.drop("address_postcode", axis=1)

school_data_s2.to_csv(school_data_curated_dir + "school_data_s2.csv", index=False)




# --- preprocess university_location_raw.csv ---
university_raw = pd.read_csv("data/raw/school_data/university_location_raw.csv")
# drop irrelevant columns
university_raw = university_raw.drop(["fid", "ogc_fid", 'address1', "country", "street_address",
       "provider_type", "latitude", "longitude", "wkb_geometry"], axis=1)

# only keep victorian universities
university_raw = university_raw[university_raw["state"] == "vic"]


university_raw.to_csv(school_data_curated_dir + "university_location_curated.csv", index=False)

# merge sa2 with university data
university_data_s2 = pd.merge(university_raw, sa2_postcode_data, left_on="postcode", right_on="postcode", how = "left")

university_data_s2.to_csv(school_data_curated_dir + "university_location_curated_s2.csv", index=False)


