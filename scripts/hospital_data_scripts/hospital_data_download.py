from urllib.request import urlretrieve
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

hospital_url = "https://www.healthcollect.vic.gov.au/HospitalLists/MainHospitalList.aspx"
def scrape_hospitals(url):
    response = requests.get(hospital_url)
    soup = BeautifulSoup(response.content, "html.parser")
    table_header = soup.find("table", {"id": "x:201238496.9:mkr:headerContent.hdn"})
    table_hospital_data = soup.find("table", {"id": "x:201238496.4:mkr:dataTbl.hdn"})

    data = []
    if table_header:
        # Iterate through the rows of the table and extract data
        for row in table_header.find_all("tr"):
            #print(row)
            # Extract the text from each cell in the row
            cells = row.find_all("th")
            row_data = [cell.get_text(strip=True) for cell in cells]
            data.append(row_data)
            
    if table_hospital_data:
        # Iterate through the rows of the table and extract data
        for row in table_hospital_data.find_all("tr"):
            #print(row)
            # Extract the text from each cell in the row
            cells = row.find_all("td")
            row_data = [cell.get_text(strip=True) for cell in cells]
            data.append(row_data)
    data_df = pd.DataFrame(data)
    data_df.columns = data_df.iloc[0]
    data_df = data_df.iloc[1:]
    return data_df
            

            
hospital_df = scrape_hospitals(hospital_url)

output_dir_hospital = "data/landing/hospital_data/"
if not os.path.exists(output_dir_hospital):
    os.makedirs(output_dir_hospital)

hospital_df.to_csv(output_dir_hospital + "hospital_data.csv", index=False)
