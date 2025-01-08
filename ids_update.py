import requests
from bs4 import BeautifulSoup
import re
from ids import id_list
from link_maker import format_name_for_steam

response = requests.get("https://market.csgo.com/api/v2/prices/RUB.json")

data = response.json()
items = data.get('items', [])

for item in items:
    name = item.get('market_hash_name', '')
    price = round(float(item.get('price', 0)) * 1.075, 2)
    if price > 500 and price < 10000:
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