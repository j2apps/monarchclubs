import gspread
from google.oauth2.service_account import Credentials

import pandas as pd

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file('credentials.json',scopes=scopes)
client = gspread.authorize(creds)

id_dict = {}

workbook = None
sheet = None

def define_sheet(sheet_id,sheet_name):
    workbook= client.open_by_key(sheet_id)
    sheet = workbook.worksheet(sheet_name)

def get_df_from_sheet():
    pass

if __name__ == "__main__":
    pass