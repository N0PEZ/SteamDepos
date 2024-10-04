import aiohttp
import asyncio
import sqlite3
import urllib.parse
from ids import id_list


proxies=[
'http://ace6a6db:befa43266e@37.221.83.23:30013',
'http://WLk96X:Vd0CaAy4ZU@188.130.129.23:1050'
]

def format_name_for_steam(name):
    formatted_name = urllib.parse.quote(name, safe='')
    formatted_name = formatted_name.replace(' ', '%20').replace('&', '%26').replace("'", '%27').replace('|','%7C').replace('(', '%28').replace(')', '%29')
    return formatted_name


async def fetch_and_process(session, item, cursor):
    name = item['market_hash_name']
    market_price=item['price']
    market_total = round(float(market_price) * 1.075, 2)
    id = id_list.get(name, None)
    if id:
        steam_url = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}'
        try:
            async with session.get(steam_url, proxy='http://ace6a6db:befa43266e@37.221.83.23:30013') as response:
                if response.status == 200:
                    steam_data = await response.json()
                    try:
                        steam_autobuy = steam_data['buy_order_graph'][0][0]
                        steam_autobuy_total = round(steam_autobuy * 0.87, 2)
                        profit_ratio = round(steam_autobuy_total / market_total, 3)
                        if profit_ratio:
                            cursor.execute('''
                                UPDATE items 
                                SET market_price=?, steam_autobuy=?, market_total=?, steam_autobuy_total=?, profit_ratio=?
                                WHERE id = ''' + str(id) + '''
                            ''', (market_price, steam_autobuy, market_total, steam_autobuy_total, profit_ratio))
                    except KeyError as e:
                        print(f"Key error: {e} for item: {item}")
                else:
                    print(
                        f"Unexpected response {response.status} with content type: {response.headers.get('Content-Type')} for {name}: {steam_url}")
        except Exception as e:
            print(f"Exception occurred while fetching {steam_url}: {e}")


async def process_items(items):
    db_path='csgo_market.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    async with aiohttp.ClientSession() as session:
        tasks = []
        # count=0
        # overall=0
        for item in items:
            if 500 < float(item['price']) < 10000:
                # overall+=1
                # print(overall)
                # count+=1
                tasks.append(fetch_and_process(session, item, cursor))
                # if count==10:
                #     count=0
                    # await asyncio.gather(*tasks)
                    # tasks=[]
                    # conn.commit()
                    # await asyncio.sleep(0.01)


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