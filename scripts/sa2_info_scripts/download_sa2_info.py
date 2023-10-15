from urllib.request import urlretrieve
import os

import pandas as pd

# Accessing all the Victorian Postcodes
post_codes_file_path = "data/landing/sa2/CG_POSTCODE_2021_SA2_2021.xlsx"
df = pd.read_excel(post_codes_file_path)

# Filter the Victorian postcodes (they are in between 3000 and 4000)
vic_df = df.loc[df["POSTCODE"].isin(range(3000,4000))]

# drop the null rows and get all of the SA2 codes
vic_df = vic_df.dropna(subset=["SA2_CODE_2021"])


sa2_codes = vic_df['SA2_CODE_2021'].values

# make sure to get all unique SA2 code starts with a 2 (Victorian SA2 codes) 
sa2_codes = [str(int(x)) for x in sa2_codes if str(x).startswith('2')]
sa2_codes = list(dict.fromkeys(sa2_codes))


URL_TEMPLATE = 'https://dbr.abs.gov.au/json/csv/SA2_'

# Create file location
output_dir = "data/landing/suburb_info"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# For each SA2 code download the summary file's data
for code in sa2_codes:
    url = f'{URL_TEMPLATE}{code}.csv'
    urlretrieve(url, f'{output_dir}/{code}.csv')


