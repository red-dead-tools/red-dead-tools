"""
Specific helpers to work with my RDR2 collecting spreadsheet data.
"""
import os
from functools import lru_cache

from . import base_dir
from .gsheets import get_sheet_rows


# env var for cloud injection
AUTH_ENV_VAR = 'RDT_GAUTH_JSON'

# private sub-module for portable local dev
AUTH_PATH = base_dir / 'red-dead-tools-private/.data/red-dead-tools-b475e08cb189.json'

ITEM_ROWS = 9


def get_gauth_json():
    return os.environ.get(AUTH_ENV_VAR) or AUTH_PATH.read_text()


@lru_cache
def get_rows(spreadsheet_name='RDR2 Collecting Needs', sheet_name="Tom"):
    return get_sheet_rows(get_gauth_json(), spreadsheet_name, sheet_name)


def get_col_item_needs():
    rows = get_rows()

    data = {}
    for prefix, col_name, *items in zip(*rows[: 2 + ITEM_ROWS]):
        if prefix and col_name != 'Weekly':
            col_name = f'{prefix} - {col_name}'
        data[col_name] = [it for it in items if it]

    return data


def get_no_hide_collections():
    rows = get_rows()

    cols = set()
    no_hide_rows = [row for row in rows if row[0] == 'No hide']
    rows = rows[:2] + no_hide_rows
    for prefix, col_name, no_hide in zip(*rows):
        if prefix and col_name != 'Weekly':
            col_name = f'{prefix} - {col_name}'
        if no_hide:
            cols.add(col_name)

    return cols


if __name__ == '__main__':
    rows = get_rows()
    print(rows)
    print()

    col_item_needs = get_col_item_needs()
    print(col_item_needs)
