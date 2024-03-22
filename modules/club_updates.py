from google_api.google_sheets_api import *
import numpy as np

def check_club_edit():
    edit_df = get_df_from_sheet('club_edit')
    #print(edit_df.index)
    if len(edit_df.index)==0: return
    club_df = get_df_from_sheet('club')

    # So a human can view the entire new proposed state of the club
    edit_df = fill_unchanged_fields(edit_df, club_df)

    # Move approved changes to the club sheet
    approved_changes = edit_df[edit_df['is_approved'].isin(['Y','y'])]
    for _, change in approved_changes.iterrows():
        update_club(change, club_df)

    # Keeps unverified changed
    # Implicitly removes rejected changes
    remaining = edit_df[~edit_df['is_approved'].isin(['Y','y','N','n'])]
    update_sheet_with_df('club_edit', remaining)

def fill_unchanged_fields(edit_df, club_df):
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

    # Filter out edits for invalid club ids
    id_list = club_df['club_id'].to_list()

    # Move approved changes to the club sheet
    approved_changes = create_df[create_df['is_approved'].isin(['Y','y'])]
    print(approved_changes.index.to_list())
    for i in approved_changes.index.to_list():
        print(i)
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




if __name__ == '__main__':
    #check_club_edit()
    check_club_create()