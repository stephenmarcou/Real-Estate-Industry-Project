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
BASE_URL = "https://dbr.abs.gov.au/region.html?lyr=sa2&rgn=206041506"

# Create a session with a User-Agent
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})   #Windows 10-based PC using Edge browser from https://deviceatlas.com/blog/list-of-user-agent-strings

response = session.get(BASE_URL) 
bs_object = BeautifulSoup(response.text, "lxml")

key_stats = bs_object.find_all('div', id = 'INC')

#main_table = key_stats.find('table', class_ = 'biscuitTable')

print(bs_object.find_all('h2'))