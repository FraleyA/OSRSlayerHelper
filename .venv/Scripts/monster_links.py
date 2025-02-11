import sqlite3
import requests
from bs4 import BeautifulSoup

def monster_links(base_url='https://oldschool.runescape.wiki', slayer_master='Kuradal', display_links=False):
    """ Grab all slayer monster links from a given slayer master's wiki page.
        slayer_master (string): Turael/Aya, Spria, Mazchna/Achtryn, Vannaka, Chaeldar, Konar, Nieve/Steve, Duradel/Kuradal.
        display_links (bool): Optionally display the links to all monsters on a wiki page.
    """

    # Define slayer master's url.
    master_url = base_url + '/w/' + slayer_master

    # This Url is crucial to properly cross-check the monster links from Duradel's wiki page.
    category_url = base_url + '/w/Category:Slayer_monsters'

    # Add header to access OSRS wiki, so that I don't get 403'd.
    header = {'User-Agent': 'Mozilla/5.0'}

    # Create a list of monster name to cross-reference with Duradel's possible assignments.
    monster_names = []
    while category_url:

        # Use requests to access the OSRS wiki.
        r = requests.get(category_url, headers=header)

        # Check if the request was successful.
        if r.status_code != 200:
            raise RuntimeError(f'Request failed with error code {r.status_code}')

        # Use beautiful soup to parse the html source code.
        soup = BeautifulSoup(r.text, 'html.parser')

        # Target id=mw-pages hyperlinks starting with "/w/".
        links = soup.select('#mw-pages a[href^="/w/"]')

        # Add monster name data to monster_names array.
        for name in links:
            href = name['href']
            monster_name = name.text.lower().strip()

            # Filter monster names using links.
            if not (href.startswith('/w/Category:') or href.startswith('/w/User:') or href.startswith('/w/Slayer_monsters')):
                monster_names.append(monster_name)

        # Update the category_url to find monsters from the next page.
        next_page = soup.find('a', string='next page')
        category_url = base_url + next_page['href'] if next_page else None

    #print(monster_names)

    ### --- Now find all monster links associated with Duradel assignments by cross-checking links with monster_names. --- ###

    # Use requests to access slayer master's wiki page.
    r = requests.get(master_url, headers=header)

    # Check that the request was successful.
    if r.status_code != 200:
        raise RuntimeError(f'Request failed with error code {r.status_code}')

    # Parse the assignment table data from the html source code.
    soup = BeautifulSoup(r.text, 'html.parser')

    # Locate the slayer assignment table on the wiki.
    assignment_table = soup.find('table', attrs={'class': 'wikitable sortable lighttable qc-active'})

    # Create a list of monster links for data retrieval.
    monster_links = []
    for link in assignment_table.find_all('a', attrs={'href': True}):
        name = link.text.lower().strip()

        # startswith() catches plural names on the wiki page, i.e. "abyssal demons" instead of "abyssal demon".
        if any(name.startswith(i) for i in monster_names):
            monster_link = link['href']
            monster_links.append(base_url + monster_link)

    if display_links:
        for link in monster_links:
            print(link)

    # Did we succeed?!
    print(f'Successfully scraped {len(monster_links)} links to monsters assigned by {slayer_master}.')

    return monster_links