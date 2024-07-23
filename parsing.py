import aiohttp
import asyncio
import sqlite3
import urllib.parse
from ids import id_list
from link_maker import create_link


def format_name_for_steam(name):
    formatted_name = urllib.parse.quote(name, safe='')
    formatted_name = formatted_name.replace(' ', '%20').replace('&', '%26').replace("'", '%27').replace('|','%7C').replace('(', '%28').replace(')', '%29')
    return formatted_name


async def fetch_and_process(session, item, cursor):
    name = item.get('market_hash_name', '')
    price = round(float(item.get('price', 0)) * 1.075, 2)
    steam_listing = format_name_for_steam(name)
    id = id_list.get(name, None)
    if id:
        steam_url = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}'
        try:
            async with session.get(steam_url) as response:
                if response.status == 200:
                    steam_data = await response.json()
                    try:
                        steam_autobuy = steam_data['buy_order_graph'][0][0]
                        steam_autobuy_total = round(steam_autobuy * 0.87, 2)
                        profit_ratio = round(steam_autobuy_total / price, 3)
                        if profit_ratio >=0.9:
                            market_link = create_link(name, steam_listing)
                            steam_link = 'https://steamcommunity.com/market/listings/730/' + steam_listing
                            cursor.execute('''
                                INSERT OR REPLACE INTO items (name, market_link, steam_link, market_total, steam_autobuy_total, profit_ratio)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (name, market_link, steam_link, price, steam_autobuy_total, profit_ratio))
                            con.commit()
                    except KeyError as e:
                        print(f"Key error: {e} for item: {item}")
                else:
                    print(
                        f"Unexpected response {response.status} with content type: {response.headers.get('Content-Type')} for URL: {steam_url}")
        except Exception as e:
            print(f"Exception occurred while fetching {steam_url}: {e}")


async def process_items(items):
    conn = sqlite3.connect('csgo_market.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            name TEXT,
            market_link TEXT,
            steam_link TEXT,
            market_total REAL,
            steam_autobuy_total REAL,
            profit_ratio REAL
        )
    ''')
    conn.commit()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in items:
            if 500 < float(item['price']) < 10000:
                tasks.append(fetch_and_process(session, item, cursor))
        await asyncio.gather(*tasks)
        conn.commit()

    conn.close()


async def cs_market_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                items = data.get('items', [])
                await process_items(items)
            else:
                print(f"Failed to fetch data. Status code: {response.status}")


cs_market_url = "https://market.csgo.com/api/v2/prices/RUB.json"
asyncio.run(cs_market_api(cs_market_url))