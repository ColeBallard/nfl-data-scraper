import pandas as pd
import math

def createSplitTeamStats(df, export_file):
    df = df.reset_index()

    split_df = pd.DataFrame()

    df_cols = df.columns.tolist()

    for index, row in df.iterrows():
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

        for col in df_cols:
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

        split_df = split_df.append(away_team_obj, ignore_index=True)
        split_df = split_df.append(home_team_obj, ignore_index=True)

    split_df.to_csv(export_file)

def makeOneDash(dash_stat):
    return dash_stat.replace('--', '-')

def toSeconds(min_sec):
    if not isinstance(min_sec, str) and math.isnan(min_sec):
        return None

    min_sec_arr = min_sec.split(':')

    return (int(min_sec_arr[0]) * 60) + int(min_sec_arr[1])

def colOneDash(df):
    extra_dash_cols = ['away_punt_returns', 'home_punt_returns', 'away_kickoff_returns', 'home_kickoff_returns', 'away_interception_returns', 'home_interception_returns']

    for col in extra_dash_cols:

        df[col] = df[col].apply(makeOneDash)

    return df

def nullToZero(x):
    if isinstance(x, str):

        if x == '':
            return 0

        x = float(x)

    if math.isnan(x):
        return 0

    else: 
        return x

def colNullToZero(df):
    possible_null_cols = ['away_had_blocked', 'home_had_blocked', 'away_int_returns', 'home_int_returns', 'away_int_returns_yds', 'home_int_returns_yds', 'away_punts', 'home_punts', 'away_punts_avg', 'home_punts_avg', 'away_fg_made', 'home_fg_made', 'away_fg_att', 'home_fg_att']

    for col in possible_null_cols:

        df[col] = df[col].apply(nullToZero)

    return df

def percentToDecimal(x):
    if isinstance(x, float):
        return None

    return float(x.strip('%')) / 100

def colPercentToDecimal(df):
    percent_cols = ['away_fourth_downs_percent', 'home_fourth_downs_percent', 'away_third_downs_percent', 'home_third_downs_percent']

    for col in percent_cols:
        df[col] = df[col].apply(percentToDecimal)

    return df

def expandTeamStats(df, export_file):
    df = df.reset_index()

    expanded_cols = {
        'away_att-comp-int':['away_pass_att', 'away_pass_comp', 'away_pass_int'],
        'home_att-comp-int':['home_pass_att', 'home_pass_comp', 'home_pass_int'],
        'away_sacked-yds_lost':['away_sacked', 'away_sacked_yds_lost'],
        'home_sacked-yds_lost':['home_sacked', 'home_sacked_yds_lost'],
        'away_punts-average':['away_punts', 'away_punts_avg'],
        'home_punts-average':['home_punts', 'home_punts_avg'],
        'away_punt_returns':['away_punt_returns_count', 'away_punt_returns_yds'],
        'home_punt_returns':['home_punt_returns_count', 'home_punt_returns_yds'],
        'away_kickoff_returns':['away_kickoff_returns_count', 'away_kickoff_returns_yds'],
        'home_kickoff_returns':['home_kickoff_returns_count', 'home_kickoff_returns_yds'],
        'away_interception_returns':['away_int_returns', 'away_int_returns_yds'],
        'home_interception_returns':['home_int_returns', 'home_int_returns_yds'],
        'away_penalties-yards':['away_penalties', 'away_penalties_yds'],
        'home_penalties-yards':['home_penalties', 'home_penalties_yds'],
        'away_fumbles-lost':['away_fumbles', 'away_fumbles_lost'],
        'home_fumbles-lost':['home_fumbles', 'home_fumbles_lost'],
        'away_field_goals':['away_fg_made', 'away_fg_att'],
        'home_field_goals':['home_fg_made', 'home_fg_att'],
        'away_third_downs':['away_third_downs_made', 'away_third_downs_att', 'away_third_downs_percent'],
        'home_third_downs':['home_third_downs_made', 'home_third_downs_att', 'home_third_downs_percent'],
        'away_fourth_downs':['away_fourth_downs_made', 'away_fourth_downs_att', 'away_fourth_downs_percent'],
        'home_fourth_downs':['home_fourth_downs_made', 'home_fourth_downs_att', 'home_fourth_downs_percent']
    }

    df = colOneDash(df)

    for col in expanded_cols:
        
        df[expanded_cols[col]] = df[col].str.split('-', expand=True)
        
        df = df.drop(col, axis=1)

        if '_count' in col:
            df = df.rename(columns={col: col.replace('_count', '')})

    df['away_time_of_possession'] = df['away_time_of_possession'].apply(toSeconds)

    df['home_time_of_possession'] = df['home_time_of_possession'].apply(toSeconds)

    df = df.rename(columns={'away_rushing': 'away_first_downs_rushing', 'home_rushing': 'home_first_downs_rushing', 'away_passing': 'away_first_downs_passing', 'home_passing': 'home_first_downs_passing', 'away_penalty': 'away_first_downs_penalty', 'home_penalty': 'home_first_downs_penalty', 'away_average_gain': 'away_rush_avg', 'home_average_gain': 'home_rush_avg', 'away_avg_yds/att': 'away_pass_att_avg', 'home_avg_yds/att': 'home_pass_att_avg'})

    df = colPercentToDecimal(df)

    df = colNullToZero(df)

    cols_list = list(df.columns.values)

    cols_list.pop(cols_list.index('player_stats_id'))

    df = df[cols_list + ['player_stats_id']]

    df.to_csv(export_file)

# team_df = pd.read_csv('team_stats.csv')

# expandTeamStats(team_df, 'expanded_team_stats.csv')

expanded_df = pd.read_csv('expanded_team_stats.csv')

createSplitTeamStats(expanded_df, 'expanded_split_team_stats.csv')