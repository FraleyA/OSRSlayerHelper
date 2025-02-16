import sqlite3
import requests
from bs4 import BeautifulSoup
from monster_links import monster_links
from scrape_table import monster_info

# Define pathway to SQL database.
db_path = 'C:/Users/Austin/PycharmProjects/OSRSlayerHelper/.venv/data/'

# Initialize a database to store relevant info.
connection = sqlite3.connect(db_path + 'KuradalTasks.db')

# Scrape links to monster wiki tables off of the desired slayer master's wiki.
monster_links = monster_links()

# Iterate through the links to extract monster data.
for link in monster_links:
    print(f'Current url: {link}...')

    monster_data = monster_info(link)
    print(monster_data, '\n')