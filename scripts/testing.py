import os

folder_path = 'data/landing/suburb_info'
number_of_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

print(f"Number of files in '{folder_path}': {number_of_files}")


import pandas as pd

# Accessing all the Victorian Postcodes
post_codes_file_path = "data/landing/sa2/CG_POSTCODE_2021_SA2_2021.xlsx"
df = pd.read_excel(post_codes_file_path)

vic_df = df.loc[df["POSTCODE"].isin(range(3000,4000))]

# drop the null rows and get all of the SA2 codes
vic_df = vic_df.dropna(subset=["SA2_CODE_2021"])

# sa2_codes = list((vic_df["SA2_CODE_2021"]))
# sa2_codes = list(dict.fromkeys(sa2_codes))
sa2_codes = vic_df['SA2_CODE_2021'].values

sa2_codes = [str(int(x)) for x in sa2_codes if str(x).startswith('2')]
sa2_codes = list(dict.fromkeys(sa2_codes))

print(len(sa2_codes))

