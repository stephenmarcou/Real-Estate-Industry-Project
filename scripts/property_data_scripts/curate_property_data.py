import pandas as pd
import re

property_data = pd.read_csv("data/raw/rental_data.csv")

# We're using regular expressions to match patterns like "$X,XXX" or "$XXX" and extract the numeric part
property_data['Rent Amount'] = property_data['cost_text'].str.extract(r'\$ ?(\d{1,4}(?:,\d{3})*)')[0]
property_data['Rent Amount'] = property_data['Rent Amount'].str.replace(',', '')

property_data['Rent Amount'] = pd.to_numeric(property_data['Rent Amount'], errors='coerce').astype(pd.Int64Dtype())


# The error data is data that didnt have numeric prices
error_rents = property_data[property_data['Rent Amount'].isna()]
property_data = property_data[property_data['Rent Amount'].notna()]
error_rents = error_rents[error_rents['cost_text'].str.contains(r'\d', regex=True)]

#Getting rid of the Rent2own with No Deposit, on holf, and contact agent
strings_to_check = ['Rent2own', 'Hold', 'contact']
mask = error_rents['cost_text'].str.contains('|'.join(strings_to_check), case=False, na=False)
error_rents = error_rents[~mask]

# This is accessing prices that dont have a dollar sign
error_rents = error_rents.reset_index(drop=True)
error_rents['Rent Amount'] = error_rents['cost_text']
error_rents['Rent Amount'] = error_rents['Rent Amount'].str.replace(',', '')
error_rents['Rent Amount'] = error_rents['Rent Amount'].str.extractall(r'(\d{3,4})').astype(str).groupby(level=0).agg(','.join)



#accessing the error rents after the last preprocessing
error_rents['Rent Amount'] = pd.to_numeric(error_rents['Rent Amount'], errors='coerce').astype(pd.Int64Dtype())



# The error data is data that didnt have numeric prices
error_rents2 = error_rents[error_rents['Rent Amount'].isna()]

# Dealing with price ranges and imputing the average value
ranges = error_rents2['cost_text'].str.extract(r'(\d+)-(\d+)')

ranges = ((pd.to_numeric(ranges[1]) + pd.to_numeric(ranges[0]))/2)
ranges.dropna(inplace=True)
ranges = ranges.astype(int)

for idx, value in ranges.items():
    error_rents2.loc[error_rents2.index == idx, 'Rent Amount'] = value


error_rents2 = error_rents2[error_rents2['Rent Amount'].notna()]

# deal with all the monthly stuff pcm, monthly etc
error_rents3 = property_data[property_data['cost_text'].str.contains('month')]
property_data = property_data[~property_data['cost_text'].str.contains('month')]


exclude_strings = ['week', 'pw', 'p/w', '/w']
pattern = '|'.join(map(re.escape, exclude_strings))
error_rents3 = error_rents3[~error_rents3['cost_text'].str.contains(pattern)]
error_rents4 = error_rents3[error_rents3['cost_text'].str.contains(pattern)]


#getting rid of cars parks and storage spaces
exclude_strings = ['Car', 'CAR', 'Storage', 'STORAGE', 'parking']
pattern = '|'.join(map(re.escape, exclude_strings))
error_rents3 = error_rents3[~error_rents3['title'].str.contains(pattern)]

#now transform monthly rents to weekly
factor = 12/52.1429 
error_rents3['Rent Amount'] = error_rents3['Rent Amount'].apply(lambda x: x * factor).astype(int)

#join the errors with the original good ones
# concetenate error_rents, error_rents2, property_data - once I drop the nans
cleaned_properties = pd.concat([property_data, error_rents, error_rents2, error_rents3, error_rents4], ignore_index=True)
cleaned_properties.rename(columns={'Rent Amount': 'Weekly Rent Amount'}, inplace=True)
#11722 rows


#taking the postcode out
cleaned_properties['Postcode'] = cleaned_properties['name'].str.extract(r'\bVIC\s(\d{4})\b')

#dropping the rows with no postcode 
cleaned_properties['Postcode'] = pd.to_numeric(cleaned_properties['Postcode'], errors='coerce')
cleaned_properties = cleaned_properties.dropna()
cleaned_properties['Postcode'] = cleaned_properties['Postcode'].astype(int)


#turning beds, baths and parking to ints
columns_to_convert = ['beds', 'baths', 'parking']
for col in columns_to_convert:
    cleaned_properties[col] = cleaned_properties[col].astype(str)
    cleaned_properties[col] = cleaned_properties[col].str.extract(r'(\d+)')
    cleaned_properties[col] = cleaned_properties[col].fillna(0).astype(int)


# Specify the folder and file path
folder_path = 'data/curated/'
file_name = 'rental_data.csv' 

# Save the DataFrame to the specified folder
cleaned_properties.to_csv(folder_path + file_name, index=False)