weapons_and_types = {'Pistol':['CZ75-Auto', 'Desert Eagle', 'Dual Berettas', 'Five-SeveN', 'Glock-18', 'P2000', 'P250', 'R8 Revolver', 'Tec-9', 'USP-S'],
'Rifle':['AK-47', 'AUG', 'FAMAS', 'Galil AR', 'M4A1-S', 'M4A4', 'SG 553'],
'Sniper%20Rifle':['AWP', 'G3SG1', 'SCAR-20', 'SSG 08'],
'SMG':['MAC-10', 'MP5-SD', 'MP7', 'MP9', 'P90', 'PP-Bizon', 'UMP-45'],
'Machinegun':['M249', 'Negev'],
'Shotgun':['MAG-7', 'Nova', 'Sawed-Off', 'XM1014'],
'Knife':['Shadow Daggers', 'Bayonet', 'Karambit', 'Knife', '★'],
'Gloves':['Hand Warps', 'gloves', '★'],
'Container':['Case', 'Capsule', 'Package', '201', '202'],
'Key':['Key'],
'Patch':['Patch |'],
'Graffiti':['Sealed Graffiti |'],
'Music%20Kit':['Music Kit |'],
'Agent':['| SWAT', '| KSK', '| Guerrilla Warfare', '| Gendarmerie Nationale', '| Sabre', '| The Professionals', '| NSWC SEAL', '| SAS', '| USAF TACP', '| TACP Cavalry',
          '| SAS', '| SEAL Frogman', '| Sabre Footsoldier', '| NZSAS', '| Phoenix', '| Elite Crew', '| FBI HRT', '| FBI Sniper', '| Brazilian 1st Battalion'],
'Pass':['Pass'],
'Equipment':['Zeus x27']}

weapon_types = ['Pistol', 'Rifle', 'Sniper%20Rifle', 'SMG', 'Machinegun', 'Shotgun', 'Knife',
                  'Container', 'Key', 'Patch', 'Graffiti', 'Music%20Kit', 'Agent', 'Pass', 'Equipment']
def create_link(name, steam_listing):
    for weapon_type in weapon_types:
        for weapon in weapons_and_types[weapon_type]:
            if weapon in name:
                link=f'https://market.csgo.com/ru/{weapon_type}/{steam_listing}'
                return link