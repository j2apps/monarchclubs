from google_api.google_sheets_api import *

def send_email():
    dfs = get_dfs()
    for key in dfs:
        df = dfs[key]['df']
        print(df)
        changes = get_changes(df)
        dfs[key]['changes'] = changes





def get_dfs():
    club_edit_df = get_df_from_sheet('club_edit')
    club_create_df = get_df_from_sheet('club_create')
    event_edit_df = get_df_from_sheet('event_edit')
    event_create_df = get_df_from_sheet('event_create')
    df_dict = {
        'club_edit': {
            'df': club_edit_df
        },
        'club_create': {
            'df': club_create_df
        },
        'event_edit': {
            'df': event_edit_df
        },
        'event_create': {
            'df': event_create_df
        }
    }
    return df_dict

def get_changes(df):
    remaining_changes = df[~df['is_approved'].isin(['Y', 'y', 'N', 'n'])]
    return remaining_changes

if __name__ == "__main__":
    send_email()