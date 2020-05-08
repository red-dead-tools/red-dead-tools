import json
from pathlib import Path
from difflib import get_close_matches
from functools import lru_cache

from .models import Collection, Item


base_dir = Path(__file__).parent.parent
data_path = base_dir / 'data' / 'en.json'


@lru_cache
def parse_data():
    with data_path.open() as stream:
        data = json.load(stream)

    collections = {}
    items = set()

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
        items.add(item)

    return collections.values(), items


def guess_by_name(name, objs):
    obj_map = {obj.name.lower(): obj for obj in objs}
    guesses = get_close_matches(name.lower(), obj_map, n=1, cutoff=0.1)
    try:
        guess = guesses[0]
    except IndexError:
        raise ValueError(f'{name} not found in {", ".join(obj_map.keys())}')
    return obj_map[guess]


def get_collection(collection_name):
    collections, items = parse_data()
    return guess_by_name(collection_name, collections)


def get_item(item_name, collection_name=None):
    collections, items = parse_data()

    if collection_name:
        collection = get_collection(collection_name)
        items = [i for i in items if i.collection == collection]

    return guess_by_name(item_name, items)
