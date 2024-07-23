import requests
from bs4 import BeautifulSoup
import re
import urllib
from ids import id_list

def format_name_for_steam(name):
    formatted_name = urllib.parse.quote(name, safe='')
    formatted_name = formatted_name.replace(' ', '%20').replace('&', '%26').replace("'", '%27').replace('|', '%7C').replace('(', '%28').replace(')', '%29')
    return formatted_name


response = requests.get("https://market.csgo.com/api/v2/prices/RUB.json")

data = response.json()
items = data.get('items', [])

for item in items:
    name = item.get('market_hash_name', '')
    price = round(float(item.get('price', 0)) * 1.075, 2)
    if price > 100 and price < 50000:
        steam_listing = format_name_for_steam(name)
        if name in id_list:
            continue
        else:
            steam_url = 'https://steamcommunity.com/market/listings/730/' + steam_listing
            html = requests.get(steam_url).text
            soup = BeautifulSoup(html, 'lxml')
            id = None
            for script in soup.find_all('script'):
                id_regex = re.search(r'Market_LoadOrderSpread\(([ 0-9]+)\)', script.text)
                if id_regex:
                    id = id_regex.groups()[0].strip()
                    break
            print(f'"{name}": {id},')