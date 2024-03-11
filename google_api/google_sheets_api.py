import gspread
from google.oauth2.service_account import Credentials
import os
import pandas as pd

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file(os.path.dirname(__file__)+'/sheets_creds.json',scopes=scopes)
client = gspread.authorize(creds)

id_dict = {"club": ("1EtErKxuI_SCU7avKLKxrFqbVsZrVqyKXEfSiQ3J-tHo","Sheet1"),
           "club_edit": ('1oavfSWb2_M288pCnpDGKd1QA4sodIiOf_QeFZaZ4PDw', 'Sheet1')}

def get_df_from_sheet(sheet_name: str) -> pd.DataFrame:
    worksheet = get_worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def update_sheet_with_df(sheet_name, df):
    worksheet = get_worksheet(sheet_name)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def edit_cell(sheet_name,cell,change):
    worksheet=get_worksheet(sheet_name)
    worksheet.update_acell(cell,change)

def get_worksheet(sheet_name: str):
    sheet_id, sheet_name = id_dict[sheet_name]
    workbook = client.open_by_key(sheet_id)
    worksheet = workbook.worksheet(sheet_name)
    return worksheet