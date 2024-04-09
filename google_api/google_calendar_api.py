import datetime
import os.path
import re


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth

scopes = ["https://www.googleapis.com/auth/calendar"]
cal_id = "7aa10897ba6aa68a4bca1b1a503ce8bfff38982fd5c946546368e45c05a61c9f@group.calendar.google.com"


def authenticate():
    creds = None
    if os.path.exists("gcal_token.json"):
        creds = Credentials.from_authorized_user_file("gcal_token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.dirname(__file__)+"/gcalendar_creds.json", scopes)
            creds = flow.run_local_server(port=0)

        with open("gcal_token.json","w")as token:
            token.write(creds.to_json())
    return creds

service = build("calendar", "v3", credentials=authenticate())
event_dict = {}



def create_event(name,desc,start,end):
    try:
            
        details  = {
            "summary": str(name),
            "description": str(desc),
            "start":{
                "dateTime": f"{start}.00Z"
                    
            },
            "end":{
                "dateTime": f"{end}.00Z"
                    
               }
        }
            
    except HttpError as error:
        print(error)
    event = service.events().insert(calendarId = cal_id, body = details).execute()
    
    return event['id']

def delete_event(event_id):
    try:
        service.events().delete(calendarId = cal_id, eventId = 'sjs252k2emd309b01dt2f81c50').execute()
        
    except HttpError as error:
        print(error)

def update_event(event):
    try:
        service.events().update(calendarId=cal_id,eventId='',body='')
        
    except HttpError as error:
        print(error)



