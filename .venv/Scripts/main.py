import sqlite3
import requests
from bs4 import BeautifulSoup

# Define pathway to SQL database.
db_path = 'C:/Users/Austin/PycharmProjects/OSRSlayerHelper/.venv/data/'

# Initialize a database to store relevant info.
connection = sqlite3.connect(db_path + 'KuradalTasks.db')

# Add header to access OSRS wiki, so that I don't get 403'd.
header = {'User-Agent': 'Mozilla/5.0'}

# Use requests to access the OSRS wiki.
r = requests.get('https://oldschool.runescape.wiki/w/Abyssal_demon', headers=header)

# Check if the request successfully connected.
if r.status_code != 200:
    raise RuntimeError(f'Request failed with status code {r.status_code}')

# Parse the OSRS wiki's html source code.
soup = BeautifulSoup(r.text, 'html.parser')

# Monster name uses 'th' tag in the html wiki page. All monster traits are described as 'data-attr-param'.
name = soup.find('th', attrs={'data-attr-param': 'name'})

# Make sure the name is found with tag 'th'.
monster_stats = {}
if name:
    monster_stats['name'] = name.text.strip()
else:
    print('Warning: Slayer monster name not found.')

# Store monster attribute parameters in a dictionary (wiki html uses 'td' tag for other stats).
for tag in soup.find_all('td', attrs={'data-attr-param': True}):
    key = tag.get('data-attr-param')
    value = tag.text.strip()

    # Check if there is an actual value, not just an empty string; i.e. not an image.
    # No need for 'dpscalc' either, just tells you to open a dps calculator.
    if value and key != 'dpscalc':
        monster_stats[key] = value

print(monster_stats)


### --- Now I need to resolve an issue with scraping certain OSRS wiki pages. --- ###

# The issue seems to stem from data being stored in a table as opposed to the tag 'data-attr-param'.
