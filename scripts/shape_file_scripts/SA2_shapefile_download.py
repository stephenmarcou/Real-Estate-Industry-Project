from urllib.request import urlretrieve
import os
import requests
import zipfile
import shutil

local_file_path_zip_sa2 = "SA2_files.zip"
local_file_path_zip_sa2_postcode = "SA2_postcode_files.zip"
output_dir_sa2 = "data/landing/sa2/"
output_dir_sa2_postcode = "data/landing/intermediate_sa2_postcode/"
folders = [output_dir_sa2, output_dir_sa2_postcode]
# create folder if they do not exist
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)



def download_zip_file(url, output_dir, local_file_path, extract_content = True):
    """ Function downloads zip file from url and opens the zip and saves the content """
    response = requests.get(url)
    with open(output_dir + local_file_path, "wb") as file:
        file.write(response.content)
    # Extract the contents of the zip file into the output folder
    if extract_content:
        with zipfile.ZipFile(output_dir + local_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

# download the zip folder with sa2 shape file        
sa2_url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip"
download_zip_file(sa2_url, output_dir_sa2, local_file_path_zip_sa2)

# download the zip folder with sa2 to postcode dataset
sa2_postcode_url = "https://data.gov.au/data/dataset/2c79581f-600e-4560-80a8-98adb1922dfc/resource/33d822ba-138e-47ae-a15f-460279c3acc3/download/asgs2021_correspondences.zip"
download_zip_file(sa2_postcode_url, output_dir_sa2_postcode, local_file_path_zip_sa2_postcode, extract_content = False)

def extract_file_from_zip(extract_zip_file_path, extract_file, output_dir):
    """ 
    Function locates a file (extract_file) from a zip file (extract_zip_file_path) and saves it to location specified by
    output_dir
    """
        # Open the downloaded zip file for reading
    with zipfile.ZipFile(extract_zip_file_path, 'r') as zip_ref:
        # Extract the specific file to the desired location
        zip_ref.extract(extract_file, path=output_dir)
        
postcode_sa2_file = "CG_POSTCODE_2021_SA2_2021.xlsx"
extract_zip_file_path = output_dir_sa2_postcode + local_file_path_zip_sa2_postcode
extract_file_from_zip(extract_zip_file_path, postcode_sa2_file, output_dir_sa2)

# remove intermediate_sa2_postcode folder
shutil.rmtree(output_dir_sa2_postcode)

print("done")

