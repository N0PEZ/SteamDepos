import re
import requests
from bs4 import BeautifulSoup
from random import choice

http = ['socks4://202.40.177.94:5678', 'http://101.33.252.195:8081', 'http://79.174.188.153:8080', 'http://103.181.168.218:8080', 'socks5://163.53.204.178:9813']


current_proxy = {
    'http': f'{choice(http)}',
}


def get_autobuy(steam_listing):
    steam_url='https://steamcommunity.com/market/listings/730/'+steam_listing
    current_proxy['http'] = choice(http)
    html = requests.get(steam_url, proxies=current_proxy,stream=True)
    print ('peername:', html.raw._connection.sock.getpeername())
    print(html.status_code)
    html=html.text
    soup = BeautifulSoup(html, 'lxml')
    print('proxy:', current_proxy['http'])
    id = None
    for script in soup.find_all('script'):
        id_regex = re.search(r'Market_LoadOrderSpread\(([ 0-9]+)\)', script.text)
        if id_regex:
            id = id_regex.groups()[0].strip()
            break

    if id:
        current_proxy['http'] = choice(http)
        id_url = f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid={id}&two_factor=0"
        html = requests.get(id_url, proxies=current_proxy)
        print(html.status_code)
        html = html.json()
        soup = BeautifulSoup(html['buy_order_summary'], 'lxml')
        return float((soup.select_one('span:last-child').text).replace(' pуб.','').replace(',','.'))
    else:
        return 0
        exit()
