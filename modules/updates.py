from google_api.google_sheets_api import *
import numpy as np

def check_club_edit():
    edit_df = get_df_from_sheet('club_edit')
    #print(edit_df.index)
    if len(edit_df.index)==0: return
    club_df = get_df_from_sheet('club')

    # So a human can view the entire new proposed state of the club
    edit_df = fill_unchanged_club_fields(edit_df, club_df)

    # Move approved changes to the club sheet
    approved_changes = edit_df[edit_df['is_approved'].isin(['Y','y'])]
    for _, change in approved_changes.iterrows():
        update_club(change, club_df)

    # Keeps unverified changed
    # Implicitly removes rejected changes
    remaining = edit_df[~edit_df['is_approved'].isin(['Y','y','N','n'])]
    update_sheet_with_df('club_edit', remaining)

def fill_unchanged_club_fields(edit_df, club_df):
    ignored_cols = ['club_id', 'is_approved', 'timestamp', 'email_address']
    edit_df = edit_df.replace(np.nan, '')

    # Iterate through every proposed change
    for _, change in edit_df.iterrows():
        # Pull current club info from club sheet
        id = change['club_id']
        current_club_info = club_df.loc[club_df['club_id']==id].iloc[0]

        # Fill every empty field in the proposed change with the current club info
        for col, value in change.to_dict().items():
            if str(value).strip() in ['', np.nan] and col not in ignored_cols:
                edit_df.loc[edit_df['club_id']==id, col] = current_club_info[col]

    # Remove NaN
    edit_df = edit_df.replace(np.nan, '')
    return edit_df

def update_club(change, df):
    id = change['club_id']
    ignored_cols = ['club_id', 'is_approved', 'timestamp', 'email_address']

    # Change every non-empty field from the proposed change
    for col, value in change.to_dict().items():
        if str(value).strip() != '' and col not in ignored_cols:
            df.loc[df['club_id']==id, col] = value
    update_sheet_with_df('club', df)


def check_club_create():
    create_df = get_df_from_sheet('club_create')
    #print(edit_df.index)
    if len(create_df.index)==0: return
    club_df = get_df_from_sheet('club')

    # Move approved changes to the club sheet
    approved_changes = create_df[create_df['is_approved'].isin(['Y','y'])]
    for i in approved_changes.index.to_list():
        row = approved_changes[approved_changes.index==i]
        new_club = create_club(row, club_df)
        club_df = pd.concat([club_df, new_club])

    remaining = create_df[~create_df['is_approved'].isin(['Y', 'y', 'N', 'n'])]
    update_sheet_with_df('club_create', remaining)
    update_sheet_with_df('club', club_df)


def create_club(new_club, club_df):
    # Find the new id based on the max of the current ids
    id_list = club_df['club_id'].to_list()
    new_id = max(id_list, key=lambda x: int(x) if not np.isnan(x) else 0) + 1
    new_club['club_id'] = new_id
    # Get rid of fields not needed for the club
    columns = club_df.columns.to_list()
    new_club = new_club[columns]
    return new_club

def check_event_create():
    create_df = get_df_from_sheet('event_create')

    if len(create_df.index) == 0: return
    event_df = get_df_from_sheet('event')
    club_df = get_df_from_sheet('club')

    # Move approved changes to the club sheet
    approved_changes = create_df[create_df['is_approved'].isin(['Y', 'y'])]
    print(approved_changes.head())
    for i in approved_changes.index.to_list():
        row = approved_changes[approved_changes.index == i]
        new_event = create_event(row, event_df, club_df)
        event_df = pd.concat([event_df, new_event])

    # Remove event create requests that have either already been processed or have been marked unapproved
    '''remaining = create_df[~create_df['is_approved'].isin(['Y', 'y', 'N', 'n'])]
    update_sheet_with_df('event_create', remaining)
    update_sheet_with_df('event', event_df)'''


def create_event(new_event, event_df, club_df):
    # Find the new id based on the max of the current ids
    event_df_for_specific_club = event_df.loc[event_df['club_id'] == new_event['club_id'].iloc[0]]
    event_id_list = event_df_for_specific_club['event_id'].to_list()
    # Assign an event ID to the event
    new_id = max(event_id_list, key=lambda x: int(x) if not np.isnan(x) else 0) + 1
    new_event['event_id'] = new_id
    # Get rid of fields not needed for the club, excluding gcal_id as it is inot yet determined
    columns = event_df.columns.to_list()
    columns.remove("gcal_id")
    new_event = new_event[columns]
    # Give the event a club_name field taken from the club df
    new_event = add_club_name_to_event(new_event, club_df)
    return new_event

def add_club_name_to_event(event, club_df):
    club = club_df[club_df['club_id'] == event['club_id'].iloc[0]]
    event['club_name'] = club['club_name']
    return event


def check_event_edit():
    edit_df = get_df_from_sheet('event_edit')
    if len(edit_df.index)==0: return
    event_df = get_df_from_sheet('event')

    # So a human can view the entire new proposed state of the club
    edit_df = fill_unchanged_event_fields(edit_df, event_df)

    # Move approved changes to the club sheet
    approved_changes = edit_df[edit_df['is_approved'].isin(['Y','y'])]
    for _, change in approved_changes.iterrows():
        update_club(change, event_df)

    # Keeps unverified changed
    # Implicitly removes rejected changes
    remaining = edit_df[~edit_df['is_approved'].isin(['Y','y','N','n'])]
    update_sheet_with_df('event_edit', remaining)

def fill_unchanged_event_fields(edit_df, event_df):
    ignored_cols = ['club_id', 'event_id', 'is_approved', 'timestamp', 'email_address']
    edit_df = edit_df.replace(np.nan, '')

    # Iterate through every proposed change
    for _, change in edit_df.iterrows():
        # Pull current club info from club sheet
        club_id = change['club_id']
        event_id = change['event_id']
        current_event_info = event_df.loc[(event_df['club_id'] == club_id) & (event_df['event_id'] == event_id)].iloc[0]

        # Fill every empty field in the proposed change with the current club info
        for col, value in change.to_dict().items():
            if str(value).strip() in ['', np.nan] and col not in ignored_cols:
                edit_df.loc[(edit_df['club_id'] == club_id) & (edit_df['event_id'] == event_id), col] = current_event_info[col]

    # Remove NaN
    edit_df = edit_df.replace(np.nan, '')
    return edit_df

def run_checks():
    check_club_create()
    check_club_edit()
    check_event_create()


if __name__ == '__main__':
    #check_club_edit()
    #check_club_create()
    #check_event_edit()
    check_event_create()
