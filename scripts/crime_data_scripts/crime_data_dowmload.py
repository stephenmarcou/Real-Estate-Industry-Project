
# https://www.crimestatistics.vic.gov.au/crime-statistics/latest-victorian-crime-data/download-data
#this has suburb data, whoch could be good

# https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Ffiles.crimestatistics.vic.gov.au%2F2023-07%2FData_Tables_Property_Items_Visualisation_Year_Ending_March_2023.xlsx&wdOrigin=BROWSELINK
# this has suburb data



import os
import requests

# URL of the Excel file
url = "https://files.crimestatistics.vic.gov.au/2023-07/Data_Tables_Property_Items_Visualisation_Year_Ending_March_2023.xlsx"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Get the content of the response (the file's binary data)
    file_content = response.content

    # Specify the local file path where you want to save the downloaded file
    local_file_path = os.path.join("data", "landing", "Data_Tables_Property_Items_Visualisation_Year_Ending_March_2023.xlsx")

    # Create the directories if they don't exist
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    # Write the binary data to the local file
    with open(local_file_path, "wb") as file:
        file.write(file_content)

    print(f"File downloaded and saved as '{local_file_path}'")
else:
    print(f"Failed to download the file. HTTP status code: {response.status_code}")

