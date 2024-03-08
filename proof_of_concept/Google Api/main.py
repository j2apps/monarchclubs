import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file('credentials.json',scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1y0xzVtdDoeQGUe6SMuXRYEBLBD5CjB08kiENr3mxNig"

workbook = client.open_by_key(sheet_id)

sheet = workbook.worksheet("Sheet1")

sheet.update_acell("A1","hello")