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
def format_date(date):
    month = date.split('/')[0]
    if len(str(date)) == 0:
        date = "0" + date
    return date
def create_gcal_event_from_dict(row_dict):
    start_time = datetime.datetime.strptime(f"{format_date(row_dict['event_date'])} {format_time(row_dict['event_start_time'])}",'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
    end_time = datetime.datetime.strptime(f"{row_dict['event_date']} {format_time(row_dict['event_end_time'])}",'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
    return(create_event(f"{row_dict['club_name']} - {row_dict['event_title']}",
                        row_dict['event_short_description'],
                        start_time,
                        end_time,
                        row_dict['event_location'],
                        row_dict['event_contacts']))

def update_gcal_event_from_dict(row_dict):
    return(update_event(row_dict['gcal_id'],f"{row_dict['club_name']} - {row_dict['event_title']}",row_dict['event_short_description'],datetime.datetime.strptime(f"{format_date(row_dict['event_date'])} {format_time(row_dict['event_start_time'])}",'%m/%d/%Y %H:%M:%S'),datetime.datetime.strptime(f"{row_dict['event_date']} {format_time(row_dict['event_end_time'])}",'%m/%d/%Y %H:%M:%S'),row_dict['event_location'],row_dict['event_contacts']))


#if __name__ == "__main__":
