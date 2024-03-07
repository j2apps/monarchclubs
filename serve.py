import pandas as pd

def get_df_from_sheet():
    return pd.read_csv('resources/sample_club_sheet.csv')

# returns the id, name, and short and long descitpion of every club in a list
# to be used to serve the landing page
def get_home_page_club_list() -> list[dict]:
    df = get_df_from_sheet()[['club_id','club_name','short_description','meeting_times']]
    club_list = df.T.to_dict().values()
    return club_list

# returns all information about a club from its id
def get_club_from_id(id: int) -> dict:
    df = get_df_from_sheet()
    club = df[df['club_id']==id].iloc[0].to_dict()
    return club


if __name__ == '__main__':
    get_club_from_id(2)
