#ge_watch.py

import bs4, pandas, plotly, requests, json, math, time

categories = {v : i for i, v in enumerate(['Miscellaneous',
        'Ammo', 'Arrows', 'Bolts', 'Construction materials',
        'Construction products', 'Cooking ingredients',
        'Costumes', 'Crafting materials', 'Familiars',
        'Farming produce', 'Fletching materials',
        'Food and Drink', 'Herblore materials',
        'Hunting equipment', 'Hunting produce', 'Jewellery',
        'Mage armor', 'Mage weapons', 'Melee armour - low level',
        'Melee armour - mid level', 'Melee armour - high level',
        'Melee weapons - low level', 'Melee weapons - mid level',
        'Melee weapons - high level', 'Mining and Smithing',
        'Potions', 'Prayer armour', 'Prayer materials',
        'Range armour', 'Range weapons', 'Runecrafting',
        'Runes, Spells and Teleports', 'Seeds',
        'Summoning scrolls', 'Tools and containers',
        'Woodcutting products', 'Pocket items', 'Stone spirits',
        'Salvage', 'Firemaking products', 'Archaeology materials'
        ])}

url = 'http://services.runescape.com/m=itemdb_rs/api/catalogue/'
detail_url = url + 'detail.json?item=%d'
config_url = 'https://secure.runescape.com/m=itemdb_rs/api/info.json'
catalogue_url = url + 'category.json?category=%d'
items_url = url + 'items.json?category=%d&alpha=%s&page=%d'

item_ids = {}
id_file_name = 'ids.txt'

def get_json(url, s = 10):
    err = True
    while err is True:
        try:
            print(url)
            return requests.get(url).json()
            err = False
        except json.decoder.JSONDecodeError:
            err = True
            print('Error, retrying...')
            time.sleep(s)

def get_last_runedate_update_configuration():
    return requests.get(config_url).json()['lastConfigUpdateRuneday']

def get_detail(item_id):
    return requests.get(detail_url % item_id).json()

def get_all_ids(s = 3):
    for c in categories.values():
        for a in get_json(catalogue_url % c)['alpha']:
            l = a['letter'].replace('#', '%23')
            for p in range(1, int(math.ceil(a['items'] / 12)) + 1):
                for i in get_json(items_url % (c, l, p))['items']:
                    item_ids[i['name']] = i['id']
                    print(i['name'], ':', i['id'])
                time.sleep(s)
    f = open(id_file_name, mode = 'w+')
    json.dump(item_ids, f)
    f.close()

def load_ids_from_file():
    f = open(id_file_name)
    r = json.load(f)
    f.close()
    return r

class Item:

    def __init__(self, name, item_id, limit):
        self.name = name
        self.id = item_id
        self.limit = limit

get_all_ids()
print('Done.')
