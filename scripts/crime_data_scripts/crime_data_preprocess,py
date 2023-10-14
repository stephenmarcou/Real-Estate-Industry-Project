import pandas as pd

# Path to the downloaded Excel file
excel_file_path = "data/landing/Data_Tables_Property_Items_Visualisation_Year_Ending_March_2023.xlsx"

# Read the Excel file into a Pandas DataFrame
xls = pd.ExcelFile(excel_file_path)

# List the sheet names in the Excel file
sheet_names = xls.sheet_names

# Print the sheet names
print("Sheet names:", sheet_names)

# Table 01 has lots of granularity, with number of items, value, postcode, property item by year
# Table 02 has offence count and offence type by LGA
# Table 04 has offence count by LGA 
# Table 06 has postcode offence count year


# Example: Read a specific sheet into a DataFrame
sheet_name_to_read = "Table 06"  
df = pd.read_excel(excel_file_path, sheet_name=sheet_name_to_read)


# Removing the postcodes that are not integers
df['Postcode'] = pd.to_numeric(df['Postcode'], errors='coerce')
df = df.dropna(subset=['Postcode'])

# conterting the postcodes to integers 
df['Postcode'] = df['Postcode'].astype(int)


# Group the DataFrame by 'suburb_town' and count the unique 'postcode' values in each group
postcode_counts = df.groupby('Suburb/Town')['Postcode'].nunique().reset_index()

# Rename the columns for clarity (optional)
postcode_counts.columns = ['Suburb/Town', 'unique_postcode_count']

# Accessing the suburbs that have more then 1 unique postcode
greater1postcodesuburbs = postcode_counts[postcode_counts['unique_postcode_count'] != 1]


# Ascot, Merijig, Newtown, Thomson are 2 distinct suburbs so naturally will have 2 suburbs
# Boronia and Wantirna South have some Muddles
# Melbourne has a few issues

dont_touch = set(['Ascot', 'Merijig', 'Newtown', 'Thomson', 'Wantirna South', 'Melbourne'])
double_up_suburbs = set(greater1postcodesuburbs['Suburb/Town'].values)

suburbs_to_fix = list(double_up_suburbs - dont_touch)


true_suburb_postcode = {}

# Setting the suburb postcode to be the postcode that appeats more often across the years the data has been collected
for suburb in suburbs_to_fix:
    group = df[df['Suburb/Town'] == suburb]
    postcode_counts = group['Postcode'].value_counts()
    postcode_with_highest_count = postcode_counts.idxmax()
    true_suburb_postcode[suburb] = postcode_with_highest_count


# converting the incorrect postcodes to the correct postcodes
for suburb, postcode in true_suburb_postcode.items():
    df.loc[df['Suburb/Town'] == suburb, 'Postcode'] = postcode
   


# Now for fixing 'Wantirna South', 'Melbourne'
# drop all 3155, as there isnt much there and we already have boronia data
df = df.drop(df[(df['Suburb/Town'] == 'Wantirna South') & (df['Postcode'] == 3155)].index)


# Melbourne University is being called Melbourne so lets change that
# Change 'Suburb/Town' to 'Melbourne University' where 'Postcode' is 3052 and 'Suburb/Town' is 'Melbourne'
df.loc[(df['Postcode'] == 3052) & (df['Suburb/Town'] == 'Melbourne'), 'Suburb/Town'] = 'Melbourne University'
df[df['Postcode'] == 3181]

# Drop rows where 'Postcode' is 3181 and 'Suburb/Town' is 'Melbourne'
df = df.drop(df[(df['Postcode'] == 3181) & (df['Suburb/Town'] == 'Melbourne')].index)



# sorting by postcode
df_sorted = df.sort_values(by=['Postcode', 'Year'])



# Specify the folder and filename for the CSV file
folder_path = 'data/raw/'
file_name = 'crime_data.csv'

# Combine the folder path and filename to create the full file path
file_path = folder_path + file_name

# Save the DataFrame as a CSV file in the specified folder
df_sorted.to_csv(file_path, index=False)


