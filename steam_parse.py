import re
import requests
from bs4 import BeautifulSoup
from random import choice

http = ['http://89.23.112.143:80', 'http://84.47.161.3:8118', 'http://77.232.21.4:8080', 'http://194.67.91.153:80', 'http://195.161.41.163:8080' ]

current_proxy = {
    'http': f'{choice(http)}',
}


def get_autobuy(steam_listing):
    steam_url='https://steamcommunity.com/market/listings/730/'+steam_listing
    current_proxy['http'] = choice(http)
    html = requests.get(steam_url, proxies=current_proxy,headers='')
    print(html.status_code)
    html=html.text
    soup = BeautifulSoup(html, 'lxml')
    print(current_proxy['http'])
    id = None
    for script in soup.find_all('script'):
        id_regex = re.search(r'Market_LoadOrderSpread\(([ 0-9]+)\)', script.text)
        if id_regex:
            id = id_regex.groups()[0].strip()
            break

    if id:
        current_proxy['http'] = choice(http)
        id_url = f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}&two_factor=0"
        html = requests.get(id_url, proxies=current_proxy,headers='')
        print(html.status_code)
        html = html.json()
        soup = BeautifulSoup(html['buy_order_summary'], 'lxml')
        return float((soup.select_one('span:last-child').text).replace(' pуб.','').replace(',','.'))
    else:
        return 111111111
        exit()
