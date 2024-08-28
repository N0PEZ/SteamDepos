import time
from datetime import datetime
import requests as req


STEAM_URL = "https://steamcommunity.com/market/itemordershistogram?country=RU&language=english&currency=5&item_nameid=49399548"

def make_req():
    r = req.get(STEAM_URL)
    if r.status_code != 200:
        return (False, r.status_code)
    return (True, r.status_code, r.text)

sc = 0
count = 0

for i in range(4999):
    print(make_req()[0:2], i)

print("START: " + datetime.now().strftime("%H:%M:%S"))

while sc != 200:
    tmp = make_req()
    sc = tmp[1]
    if tmp[0] == False:
        time.sleep(count)
        print(f"Time: {count} ")
        count += 5*60

print("END: " + datetime.now().strftime("%H:%M:%S"))