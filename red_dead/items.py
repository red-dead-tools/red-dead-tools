from difflib import get_close_matches

import httpx

from .caching import cache
from .models import Collection, Item


REPO_BASE_URL = 'https://raw.githubusercontent.com/jeanropke/RDR2CollectorsMap/master'
ITEM_URL = f'{REPO_BASE_URL}/langs/en.json'
WEEKLY_URL = f'{REPO_BASE_URL}/data/weekly_sets.json'
WEEKLY_SET_URL = 'https://pepegapi.jeanropke.net/v2/rdo/weekly'

TWELVE_HOURS = 12 * 60 * 60


@cache(expire_secs=TWELVE_HOURS)
def parse_data():
    data = httpx.get(ITEM_URL).json()

    collections = {}
    items = {}

    for long_code, name in data.items():
        col_item_code, _, attrib = long_code.partition('.')

        if attrib != 'name':
            continue

        col_code = col_item_code.split('_', 1)[0]

        try:
            col_name = data[f'menu.{col_code}']
        except KeyError:
            continue

        try:
            col = collections[col_name]
        except KeyError:
            col = Collection(code=col_code, name=col_name)
            collections[col_name] = col

        item = Item(code=col_item_code, name=name, collection=col)
        items[col_item_code] = item

    data = httpx.get(WEEKLY_SET_URL).json()
    current = data['set'].replace('AWARD_ROLE_COLLECTOR_SET_', '').lower() + '_set'

    data = httpx.get(WEEKLY_URL).json()

    weekly_item_codes = data['sets'][current]
    col = Collection(code='weekly', name='Weekly')
    for item_code in weekly_item_codes['items']:
        orig = items[item_code]
        item = Item(code=item_code, name=orig.name, collection=col)
        items[f'weekly_{item_code}'] = item
    collections['weekly'] = col

    return set(collections.values()), set(items.values())


def numerise(text):
    num_names = 'ace two three four five six seven eight nine ten'.title().split()
    num_map = {str(i): f'{name} of ' for i, name in enumerate(num_names, 1)}
    num_map.update({'t': 'knight', 'p': 'page', 'q': 'queen', 'k': 'king'})
    return num_map.get(text.lower().strip(), text)


def guess_by_name(name, objs):
    name = numerise(name)

    obj_map = {obj.name.lower(): obj for obj in objs}
    guesses = get_close_matches(name.lower(), obj_map, n=1, cutoff=0.1)
    try:
        guess = guesses[0]
    except IndexError:
        raise ValueError(f'{name} not found in {", ".join(obj_map.keys())}')
    return obj_map[guess]


def get_collection(collection_name):
    collections, _ = parse_data()
    return guess_by_name(collection_name, collections)


def get_item(item_name, collection_name=None):
    collections, items = parse_data()

    if collection_name:
        items = items_for_collection(collection_name, items)

    return guess_by_name(item_name, items)


def get_item_by_code(item_code, items):
    return next(
        it for it in items if it.code == item_code if it.collection.name != 'Weekly'
    )


def items_for_collection(collection_name, items):
    collection = get_collection(collection_name)
    return {i for i in items if i.collection == collection}
