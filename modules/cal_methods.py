from google_api.google_calendar_api import *

import datetime

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

def create_gcal_event_from_dict(row_dict):
 
    return(create_event(f"{row_dict['club_name']} - {row_dict['event_title']}",row_dict['event_short_description'],datetime.datetime.strptime(f"{row_dict['event_date']} {format_time(row_dict['event_start_time'])}",'%m/%d/%y %H:%M:%S'),datetime.datetime.strptime(f"{row_dict['event_date']} {format_time(row_dict['event_end_time'])}",'%m/%d/%y %H:%M:%S'),row_dict['event_location'],row_dict['event_contacts']))

def update_gcal_event_from_dict(row_dict):
    return(update_event(row_dict['gcal_id'],f"{row_dict['club_name']} - {row_dict['event_title']}",row_dict['event_short_description'],datetime.datetime.strptime(f"{row_dict['event_date']} {format_time(row_dict['event_start_time'])}",'%m/%d/%y %H:%M:%S'),datetime.datetime.strptime(f"{row_dict['event_date']} {format_time(row_dict['event_end_time'])}",'%m/%d/%y %H:%M:%S'),row_dict['event_location'],row_dict['event_contacts']))


