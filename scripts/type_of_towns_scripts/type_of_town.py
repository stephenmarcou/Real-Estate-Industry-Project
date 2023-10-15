from bs4 import BeautifulSoup
from urllib.request import urlretrieve, urlopen
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import json
import os


def all_town_lat_long_data():
    """
    This function fetches latitude and longitude data for a list of towns and saves it to CSV files.
    It processes town names, sends API requests to obtain location data.
    """
    
    all_towns = get_all_towns()
    folder_path = 'data/landing/all_towns_lat_long'
    i = len([name for name in os.listdir(folder_path) if os.path.isfile(folder_path + '/' + name)]) - 1 # It has DS.STORE in, as well

    # Loop through the list of towns
    while i < len(all_towns):

        # Request and get the data for said town
        town = all_towns[i]
        url = f"http://api.geonames.org/postalCodeSearch?country=AU&maxRows=500&placename={convert_to_geonames_format(town)}&postalcode_startsWith=3&username=seamus"
        response = urlopen(url)
        tree = ET.parse(response)
        root = tree.getroot()  
        
        # Create empty lists to store data
        postalcode_list = []
        name_list = []
        lat_list = []
        lng_list = []

        # Iterate over <code> elements and extract data
        for code in root.findall('code'):
            postalcode = code.find('postalcode').text
            name = code.find('name').text
            lat = code.find('lat').text
            lng = code.find('lng').text

            postalcode_list.append(postalcode)
            name_list.append(name)
            lat_list.append(lat)
            lng_list.append(lng)

        # Create a Pandas DataFrame
        data = {
            'postalcode': postalcode_list,
            'name': name_list,
            'lat': lat_list,
            'lng': lng_list,
        }

        # Save the current town data to a folder to be processed more later
        df = pd.DataFrame(data)
        df.to_csv(f'data/landing/all_towns_lat_long/{town}.csv')

        i += 1

def get_all_towns():
    """Returns DataFrame of all towns in VIC"""
    places = "https://www.victorianplaces.com.au/places"
    response = requests.get(places)
    soup = BeautifulSoup(response.text, 'html.parser')
    txt = soup.text.split("\n\n")
    txt = [t for t in txt if t]
    txt = txt[6:-7]
    txt[0] = 'Abbotsford'
    
    for i in range(len(txt)):
        if txt[i][-1] == ' ':
            txt[i] = txt[i][:-1]

    return txt

def convert_to_geonames_format(town: str):
    """Returns the given town in the format needed"""
    return town.lower().replace(' ', '-').replace(u"\u2018", "'").replace(u"\u2019", "'")
    
def rural_melb_town_data():
    """
    Function that downloads rural town data.
    """

    # Grab all the data from the url 
    RURAL_TOWNS_MELB_GPX_FILE = "https://geoexport.toolforge.org/gpx?coprimary=all&titles=Category:Towns_in_Victoria_(state)"
    filename = "data/landing/town_data.gpx"
    urlretrieve(RURAL_TOWNS_MELB_GPX_FILE, filename)

    tree = ET.parse(filename)
    root = tree.getroot()

    # Find each waypoint and add to a list
    waypoints = []
    for wpt in root.findall(".//{http://www.topografix.com/GPX/1/1}wpt"):
        lat = float(wpt.get("lat"))
        lon = float(wpt.get("lon"))
        name = wpt.find(".//{http://www.topografix.com/GPX/1/1}name").text
        description = wpt.find(".//{http://www.topografix.com/GPX/1/1}desc").text
        waypoints.append({"Name": name, "Description": description, "Latitude": lat, "Longitude": lon})

    df = pd.DataFrame(waypoints)

    # Data is then saved to a dataframe
    df.to_csv("data/raw/melb_town_data.csv")
    
def get_city_centre_data():
    """
    Function that finds all the city centres in Victoria, as specified by Wikipedia
    """

    CITY_CENTRES_URL = "https://en.wikipedia.org/wiki/Category:Cities_in_Victoria_(state)"
    response = requests.get(CITY_CENTRES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # On hand cleaning, since the data structure of wikipedia is not the best.
    s = [q for q in soup.text.split('\n') if q]
    s = s[77:92]
    s[2] = s[2][:-1]
    s[3] = s[3][:-11]
    s[4] = s[4][:-1]
    s[5] = s[5][:-11]
    s[7] = s[7][:-1]
    s[8] = s[8][:-10]
    s[10] = s[10][:-1]
    s[11] = s[11][:-1]

    # Save data to a csv
    pd.DataFrame(s).to_csv('data/landing/city_centres.csv')

def get_coastal_town_data():
    """
    Function that finds all the coastal towns in Victoria, as specified by Wikipedia
    """

    COASTAL_TOWNS_URL = "https://en.wikipedia.org/wiki/Category:Coastal_towns_in_Victoria_(state)"

    response = requests.get(COASTAL_TOWNS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    li_elements = soup.find_all('li')

    currently_a_town = False
    town_list = []

    # Iterate over all list elements and save the coastal town names
    for li in li_elements:
        if currently_a_town:
            town_list.append(li.text)
            if li.text == 'Yanakie, Victoria':
                break
        else:
            if li.text == 'Agnes, Victoria':
                currently_a_town = True

    # Remove Victoria tag from end of towns if it is there
    town_list = [town.split(', Victoria')[0] for town in town_list]
    
    # Return as a csv
    pd.DataFrame(town_list, columns=['coastal_town']).to_csv('../data/raw/coastal_towns.csv', index=None)                

if __name__ == "__main__":
    all_town_lat_long_data() 
    get_all_towns()
    rural_melb_town_data()
    get_city_centre_data()
    get_coastal_town_data()
