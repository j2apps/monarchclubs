from google_api.google_calendar_api import *
from google_api.google_sheets_api import *


def create_gcal_event_from_dict(row_dict):
 
    return(create_event(f"{row_dict['club_name']} - {row_dict['event_title']}",row_dict['event_short_description'],format_time(row_dict['event_start_time']),format_time(row_dict['event_end_time']),row_dict['event_location'],row_dict['event_contacts']))

def update_gcal_event_from_dict(row_dict):
    return(update_event(row_dict['gcal_id'],f"{row_dict['club_name']} - {row_dict['event_title']}",row_dict['event_short_description'],format_time(row_dict['event_start_time']),format_time(row_dict['event_end_time']),row_dict['event_location'],row_dict['event_contacts']))

def format_time(time):
    t = time.split(' ')
    if t[1] == 'AM':
        return t[0]
    else:
        t1 = t[0].split(':',1)
        t2 = int(t1[0].lstrip('0'))
        t2+=12
        t3 = str(t2) + f":{t1[1]}"
        return t3
