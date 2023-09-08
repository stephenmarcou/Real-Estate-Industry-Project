from urllib.request import urlretrieve
import os
import zipfile

def download_zones():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')
    output_dir = os.getcwd() + '/data/landing/local_zone/'

    # check if it exists as it makedir will raise an error if it does exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # download (code is adapted from the tutorials)
    urlretrieve('https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/LGA_2023_AUST_GDA2020.zip',  
                f'{output_dir}/local_zones.zip')

def unzip_folder():
    output_dir = './data/raw/local_zone/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    zip_file_path = f'./data/landing/local_zone/local_zones.zip'

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract all the contents to the specified directory
        zip_ref.extractall(output_dir)
        
unzip_folder()