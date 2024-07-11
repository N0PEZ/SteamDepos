import requests
import sqlite3
import urllib.parse
#from steam_parse import get_autobuy

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
                market_total REAL,
                steam_link TEXT
            )
        ''')
        conn.commit()


        weapons_and_knives = [
            'AK-47', 'M4A1-S', 'M4A4', 'AWP', 'SSG 08', 'AUG', 'SG 553',
            'FAMAS', 'Galil AR', 'G3SG1', 'SCAR-20', 'MAC-10', 'MP7', 'MP9',
            'PP-Bizon', 'P90', 'UMP-45', 'MP5-SD', 'M249', 'Negev', 'MAG-7',
            'Nova', 'Sawed-Off', 'XM1014', 'Glock-18', 'USP-S', 'P2000', 'Dual Berettas',
            'P250', 'Five-SeveN', 'Tec-9', 'CZ75-Auto', 'Desert Eagle', 'R8 Revolver',
            'Knife', 'Flip Knife', 'Bayonet', 'Butterfly Knife', 'Karambit',
            'Gut Knife', 'Huntsman Knife', 'Falchion Knife', 'Bowie Knife',
            'Shadow Daggers', 'Ursus Knife', 'Navaja Knife', 'Stiletto Knife',
            'Talon Knife', 'Classic Knife', 'Paracord Knife', 'Survival Knife',
            'Skeleton Knife', 'Nomad Knife',
            'Ava', 'B Squadron Officer', 'Blackwolf', 'Blueberries', 'Buckshot',
            'Cmdr. Davida', 'Cmdr. Frank', 'Col. Mangos', 'Darryl', 'Dead Cold',
            'Dragomir', 'Elite Crew', 'FBI', 'Getaway Sally', 'Gendarmerie',
            'Ground Rebel', 'Lt. Rex Krikey', 'M | Sekiro', 'Marcus Delrow', 'Maximus',
            'Michael Syfers', 'No. 0 1/2', 'Number K', 'Officer Jacques',
            'Osiris', 'Paramedic', 'Prof. Shahmat', 'Rezan The Redshirt',
            'Rosa', 'Rush', 'Safecracker Voltzmann', 'Seal Team 6 Soldier',
            'Sir Bloody Darryl', 'Sir Bloody Miami', 'Sir Bloody Silent',
            'Sir Bloody Skipper', 'Sir Bloody Loudmouth', 'Sniper', 'Soldier',
            'Special Agent Ava', 'Special Agent Blueberries', 'Special Agent Hoss',
            'Special Agent Marcus', 'Special Agent Michael', 'Squadron Officer'
        ]

        for item in items:
            name = item.get('market_hash_name', '')
            price = round(float(item.get('price', 0)) * 1.075,2)
            if any(weapon in name for weapon in weapons_and_knives) and price >= 100:
                steam_listing = format_name_for_steam(name)
                #get_autobuy(steam_listing)
                cursor.execute('''
                    INSERT OR REPLACE INTO items (name, market_total, steam_link)
                    VALUES (?, ?, ?)
                ''', (name, price, steam_listing))

        conn.commit()
        conn.close()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

cs_market_url = "https://market.csgo.com/api/v2/prices/RUB.json"
cs_market_api(cs_market_url)