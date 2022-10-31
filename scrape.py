from datetime import datetime
from requests_html import HTMLSession
from IPython.display import display
import pandas as pd
from cls import Team, TeamName

def getTeams():
    team_list = []

    data = pd.read_csv('https://raw.githubusercontent.com/ColeBallard/historical-nfl-team-names/main/historical-nfl-team-names.csv')

    i = 0

    for team in data['CurrentTeam'].unique():
        team_list.append(Team(id=i, name=team))

        i += 1

    return team_list

def getTeamNames(team_list):
    team_name_list = []

    data = pd.read_csv('https://raw.githubusercontent.com/ColeBallard/historical-nfl-team-names/main/historical-nfl-team-names.csv')


    for i, row in data.iterrows():
        team_name_list.append(TeamName(id=i, name=row['Team'], teamId=list(filter(lambda x: x.name == row['CurrentTeam'], team_list))[0].id, start_use_date=row['YearStart'], end_use_date=row['YearEnd']))

    return team_name_list

def getGame(session, url, player_stats_id, export):
    team_stat_headers = ['First downs', 'Rushing', 'Passing', 'Penalty', 'Total Net Yards', 'Net Yards Rushing', 'Rushing Plays', 'Average Gain', 'Net Yards Passing', 'Att - Comp - Int', 'Sacked - Yds Lost', 'Gross Yards Passing', 'Avg. Yds/Att', 'Punts - Average', 'Had Blocked', 'Punt Returns', 'Kickoff Returns', 'Interception Returns', 'Penalties - Yards', 'Fumbles - Lost', 'Field Goals', 'Third Downs', 'Fourth Downs', 'Total Plays', 'Average Gain', 'Time of Possession']

    res = session.get(url)

    team_stats_obj = {}

    game_info = res.html.find('center')[1].text.split('\n')

    if 'AFC' in game_info[0] or 'NFC' in game_info[0] or 'Super Bowl' in game_info[0]:
        if 'Wild Card' in game_info[0]:
            team_stats_obj['postseason'] = 1

        elif 'Divisional' in game_info[0]:
            team_stats_obj['postseason'] = 2

        elif 'Championship' in game_info[0]:
            team_stats_obj['postseason'] = 3

        elif 'Super Bowl' in game_info[0]:
            team_stats_obj['postseason'] = 4

        playoff_add = 1

    else:
        team_stats_obj['postseason'] = 0

        playoff_add = 0

    team_names = game_info[0 + playoff_add]

    team_stats_obj['away_team'] = team_names[:team_names.index(' at ')]
    team_stats_obj['home_team'] = team_names[(team_names.index(' at ') + 4):]

    team_stats_obj['date'] = game_info[1 + playoff_add]
    team_stats_obj['stadium'] = game_info[2 + playoff_add]

    if len(game_info) == 4 and 'Attendance' in game_info[3]:
        team_stats_obj['attendance'] = game_info[3][12:].replace(',', '')

    elif len(game_info) == 5 and 'Attendance' in game_info[4]:
        team_stats_obj['attendance'] = game_info[4][12:].replace(',', '')

    else:
        team_stats_obj['attendance'] = 'unknown'

    score_line = res.html.find('.statistics', first=True).text.split('\n')

    if score_line[4] == '5':
        team_stats_obj['overtime'] = 'true'

        team_stats_obj['away_score'] = score_line[12]

        team_stats_obj['home_score'] = score_line[19]

        for i in range(5):
            team_stats_obj[f'away_score_q{i + 1}'] = score_line[7 + i]

        for i in range(5):
            team_stats_obj[f'home_score_q{i + 1}'] = score_line[14 + i]

    else:
        team_stats_obj['overtime'] = 'false'

        team_stats_obj['away_score'] = score_line[10]

        team_stats_obj['home_score'] = score_line[16]

        for i in range(4):
            team_stats_obj[f'away_score_q{i + 1}'] = score_line[6 + i]

        team_stats_obj['away_score_q5'] = '0'
            
        for i in range(5):
            team_stats_obj[f'home_score_q{i + 1}'] = score_line[12 + i]

        team_stats_obj['home_score_q5'] = '0'

    team_stats = res.html.find('#divBox_team', first=True).text.split('\n')

    i = -1

    for stat in team_stats:
        i += 1

        if i == 0:
            continue

        elif i == 1:
            away_team_abb = stat

        elif i == 2:
            home_team_abb = stat

        elif stat == home_team_abb or stat == away_team_abb:
            i -= 1
            continue

        elif stat in team_stat_headers:
            stat_name = stat.lower().replace(' ', '_')
            stat_name = stat_name.replace('_-_', '-')
            stat_name = stat_name.replace('.', '')

            i = 3

        elif i % 3 == 1:
            team_stats_obj[f'away_{stat_name}'] = stat

        elif i % 3 == 2:
            team_stats_obj[f'home_{stat_name}'] = stat

    team_stats_obj['player_stats_id'] = player_stats_id

    # print(team_stats_obj)

    player_stats_obj = {}

    player_stats = res.html.find('#divBox_stats', first=True).text.split('\n')

    for stat in player_stats:
        if stat == 'Passing':
            stat_section = 'pass'

        elif stat == 'Rushing':
            stat_section = 'rush'

        elif stat == 'Receiving':
            stat_section = 'rec'

        elif stat == 'Kickoff Returns':
            stat_section = 'kick_ret'

        elif stat == 'Punt Returns':
            stat_section = 'punt_ret'

        elif stat == 'Punting':
            stat_section = 'punt'

        elif stat == 'Kicking':
            stat_section = 'kick'

        elif stat == 'Kickoffs':
            stat_section = 'kickoff'

        elif stat == 'Defense':
            stat_section = 'def'

        elif stat == 'Fumbles':
            stat_section = 'def'

        elif team_stats_obj['away_team'] in stat:
            team = 'away'
            header_flag = True
            stat_headers = []

        elif team_stats_obj['home_team'] in stat:
            team = 'home'
            header_flag = True
            stat_headers = []

        elif '.\xa0' in stat:
            header_flag = False
            player = stat[:(stat.index('.\xa0') - 1)]

            if team == 'away' and player not in player_stats_obj:
                player_stats_obj[player] = {'date': team_stats_obj['date'], 'team': team_stats_obj['away_team'], 'player_stats_id': player_stats_id}

            elif team == 'home' and player not in player_stats_obj:
                player_stats_obj[player] = {'date': team_stats_obj['date'], 'team': team_stats_obj['home_team'], 'player_stats_id': player_stats_id}

            i = 0

        elif stat == 'TeamTeam' or stat == '.':
            header_flag = False
            player = ''

        else:
            if header_flag:
                stat_headers.append(f'{stat_section}_{stat.lower()}')

            else:
                if player != '':
                    player_stats_obj[player][stat_headers[i]] = stat

                    i += 1

    # print(player_stats_obj)

    team_df = pd.DataFrame.from_dict([team_stats_obj])

    player_df = pd.DataFrame.from_dict(player_stats_obj, orient='index')

    # display(team_df)

    # display(player_df)

    if export:
        team_df.to_csv('team_stats.csv')

        player_df.to_csv('player_stats.csv')

    return [team_df, player_df]

def getGames():
    session = HTMLSession()

    player_stats_id = 0

    final_team_df = pd.DataFrame()

    final_player_df = pd.DataFrame()

    for year in range(1978, 2022):
        res = session.get(f'https://www.footballdb.com/games/index.html?lg=NFL&yr={year}')

        for week in res.html.find('.statistics'):

            for game in week.find('tbody tr'):

                game_url = str(game.find('a', first=True).links)
                game_url = game_url.replace("{'", '')
                game_url = game_url.replace("'}", '')

                url = f'https://www.footballdb.com{game_url}'

                print(url)

                game_stats = getGame(session, url, player_stats_id, False)

                final_team_df = final_team_df.append(game_stats[0])

                final_player_df = final_player_df.append(game_stats[1])

                player_stats_id += 1

    final_team_df.to_csv('team_stats.csv')

    final_player_df.to_csv('player_stats.csv')

getGames()

# getGame(HTMLSession(), 'https://www.footballdb.com/games/boxscore/tennessee-titans-vs-miami-dolphins-2004091204', 0, True)