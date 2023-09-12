from urllib.request import urlretrieve
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

school_locations_url = "https://www.education.vic.gov.au/Documents/about/research/datavic/dv309_schoollocations2021.csv"

# check if it exists as it makedir will raise an error if it does exist
landing_output_dir_school_data = "data/landing/school_data/"
if not os.path.exists(landing_output_dir_school_data):
    os.makedirs(landing_output_dir_school_data)

def retrieve_url(url, landing_output_dir):
    ''' 
    Function reads in csv file from url, and outputs 
    the csv file at the specified directory by landing_output_dir.
    Is used to read in school location data
    '''
    output_dir = f"{landing_output_dir}/school_locations.csv"
    # download
    urlretrieve(url, output_dir)
    
retrieve_url(school_locations_url, landing_output_dir_school_data)



# -- Scrape VCE results ---

def scrape_vce_results(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('div', {'class': 'table-responsive'})
    
    for table in tables:
        subheader = table.find_previous(lambda tag: tag.name == 'h2')
        if subheader.text == "Top 150 Schools by VCE Success Rate in 2022":
            # Extract data from the table
            data = []
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
                data.append(row_data)
            vce_df = pd.DataFrame(data)
            vce_df.columns = vce_df.iloc[0]
            vce_df = vce_df.iloc[1:]
            
            return vce_df
 
vce_results_url = "https://www.matrix.edu.au/beginners-guide-vce-high-school-rankings/2022-high-school-vce-rankings/"       
vce_df = scrape_vce_results(vce_results_url)
vce_df.to_csv(landing_output_dir_school_data + 'vce_results.csv', index=False)