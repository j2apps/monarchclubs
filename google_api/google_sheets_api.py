import gspread
from google.oauth2.service_account import Credentials
import os
import pandas as pd

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file(os.path.dirname(__file__)+'/sheets_creds.json',scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1xgoY1gbn867EmpvY0rf4aWf9cTzCPENDwtyGQoXZpe0'

def get_df_from_sheet(sheet_name: str) -> pd.DataFrame:
    worksheet = get_worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def update_sheet_with_df(sheet_name, df):
    worksheet = get_worksheet(sheet_name)
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def edit_cell(sheet_name,cell,change):
    worksheet=get_worksheet(sheet_name)
    worksheet.update_acell(cell,change)

def get_worksheet(sheet_name: str):
    workbook = client.open_by_key(sheet_id)
    worksheet = workbook.worksheet(sheet_name)
    return worksheet