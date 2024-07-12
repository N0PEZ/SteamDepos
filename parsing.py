import requests
import sqlite3
import urllib.parse
import link_maker
from steam_parse import get_autobuy
from time import sleep


def format_name_for_steam(name):
    formatted_name = urllib.parse.quote(name, safe='')
    formatted_name = formatted_name.replace(' ', '%20').replace('&', '%26').replace("'", '%27').replace('|', '%7C').replace('(', '%28').replace(')', '%29')
    return formatted_name


def cs_market_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])

        conn = sqlite3.connect('csgo_market.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                name TEXT,
                link TEXT,
                market_total REAL,
                steam_autobuy_total REAL,
                profit_ratio REAL
            )
        ''')
        conn.commit()


        for item in items:
            name = item.get('market_hash_name', '')
            price = round(float(item.get('price', 0)) * 1.075,2)
            if price > 8000 and price < 8500:
                steam_listing = format_name_for_steam(name)
                steam_autobuy = get_autobuy(steam_listing)
                print(steam_autobuy)
                #sleep(10)
                steam_autobuy_total = round(steam_autobuy*0.87,2)
                profit_ratio = round(steam_autobuy_total/price,3)
                link=link_maker.create_link(name,steam_listing)
                cursor.execute('''
                    INSERT OR REPLACE INTO items (name, link, market_total, steam_autobuy_total, profit_ratio)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, link, price, steam_autobuy_total, profit_ratio))


        conn.commit()
        conn.close()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

cs_market_url = "https://market.csgo.com/api/v2/prices/RUB.json"
cs_market_api(cs_market_url)