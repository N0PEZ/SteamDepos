import re
import requests
from bs4 import BeautifulSoup

def get_autobuy(steam_listing):
    steam_url='https://steamcommunity.com/market/listings/730/'+steam_listing
    html = requests.get(steam_url).text
    soup = BeautifulSoup(html, 'lxml')

    id = None
    for script in soup.find_all('script'):
        id_regex = re.search(r'Market_LoadOrderSpread\(([ 0-9]+)\)', script.text)
        if id_regex:
            id = id_regex.groups()[0].strip()
            break

    if id:
        id_url = f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}&two_factor=0"
        html = requests.get(id_url).json()
        soup = BeautifulSoup(html['buy_order_summary'], 'lxml')
        return float((soup.select_one('span:last-child').text).replace(' pуб.','').replace(',','.'))
    else:
        return 0
        exit()
