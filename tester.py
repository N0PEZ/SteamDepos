import json

with open ('beb.json') as beb:
    data=json.load(beb)
    print(data)