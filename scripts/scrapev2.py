"""
A very simple, naive, and basic web scraping script. This will not
work completely and is only applicable to domain.com.

"""
# built-in imports
import re
import requests  # Import the requests library
import json
import csv

from collections import defaultdict

# user packages
from bs4 import BeautifulSoup

import os
import pandas as pd

# constants
BASE_URL = "https://www.domain.com.au"

# Create a session with a User-Agent
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})   #Windows 10-based PC using Edge browser from https://deviceatlas.com/blog/list-of-user-agent-strings


# begin code
url_links = []
property_metadata = defaultdict(dict)

'''
# Accessing all the Victorian Postcodes
post_codes_file_path = "data/landing/sa2/CG_POSTCODE_2021_SA2_2021.xlsx"
df = pd.read_excel(post_codes_file_path)

all_postcodes = df['POSTCODE'].values
all_postcodes = set(all_postcodes)

victorian_postcodes = [str(int(x)) for x in all_postcodes if str(x).startswith('3')]
print(victorian_postcodes)

# generating a list of urls to vist from all the victorian postcodes
for postcode in victorian_postcodes:
    page = 0

    # generate list of urls to visit
    while True:
        page += 1
        if page%10 == 0:
            print('page', page)

        url = BASE_URL + f"/rent/?postcode={postcode}&excludedeposittaken=1&ssubs=0&sort=price-desc&page={page}"
        print(f"Visiting {url}")
        response = session.get(url) 
        bs_object = BeautifulSoup(response.text, "lxml")

        # find the unordered list (ul) elements which are the results, then
        # find all href (a) tags that are from the base_url website.
        try:
            index_links = bs_object \
                .find(
                    "ul",
                    {"data-testid": "results"}
                ) \
                .findAll(
                    "a",
                    href=re.compile(f"{BASE_URL}/*")
                )
            
        # Handle the AttributeError if needed (e.g., print an error message)
        except AttributeError:
            print("AttributeError: 'NoneType' object has no attribute 'findAll'")
            break 


        for link in index_links:
            # if it's a property address, add it to the list
            if 'address' in link['class']:
                url_links.append(link['href'])

#saving the list of urls
with open('data/landing/property_urls.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
     
    # Write each string as a separate row in the CSV file
    for item in url_links:
        csv_writer.writerow([item])

'''
df = pd.read_csv('data/landing/property_urls.csv')
url_links = [url[0] for url in df.values]

# for each url, scrape some metadata
for up_to, property_url in enumerate(url_links[1:], start=1):
    response = session.get(property_url)  
    bs_object = BeautifulSoup(response.text, "lxml")

    print(property_url)
    try:
        # looks for the header class to get property name
        property_metadata[property_url]['name'] = bs_object \
            .find("h1", {"class": "css-164r41r"}) \
            .text

        # looks for the div containing a summary title for cost
        property_metadata[property_url]['cost_text'] = bs_object \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text

        # extract coordinates from the hyperlink provided
        property_metadata[property_url]['coordinates'] = [
            float(coord) for coord in re.findall(
                r'destination=([-\s,\d\.]+)',
                bs_object \
                    .find(
                        "a",
                        {"target": "_blank", 'rel': "noopener noreferrer"}  
                    ) \
                    .attrs['href']
            )[0].split(',')
        ]

        #property type
        property_type = bs_object \
        .find('div', {'data-testid': 'listing-summary-property-type', 'class': 'css-dvvls9'}) \
            .find('span', class_='css-in3yi3') \
            .text
        
        property_metadata[property_url]['property type'] = property_type

        #if carspace delete the entry and keep going
        if property_type == 'Carspace': 
            del property_metadata[property_url]
            continue

        # get rooms and parking
        rooms = bs_object \
            .find("div", {"data-testid": "property-features"}) \
            .findAll("span", {"data-testid": "property-features-text-container"})

        # Beds
        beds = [
            re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Bed' in feature.text
        ]
        if len(beds) == 0:
            del property_metadata[property_url]
            continue
        else:
            property_metadata[property_url]['beds'] = beds[0]


        # Baths
        baths = [
            re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Bath' in feature.text
        ]
        if len(baths) == 0:
            del property_metadata[property_url]
            continue
        else:
            property_metadata[property_url]['baths'] = baths[0]



        # parking
        parking = [
            re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Parking' in feature.text
        ]
        if len(parking) == 0:
            property_metadata[property_url]['parking'] = 0
        else:
            property_metadata[property_url]['parking'] = parking[0]


        
        #property Description heading
        property_metadata[property_url]['title'] = bs_object \
            .find('h4', {'data-testid': 'listing-details__description-headline', 'class': 'css-juce83'}) \
            .text
        
        #description 
        headline = bs_object.find('h4', {'data-testid': 'listing-details__description-headline', 'class': 'css-juce83'})
        property_metadata[property_url]['description'] = [
            sibling_p.text for sibling_p in headline.find_next_siblings('p')
        ]

        # Property Features
        features_listing = bs_object.findAll('li', {'data-testid': 'listing-details__additional-features-listing', 'class': 'css-vajaaq'})
        features_suggested = bs_object.findAll('li', {'data-testid': 'listing-details__additional-features-suggested', 'class': 'css-vajaaq'})
        property_metadata[property_url]['property features'] = [feature.text for feature in features_listing + features_suggested]


        # NBN
        nbn_description_element = bs_object.find("p", {"data-testid": "nbn-connection_description"})
        #Checking if they have nbn or not
        if nbn_description_element:
            # If the element exists, extract the text content
            nbn_description = nbn_description_element.text
        else:
            # If the element doesn't exist, populate 'No NBN'
            nbn_description = 'No NBN'

        # Assign the value to the property_metadata dictionary
        property_metadata[property_url]['NBN'] = nbn_description
        
    except AttributeError:
        #print(f"Issue with {property_url}, see raw dump below")
        #print(bs_object.text)
        continue

    if up_to%1000 == 0:
        formatted_json = json.dumps(property_metadata, indent=4)

        # output to example json in data/landing/
        with open(f'data/landing/rentals_victoria_entry_{up_to-999}-{up_to}.json', 'w') as f:
            f.write(formatted_json)
            property_metadata = defaultdict(dict)

    
formatted_json = json.dumps(property_metadata, indent=4)

# output to example json in data/landing/
with open(f'data/landing/rentals_victoria_entry_12001-{up_to}.json', 'w') as f:
    f.write(formatted_json)

