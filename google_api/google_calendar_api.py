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

'''
start and end time must be in YYYY-MM-DDTHH:MM:SS
'''
def create_event(name,desc,start,end,loc,contact):
    try:
            
        details  = {
            "summary": str(name),
            "description": str(desc),
            "start":{
                "dateTime": f"{start}",
                "timeZone": "America/Denver"
                    
            },
            "end":{
                "dateTime": f"{end}",
                "timeZone": "America/Denver"
               },
            "location": str(loc),
            "creator":{
                "displayName":str(contact)
            }
        }
        event = service.events().insert(calendarId = cal_id, body = details).execute()
        return event['id']
    except HttpError as error:
        return None
    
    
    

def delete_event(event_id):
    try:
        service.events().delete(calendarId = cal_id, eventId = event_id).execute()
        
    except HttpError as error:
        return None

        

def update_event(event_Id,name,desc,start,end,loc,contact):
    try:
        details  = {
            "summary": str(name),
            "description": str(desc),
            "start":{
                "dateTime": f"{start}",
                "timeZone": "America/Denver"
                    
            },
            "end":{
                "dateTime": f"{end}",
                "timeZone": "America/Denver"
               },
            "location": str(loc),
            "creator":{
                "displayName":str(contact)
            }
        }
        event = service.events().update(calendarId=cal_id,eventId=event_Id,body=details).execute()
        return event['id']
        
    except HttpError as error:
        return None
