"""
Specific helpers to work with my RDR2 collecting spreadsheet data.
"""
import os

from .gsheets import get_sheet_rows
from . import base_dir

# env var for cloud injection
AUTH_ENV_VAR = 'RDT_GAUTH_JSON'

# private sub-module for portable local dev
AUTH_PATH = base_dir / 'red-dead-tools-private/.data/red-dead-tools-b475e08cb189.json'

ITEM_ROWS = 8


def get_gauth_json():
    return os.environ.get(AUTH_ENV_VAR) or AUTH_PATH.read_text()


def get_rows(spreadsheet_name='RDR2 Collecting Needs', sheet_name="Tom’s dailies"):
    return get_sheet_rows(get_gauth_json(), spreadsheet_name, sheet_name)


def get_col_item_needs():
    rows = get_rows()

    data = {}
    for prefix, col_name, *items in zip(*rows[:2 + ITEM_ROWS]):
        if prefix:
            col_name = f'{prefix} - {col_name}'
        data[col_name] = [it for it in items if it]

    return data


if __name__ == '__main__':
    rows = get_rows()
    print(rows)
    print()

    col_item_needs = get_col_item_needs()
    print(col_item_needs)
