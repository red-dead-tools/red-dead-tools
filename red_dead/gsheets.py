"""
Generic helpers for fetching data from Google Spreadsheets.
"""
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def gsheets_api_connect(gauth_json):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    gauth_dict = json.loads(gauth_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        gauth_dict, scope
    )
    return gspread.authorize(credentials)


def get_sheet_rows(gauth_json, spreadsheet_name, sheet_name):
    conn = gsheets_api_connect(gauth_json)
    spreadsheet = conn.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(sheet_name)
    rows = sheet.get_all_values()
    return rows
