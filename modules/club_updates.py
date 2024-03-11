from google_api.google_sheets_api import *


def check_club_updates():
    edit_df = get_df_from_sheet('club_edit')
    approved_changes = edit_df[edit_df['is_approved']=='Y']
    rejected_changed = edit_df[edit_df['is_approved']=='N']

    club_df = get_df_from_sheet('club')

    for _, change in approved_changes.iterrows():
        update_club(change, club_df)

def update_club(change, df):
    id = change['club_id']
    for col, value in change.to_dict().items():
        if value != '' and col != 'club_id' and col != 'is_approved':
            df.loc[df['club_id']==id, col] = value
    update_sheet_with_df('club', df)






if __name__ == '__main__':
    check_club_updates()