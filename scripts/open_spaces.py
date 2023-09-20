from urllib.request import urlretrieve
import os
import zipfile

def download_zones():
    output_dir = 'data/landing/open_space/'

    # check if it exists as it makedir will raise an error if it does exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # download (code is adapted from the tutorials)
    urlretrieve('https://opendata.arcgis.com/datasets/da1c06e3ab6948fcb56de4bb3c722449_0.zip',  
                f'{output_dir}/open_space.zip')

download_zones()


def unzip_folder():
    output_dir = 'data/raw/open_space/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    zip_file_path = f'data/landing/open_space/open_space.zip'

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract all the contents to the specified directory
        zip_ref.extractall(output_dir)
        
unzip_folder()