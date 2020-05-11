from datetime import datetime
from collections import defaultdict

from .sheet_transform import get_col_item_needs
from .models import Settings
from .items import get_item, parse_data
from . import base_dir

export_path = base_dir / 'exports'


def get_important():
    imp_items = defaultdict(set)
    for col_name, items in get_col_item_needs().items():
        for item_name in items:
            of_import = not item_name.startswith('!')
            item_name = item_name.strip('!')
            item = get_item(item_name, col_name)
            print(f'{col_name:>30} - {item_name:>30} --> {item.name}')
            imp_items[of_import].add(item)
    return imp_items[True], imp_items[False]


def get_settings():
    _, items = parse_data()

    important, unimportant = get_important()

    unimportant = unimportant | items - important

    return Settings(
        important_items=important,
        unimportant_items=unimportant,
    )


def write_export():
    s = get_settings()
    now = datetime.now()
    path = export_path / now.strftime('%Y-%m-%d_%H-%M-%S.json')

    path.write_text(s.as_json())
    print(f'export written to {path}')


if __name__ == '__main__':
    s = get_settings()

    write_export()
