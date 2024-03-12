from google_api.google_sheets_api import *

def check_club_updates():
    edit_df = get_df_from_sheet('club_edit')
    club_df = get_df_from_sheet('club')
    id_list = club_df['club_id'].to_list()
    edit_df = edit_df[edit_df['club_id'].isin(id_list)]

    approved_changes = edit_df[edit_df['is_approved']=='Y']

    for _, change in edit_df.iterrows():
        fill_unchanged_fields(change, edit_df, club_df)

    #implicitly removes rejected changes
    remaining = edit_df[edit_df['is_approved']=='']
    update_sheet_with_df('club_edit', remaining)


    for _, change in approved_changes.iterrows():
        update_club(change, club_df)

def fill_unchanged_fields(change, edit_df, club_df):
    id = change['club_id']
    ignored_cols = ['club_id', 'is_approved', 'timestamp', 'email_address']
    current_club_info = club_df.loc[club_df['club_id']==id]
    for col, value in change.to_dict().items():
        if str(value).strip() == '' and col not in ignored_cols:
            edit_df.loc[edit_df['club_id']==id, col] = current_club_info[col]
    update_sheet_with_df('club_edit', edit_df)

def update_club(change, df):
    id = change['club_id']
    ignored_cols = ['club_id', 'is_approved', 'timestamp', 'email_address']
    for col, value in change.to_dict().items():
        if str(value).strip() != '' and col not in ignored_cols:
            df.loc[df['club_id']==id, col] = value
    update_sheet_with_df('club', df)


if __name__ == '__main__':
    check_club_updates()