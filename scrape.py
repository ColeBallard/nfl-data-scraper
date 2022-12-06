from datetime import datetime
from requests_html import HTMLSession
import pandas as pd

def getGame(session, url, player_stats_id, export):
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

    team_stats_sections = res.html.find('#divBox_team', first=True).find('tbody')

    for section in team_stats_sections:
        
        for row in section.find('tr'):

            stats = row.find('td')

            stat_name = stats[0].text

            stat_name = stat_name.lower().replace(' ', '_').replace('_-_', '-').replace('.', '')

            team_stats_obj[f'away_{stat_name}'] = stats[1].text

            team_stats_obj[f'home_{stat_name}'] = stats[2].text

    team_stats_obj['player_stats_id'] = player_stats_id

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

    team_df = pd.DataFrame.from_dict([team_stats_obj])

    player_df = pd.DataFrame.from_dict(player_stats_obj, orient='index')

    if export:
        team_df.to_csv('team_stats.csv')

        player_df.to_csv('player_stats.csv')

    return [team_df, player_df]

def getGames(start_year, end_year, last_year_start_week, last_year_end_week):
    session = HTMLSession()

    player_stats_id = 0

    final_team_df = pd.DataFrame()

    final_player_df = pd.DataFrame()

    for year in range(start_year, end_year + 1):
        res = session.get(f'https://www.footballdb.com/games/index.html?lg=NFL&yr={year}')

        if year != end_year:

            for week in res.html.find('.statistics'):

                for game in week.find('tbody tr'):

                    if game.find('a', first=True) == None:
                        continue

                    game_url = str(game.find('a', first=True).links)
                    game_url = game_url.replace("{'", '')
                    game_url = game_url.replace("'}", '')

                    url = f'https://www.footballdb.com{game_url}'

                    print(url)

                    game_stats = getGame(session, url, player_stats_id, False)

                    final_team_df = final_team_df.append(game_stats[0])

                    final_player_df = final_player_df.append(game_stats[1])

                    player_stats_id += 1

        else:

            for week in res.html.find('.statistics')[last_year_start_week - 1:last_year_end_week]:

                for game in week.find('tbody tr'):

                    if game.find('a', first=True) == None:
                        continue

                    game_url = str(game.find('a', first=True).links)
                    game_url = game_url.replace("{'", '')
                    game_url = game_url.replace("'}", '')

                    url = f'https://www.footballdb.com{game_url}'

                    print(url)

                    game_stats = getGame(session, url, player_stats_id, False)

                    final_team_df = final_team_df.append(game_stats[0])

                    final_player_df = final_player_df.append(game_stats[1])

                    player_stats_id += 1

    return [final_team_df, final_player_df]

def getLastFinishedWeek(year):
    session = HTMLSession()

    res = session.get(f'https://www.footballdb.com/games/index.html?lg=NFL&yr={year}')

    week_count = 0

    for week in res.html.find('.statistics'):

        no_game = False

        for game in week.find('tbody tr'):

            if game.find('a', first=True) == None:
                no_game = True

        if no_game == False:
            week_count += 1

        else:
            break

    return week_count

def getNFLYear():
    current_year = int(datetime.today().strftime('%Y'))

    current_month = int(datetime.today().strftime('%m'))

    if current_month < 6:
        current_year -= 1

    return current_year

def readScrapeInfo():
    with open('info.txt', 'r') as f:
        latest_scraped_year = int(f.readline().replace('latest_scraped_year = ', '').rstrip())

        latest_scraped_week = int(f.readline().replace('latest_scraped_week = ', '').rstrip())

        return [latest_scraped_year, latest_scraped_week]

def writeScrapeInfo(current_year, last_finished_week):
    with open('info.txt', 'w') as f:
        f.writelines('\n'.join([f'latest_scraped_year = {current_year}', f'latest_scraped_week = {last_finished_week}']))

#############################################################################

def getMostRecentGames():
    current_year = getNFLYear()

    last_finished_week = getLastFinishedWeek(current_year)

    scrapeInfo = readScrapeInfo()
    
    recent_dfs = getGames(scrapeInfo[0], current_year, scrapeInfo[1] + 1, last_finished_week)

    writeScrapeInfo(current_year, last_finished_week)

    team_df = pd.read_csv('team_stats.csv')

    player_df = pd.read_csv('player_stats.csv')

    team_df = team_df.append(recent_dfs[0], ignore_index = True)

    player_df = player_df.append(recent_dfs[1], ignore_index = True)

    team_df.to_csv('team_stats_new.csv', header=False)

    player_df.to_csv('player_stats_new.csv', header=False)

def getAllGames():
    current_year = getNFLYear()

    last_finished_week = getLastFinishedWeek(current_year)

    final_dfs = getGames(1978, current_year, 1, last_finished_week)

    final_dfs[0].to_csv('team_stats.csv')

    final_dfs[1].to_csv('player_stats.csv')

    writeScrapeInfo(current_year, last_finished_week)