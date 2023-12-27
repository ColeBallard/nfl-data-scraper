from datetime import datetime
import pandas as pd
import math

def getTeams():
    team_names = {}

    team_names_df = pd.read_csv('https://raw.githubusercontent.com/ColeBallard/historical-nfl-team-names/main/historical-nfl-team-names.csv')

    for index, team in team_names_df.iterrows():
        team_names[team['Team']] = team['CurrentTeam']

    return team_names

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

def seperateTeamStats(df):
    seperate_teams = {}

    for team in getTeams():
        seperate_teams[team] = {}

    for index, row in df.iterrows():
        month = datetime.strptime(row['date'], '%B %d, %Y').month

        year = datetime.strptime(row['date'], '%B %d, %Y').year

        if month >= 1 and month <= 6:
            year -= 1

        if year not in seperate_teams[row['team']].keys():
            seperate_teams[row['team']][year] = [row]

        else:
            seperate_teams[row['team']][year].append(row)

    return seperate_teams

def getWinPct(index, team, year, seperate_team_stats):
    wins = 0.0

    if index == 0:
        return None

    for game in seperate_team_stats[team][year][0:index]:
        wins += game['outcome']

    return wins / index

def getWinStreak(index, team, year, seperate_team_stats):
    streak = 0

    if index == 0:
        return 0

    for game in seperate_team_stats[team][year][0:index]:
        if streak >= 1:
            if game['outcome'] == 1:
                streak += 1

            elif game['outcome'] == 0:
                streak = -1

        elif streak <= -1:
            if game['outcome'] == 1:
                streak = 1

            elif game['outcome'] == 0:
                streak -= 1

        else:
            if game['outcome'] == 1:
                streak = 1

            elif game['outcome'] == 0:
                streak = -1
        
    # ties don't affect streak

    return streak

def unknownToNull(x):
    if x == 'unknown':
        return None

    else:
        return x

#############################################################################

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

def splitTeamStats(df, export_file):
    df = df.reset_index()

    split_objs = []

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

        split_objs.append(away_team_obj)
        split_objs.append(home_team_obj)

    split_df = pd.DataFrame.from_dict(split_objs)

    # delete unnamed and pointless columns
    split_df = split_df.drop(split_df.columns[[2, 3, 4]],axis = 1)

    split_df['attendance'] = split_df['attendance'].apply(unknownToNull)

    split_df.to_csv(export_file)

def staggerTeamStats(df, team_dict, export_file):
    df = df.reset_index()

    seperate_teams = seperateTeamStats(df)

    seperate_teams_list = []

    for team in seperate_teams:

        for year in seperate_teams[team]:

            for index, game in enumerate(seperate_teams[team][year]):

                # -1 to account for 0 index, and -1 to account for no outcome associated with final game stats
                if index <= (len(seperate_teams[team][year]) - 2):
                    game['outcome'] = seperate_teams[team][year][index + 1]['outcome']
                    game['home_or_away'] = seperate_teams[team][year][index + 1]['home_or_away']
                    game['postseason'] = seperate_teams[team][year][index + 1]['postseason']
                    game['opponent'] = seperate_teams[team][year][index + 1]['opponent']
                    game['date'] = seperate_teams[team][year][index + 1]['date']
                    game['stadium'] = seperate_teams[team][year][index + 1]['stadium']

                    game['current_team'] = team_dict[game['team']]
                    game['opp_current_team'] = team_dict[game['opponent']]

                    game['team_win_pct'] = getWinPct(index, team, year, seperate_teams)
                    game['opp_win_pct'] = getWinPct(index, game['opponent'], year, seperate_teams)

                    game['team_win_streak'] = getWinStreak(index, team, year, seperate_teams)
                    game['opp_win_streak'] = getWinStreak(index, game['opponent'], year, seperate_teams)

                    seperate_teams_list.append(game)

    seperate_df = pd.DataFrame(seperate_teams_list)

    for index, col in enumerate(seperate_df.columns.values):
        if index >= 9 and index <= 102:
            seperate_df.rename(columns={seperate_df.columns[index]: f'prev_{col}'},inplace=True)

    seperate_df = seperate_df.drop(seperate_df.columns[1], axis=1)

    # move player stats id and game index columns to end

    cols_list = list(seperate_df.columns.values)

    cols_list.pop(cols_list.index('prev_player_stats_id'))

    cols_list.pop(cols_list.index('prev_game_index'))

    seperate_df = seperate_df[cols_list + ['prev_player_stats_id'] + ['prev_game_index']]

    seperate_df.to_csv(export_file)

def preprocessTeamStats(df, export_file):
    df = df.reset_index()

    # Drop the first column
    df = df.iloc[:, 1:]

    df = df.drop(['index', 'team', 'opponent', 'stadium', 'current_team', 'opp_current_team', 'prev_player_stats_id', 'prev_game_index'], axis=1)

    

    df.to_csv(export_file)

#############################################################################

def showMenu():
    print("\nMenu:")
    print("1. Perform All Transformations")
    print("2. Expand Team Stats")
    print("3. Split Team Stats")
    print("4. Stagger Team Stats")
    print("5. Preprocess Team Stats")
    print("6. Exit")
    choice = input("Enter your choice (1/2/3/4/5): ")
    return choice

def main():
    while True:
        user_choice = showMenu()

        if user_choice == '1':
            team_df = pd.read_csv('team_stats.csv')
            expandTeamStats(team_df, 'expanded_team_stats.csv')

            expanded_df = pd.read_csv('expanded_team_stats.csv')
            splitTeamStats(expanded_df, 'expanded_split_team_stats.csv')

            expanded_split_df = pd.read_csv('expanded_split_team_stats.csv')
            staggerTeamStats(expanded_split_df, getTeams(), 'staggered_team_stats.csv')

            staggered_df = pd.read_csv('staggered_team_stats.csv')
            preprocessTeamStats(staggered_df, 'preprocessed_team_stats.csv')

        elif user_choice == '2':
            team_df = pd.read_csv('team_stats.csv')
            expandTeamStats(team_df, 'expanded_team_stats.csv')

        elif user_choice == '3':
            expanded_df = pd.read_csv('expanded_team_stats.csv')
            splitTeamStats(expanded_df, 'expanded_split_team_stats.csv')

        elif user_choice == '4':
            expanded_split_df = pd.read_csv('expanded_split_team_stats.csv')
            staggerTeamStats(expanded_split_df, getTeams(), 'staggered_team_stats.csv')

        elif user_choice == '5':
            staggered_df = pd.read_csv('staggered_team_stats.csv')
            preprocessTeamStats(staggered_df, 'preprocessed_team_stats.csv')

        elif user_choice == '6':
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()