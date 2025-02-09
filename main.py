import aiohttp
import asyncio
import requests
from ids import id_list
import json
from link_maker import create_link, format_name_for_steam, ban_words

depos = []
withdraw = []

async def steam_api(session, name, market_price, market_autobuy):
    id = id_list.get(name, None)
    if id:
        steam_url = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}'
        try:
            async with session.get(steam_url) as response:
                if response.status == 200:
                    steam_data = await response.json()
                    steam_listing = format_name_for_steam(name)
                    market_link = create_link(name, steam_listing)
                    steam_link = 'https://steamcommunity.com/market/listings/730/' + steam_listing
                    steam_price = steam_data['sell_order_graph'][0][0]
                    steam_autobuy = steam_data['buy_order_graph'][0][0]
                    profit_ratio = round(steam_autobuy / market_price, 3)
                    withdrawal_profit = round(market_autobuy / steam_price, 3)
                    if profit_ratio>=0.9:
                        depos.append({'id':id, 'name':name, 'market_link':market_link, 'steam_link':steam_link, 'market_price':market_price, 'market_autobuy':market_autobuy, 'steam_price':steam_price, 'steam_autobuy':steam_autobuy, 'profit_ratio':profit_ratio, 'withdrawal_profit':withdrawal_profit})
                    elif withdrawal_profit>0.8:
                        withdraw.append({'id':id, 'name':name, 'market_link':market_link, 'steam_link':steam_link, 'market_price':market_price, 'market_autobuy':market_autobuy, 'steam_price':steam_price, 'steam_autobuy':steam_autobuy, 'profit_ratio':profit_ratio, 'withdrawal_profit':withdrawal_profit})
                else:
                    print(
                        f"Response status {response.status} for {name}: {steam_url}")
        except Exception as e:
            print(f"Exception occurred while fetching {steam_url}: {e}")

async def process_items(items, autobuys):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for item in items:
            name = item['market_hash_name']
            market_price=float(item['price'])
           
            if 500 < float(item['price']) < 10000 and not any(banword in item['market_hash_name'] for banword in ban_words):
                try:
                    market_autobuy = autobuys[name]
                except:
                    market_autobuy = 1
                tasks.append(steam_api(session, name, market_price, market_autobuy))
        await asyncio.gather(*tasks)

        deposit=sorted(depos, key=lambda d: d['profit_ratio'], reverse=True)
        withdrawal=sorted(withdraw, key=lambda d: d['withdrawal_profit'], reverse=True)
        with open('/var/www/steamdepos/api/depos.json', 'w') as file:
            json.dump(deposit, file)
        with open('/var/www/steamdepos/api/withdraw.json', 'w') as file:
            json.dump(withdrawal, file)


async def cs_market_api():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://market.csgo.com/api/v2/prices/RUB.json") as response:
            data = await response.json()
            items = data.get('items', [])
            orders_api = requests.get("https://market.csgo.com/api/v2/prices/orders/RUB.json").json()
            autobuys = {item['market_hash_name']: item['price'] for item in orders_api.get('items', [])}
            await process_items(items, autobuys)

asyncio.run(cs_market_api())