from urllib.request import urlretrieve
import os
import requests
import zipfile
import shutil

# Define local file paths and output directories
local_file_path_zip_postcode = "postcode_files.zip"
local_file_path_zip_sa2_postcode = "SA2_postcode_files.zip"
output_dir_postcode = "data/landing/postcode/"

# Check if the output directory for postcode files exists; if not, create it
if not os.path.exists(output_dir_postcode):
    os.makedirs(output_dir_postcode)
        
def download_zip_file(url, output_dir, local_file_path, extract_content = True):
    """ Function downloads zip file from url and opens the zip and saves the content """
    
    # Send a request to the URL to retrieve the ZIP file content
    response = requests.get(url)
    
    # Save the content of the ZIP file locally
    with open(output_dir + local_file_path, "wb") as file:
        file.write(response.content)
        
    # Extract the contents of the zip file into the output folder
    if extract_content:
        with zipfile.ZipFile(output_dir + local_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

# Define the URL of the postcode shape file ZIP
postcode_url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/POA_2021_AUST_GDA2020_SHP.zip"

# download the zip folder with postcode shape file
download_zip_file(postcode_url, output_dir_postcode, local_file_path_zip_postcode)