import pandas as pd
import numpy as np

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

# Create dataset with important features
cols = ["Estimated resident population (no.)", "Population density (persons/km2)",
        "Employed (no.)", "Unemployed (no.)", "In the Labour force (no.)", "Total persons aged 15 years and over (no.)",
        'Median equivalised total household income (weekly) ($)',
        'Land area (ha)', 'Median weekly household rental payment ($)', 
        'Average family size (no. of persons)', 'Total families (no.)', 'Total dwellings (no.)']

# Census data years
years = ["2011", "2016", "2021"]
df_1 = (pd.DataFrame(columns= cols, index=sa2_codes)).rename_axis('SA2_Code', axis=1)
df_2 = (pd.DataFrame(columns= cols, index=sa2_codes)).rename_axis('SA2_Code', axis=1)
df_3 = (pd.DataFrame(columns= cols, index=sa2_codes)).rename_axis('SA2_Code', axis=1)

folder_path = 'data/landing/suburb_info/'

# Go through each SA2 Code and obtain the important information from each summary file
for code in sa2_codes:
    
    # Read SA2 Code data file
    trial_df = pd.read_csv(f"{folder_path}{code}.csv")

    # Store information for each year of census data
    for year in years:
        try:
            
            pop_density = trial_df[year].loc[trial_df["Description"] == "Population density (persons/km2)"].values[0]
            
            num_employed = trial_df[year].loc[trial_df["Measure Code"] == "LF_6"].values[0]
            
            num_unemployed = trial_df[year].loc[trial_df["Measure Code"] == "LF_3"].values[0]
            
            num_labour = trial_df[year].loc[trial_df["Measure Code"] == "LF_2"].values[0]
            
            work_pop = trial_df[year].loc[trial_df["Measure Code"] == "LF_9"].values[0]
            
            income = trial_df[year].loc[trial_df["Description"] == 'Median equivalised total household income (weekly) ($)'].values[0]

            area = trial_df[year].loc[trial_df["Description"] == 'Land area (ha)'].values[0]

            median_rent = trial_df[year].loc[trial_df["Description"] == 'Median weekly household rental payment ($)'].values[0]

            avg_family = trial_df[year].loc[trial_df["Description"] == 'Average family size (no. of persons)'].values[0]

            total_family = trial_df[year].loc[trial_df["Description"] == 'Total families (no.)'].values[0]
            
            
            if year == "2011":
                
                # Use data from 2017 for 2011 because it did not exist
                pop_size = trial_df["2017"].loc[trial_df["Description"] == "Estimated resident population (no.)"].values[0]
                
                dwellings = trial_df["2017"].loc[trial_df["Description"] == 'Total dwellings (no.)'].values[0]
                
                # Store information into the 2011 dataframe
                df_1.loc[code] = [pop_size, pop_density, num_employed, num_unemployed, num_labour, work_pop,
                            income, area, median_rent, avg_family, total_family, dwellings]
                
            elif year == "2016":
                
                # Use data from 2019 for 2016 because it did not exist
                pop_size = trial_df["2019"].loc[trial_df["Description"] == "Estimated resident population (no.)"].values[0]
                
                dwellings = trial_df["2019"].loc[trial_df["Description"] == 'Total dwellings (no.)'].values[0]
                
                # Store information into the 2016 dataframe
                df_2.loc[code] = [pop_size, pop_density, num_employed, num_unemployed, num_labour, work_pop,
                            income, area, median_rent, avg_family, total_family, dwellings]
            
            else:
                
                pop_size = trial_df[year].loc[trial_df["Description"] == "Estimated resident population (no.)"].values[0]
                
                dwellings = trial_df[year].loc[trial_df["Description"] == 'Total dwellings (no.)'].values[0]
                
                # Store information into the 2021 dataframe
                df_3.loc[code] = [pop_size, pop_density, num_employed, num_unemployed, num_labour, work_pop,
                            income, area, median_rent, avg_family, total_family, dwellings]
        
        except IndexError:
            continue
    
# After retreiving all information save the files
df_1.to_csv("data/curated/suburb_info_2011.csv", index_label="SA2_codes")
df_2.to_csv("data/curated/suburb_info_2016.csv", index_label="SA2_codes")
df_3.to_csv("data/curated/suburb_info_2021.csv", index_label="SA2_codes")
