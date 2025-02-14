import sqlite3
import requests
from bs4 import BeautifulSoup
import re

# Use requests to access the OSRS wiki.
base_url = 'https://oldschool.runescape.wiki'

# Use header, so the wiki page does not block me. I'm not a bot Jagex, I swear!
monster_name = 'Adamant_dragon'
r = requests.get(base_url + '/w/' + monster_name, headers={'User-Agent': 'Mozilla/5.0'})

# Check if the request successfully connected.
if r.status_code != 200:
    raise RuntimeError(f'Request failed with status code {r.status_code}')

# Parse the OSRS wiki's html source code.
soup = BeautifulSoup(r.text, 'html.parser')

# Need to find the table class to scrape.
# table_class1 = 'infobox infobox-switch no-parenthesis-style infobox-monster' # abyssal demon
# table_class2 = 'infobox no-parenthesis-style infobox-monster' # adamant dragon

info_table = soup.find('table', class_=re.compile('monster'))

# Ah yes, the bane of my existence.
#info_table = soup.find('table', attrs={'class': table_class1})

# header will store the monster's name data, i.e. 'adamant dragon'.
header = info_table.find('th', attrs={'class': 'infobox-header'})
if header:
    # Define nested dictionary structure based on the wiki table headers.
    monster_name = header.get_text(strip=True).upper()
    stat_categories = {
        monster_name: {},
        'COMBAT INFO': {},
        'SLAYER INFO': {},
        'COMBAT STATS': {},
        'AGGRESSIVE STATS': {},
        'MELEE DEFENCE': {},
        'MAGIC DEFENCE': {},
        'RANGED DEFENCE': {},
        'IMMUNITIES': {},
        'ADVANCED DATA': {}
    }
else:
    print('Warning: Monster name not found.')

# Iterate through table rows to extract information while tracking the current header.
table_rows = info_table.find_all('tr')
current_header = monster_name
print(f'Starting header: {current_header}\n')

for row in table_rows:
    print(row.prettify(), '\n')

    ### INSERT code here to extract header data for released, members, combat level, etc. ###

    # subheader will store consecutive monster info categories, i.e. 'combat info', 'slayer info', and so on.
    subheader = row.find('th', class_='infobox-subheader')

    # If we encounter a new subheader, i.e. 'combat info', update current_header.
    if subheader:
        current_header = subheader.get_text(strip=True).upper()
        print(f'Current subheader is {current_header}...\n')

    # Deal with each field accordingly.
    for header in stat_categories:
        if header == current_header:
            attribute = row.find('th')
            data = row.find('td')
            if attribute:
                attribute_text = attribute.get_text(strip=True).lower()
                print(attribute_text)
            if data:
                data_text = data.get_text(strip=True).lower()
                print(data_text)

            if attribute and data:
                attribute_text = attribute.get_text(strip=True).lower()
                # Extract text while preserving spaces for newlines
                data_text = data.get_text('\n', strip=True).lower().replace('\n', ' ')

                # Filter out empty strings, i.e. 'assigned by': ''.
                if data_text:
                    stat_categories[current_header][attribute_text] = data_text

    combat_skills = row.find_all('a', attrs={'title': True})
    combat_stats = row.find_all('td', attrs={'class': 'infobox-nested'})

    if combat_skills:
        combat_skills_text = [skill['title'].strip().lower() for skill in combat_skills]
        print(combat_skills_text)
    if combat_stats:
        combat_stats_text = [stat.get_text(strip=True).lower() for stat in combat_stats]
        for i in range(len(combat_skills_text)):
            stat_categories[current_header][combat_skills_text[i]] = combat_stats_text[i]

for category in stat_categories:
    print(category)
    print(stat_categories[category], '\n')
