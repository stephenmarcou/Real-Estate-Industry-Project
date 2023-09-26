from urllib.request import urlretrieve
import os

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

# vic_df = df.loc[df["POSTCODE"].isin(range(3000,4000))]

# # drop the null rows and get all of the SA2 codes
# vic_df = vic_df.dropna(subset=["SA2_CODE_2021"])

# sa2_codes = list((vic_df["SA2_CODE_2021"]))
# sa2_codes = list(dict.fromkeys(sa2_codes))



URL_TEMPLATE = 'https://dbr.abs.gov.au/json/csv/SA2_'

output_dir = "data/landing/suburb_info"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

i = 0
for code in sa2_codes:
    i += 1
    print(i)
    # print(code)
    url = f'{URL_TEMPLATE}{code}.csv'
    urlretrieve(url, f'{output_dir}/{code}.csv')


