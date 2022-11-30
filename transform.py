import pandas as pd

def createSplitTeamStats():
    team_df = pd.read_csv('team_stats.csv')

    team_df = team_df.reset_index()

    split_team_df = pd.DataFrame()

    team_df_cols = team_df.columns.tolist()

    for index, row in team_df.iterrows():
        away_team_obj = {}
        home_team_obj = {}

        if row['away_score'] > row['home_score']:
            away_team_obj['outcome'] = 1
            home_team_obj['outcome'] = 0

        elif row['away_score'] < row['home_score']:
            away_team_obj['outcome'] = 0
            home_team_obj['outcome'] = 1

        else:
            away_team_obj['outcome'] = 0.5
            home_team_obj['outcome'] = 0.5

        away_team_obj['home_or_away'] = 1
        home_team_obj['home_or_away'] = 0

        for col in team_df_cols:
            if 'away' not in col and 'home' not in col:
                away_team_obj[col] = row[col]
                home_team_obj[col] = row[col]

            elif col == 'away_team':
                away_team_obj['team'] = row[col]
                home_team_obj['opponent'] = row[col]

            elif col == 'home_team':
                home_team_obj['team'] = row[col]
                away_team_obj['opponent'] = row[col]

            elif 'away' in col:
                away_team_obj[col.replace('away', 'team')] = row[col]
                home_team_obj[col.replace('away', 'opp')] = row[col]

            elif 'home' in col:
                away_team_obj[col.replace('home', 'opp')] = row[col]
                home_team_obj[col.replace('home', 'team')] = row[col]

            else:
                print('error')

        away_team_obj['game_index'] = away_team_obj.pop('index')
        home_team_obj['game_index'] = home_team_obj.pop('index')

        split_team_df = split_team_df.append(away_team_obj, ignore_index=True)
        split_team_df = split_team_df.append(home_team_obj, ignore_index=True)

    split_team_df.to_csv('split_team_stats.csv')