# from urllib.request import urlretrieve
# import os

# URL = 'https://www.matthewproctor.com/Content/postcodes/australian_postcodes.csv'

# output_dir = "data/landing/sa2"
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
    
# urlretrieve(URL, f'{output_dir}/postcodes.csv')

import requests
import os

URL = 'https://www.matthewproctor.com/Content/postcodes/australian_postcodes.csv'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

output_dir = "data/landing/sa2"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

response = requests.get(URL, headers=headers)

# Check if the HTTP response status code is 200 (OK). If yes, it means the content was successfully retrieved.
if response.status_code == 200:
    with open(f'{output_dir}/postcodes.csv', 'wb') as file:
        file.write(response.content)
else:
    print(f"Failed to download file. Status code: {response.status_code}")
