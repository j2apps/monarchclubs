import gspread
from google.oauth2.service_account import Credentials

import pandas as pd

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file('Google_api/sheets_creds.json',scopes=scopes)
client = gspread.authorize(creds)

id_dict = {}

sheet_id = "1y0xzVtdDoeQGUe6SMuXRYEBLBD5CjB08kiENr3mxNig"
sheet_name = "Sheet1"

workbook= client.open_by_key(sheet_id)
sheet = workbook.worksheet(sheet_name)

def get_df_from_sheet(worksheet):
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def update_sheet_with_df(worksheet,df):
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def edit_cell(worksheet,cell,change):
    worksheet.update_acell(cell,change)

edit_cell(sheet,'A1','new')