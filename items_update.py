import requests
import sqlite3
from link_maker import create_link
from ids import id_list
import urllib

db_path='csgo_market.db'
data = requests.get("https://market.csgo.com/api/v2/prices/RUB.json").json()
items = data.get('items', [])

def format_name_for_steam(name):
    formatted_name = urllib.parse.quote(name, safe='')
    formatted_name = formatted_name.replace(' ', '%20').replace('&', '%26').replace("'", '%27').replace('|','%7C').replace('(', '%28').replace(')', '%29')
    return formatted_name


def fetch_and_process(item, cursor):
    name = item['market_hash_name']
    market_price=0
    market_total = 0
    steam_listing = format_name_for_steam(name)
    id = id_list.get(name, None)
    if id:
        steam_url = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}'
        steam_autobuy = 0
        steam_autobuy_total = 0
        profit_ratio = 0
        market_link = create_link(name, steam_listing)
        steam_link = 'https://steamcommunity.com/market/listings/730/' + steam_listing
        cursor.execute('''
        INSERT INTO items (id, name, market_link, steam_link, market_price, steam_autobuy, market_total, steam_autobuy_total, profit_ratio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, name, market_link, steam_link, market_price, steam_autobuy, market_total, steam_autobuy_total, profit_ratio))


conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id TEXT UNIQUE,
        name TEXT,
        market_link TEXT,
        steam_link TEXT,
        market_price REAL,
        steam_autobuy REAL,
        market_total REAL,
        steam_autobuy_total REAL,
        profit_ratio REAL
    )
''')
conn.commit()

for item in items:
    if 500 < float(item['price']) < 10000:
        fetch_and_process(item, cursor)
conn.commit()

conn.close()