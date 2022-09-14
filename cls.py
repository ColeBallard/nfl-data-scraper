from dataclasses import dataclass
from datetime import date

@dataclass
class Team:
    id: int = 0
    name: str = ''

@dataclass
class Stadium:
    id: int = 0
    name: str = ''
    elevation: int = 0

@dataclass
class Player:
    id: int = 0
    name: str = ''
    height: int = 0

@dataclass
class Report:
    id: int = 0
    source: str = ''
    description: str = ''
    published: date = date

@dataclass
class TeamName:
    id: int = 0
    name: str = ''
    team: Team = Team
    start_use_date: date = date
    end_use_date: date = date

@dataclass
class TeamStadium:
    id: int = 0
    team: Team = Team
    stadium: Stadium = Stadium
    start_use_date: date = date
    end_use_date: date = date

@dataclass
class PlayerReport:
    id: int = 0
    report: Report = Report
    player: Player = Player

@dataclass
class Game:
    id: int = 0
    postseason: int = 0
    home_teamstadium: TeamStadium = TeamStadium
    home_elevation_diff: int = 0
    away_teamstadium: TeamStadium = TeamStadium
    away_elevation_diff: int = 0
    date_played: date = date
    attendance: int = 0

@dataclass
class Stat:
    id: int = 0
    score: int = 0
    first_downs: int = 0
    rush_first_downs: int = 0
    pass_first_downs: int = 0
    pen_first_downs: int = 0
    total_net_yards: int = 0
    rush_net_yards: int = 0
    rush_plays: int = 0
    rush_avg_gain: float = 0.0
    pass_net_yards: int = 0
    pass_att: int = 0
    pass_cmp: int = 0
    pass_sack: int = 0
    pass_sack_yds_lost: int = 0
    pass_gross_yds: int = 0
    pass_avg_gain: float = 0.0
    punt_num: int = 0
    punt_avg: float = 0.0
    punt_block: int = 0
    punt_return_num: int = 0
    punt_return_yds: int = 0
    kickoff_return_num: int = 0
    kickoff_return_yds: int = 0
    int_return_num: int = 0
    int_return_yds: int = 0
    pen_num: int = 0
    pen_yds: int = 0
    fum_num: int = 0
    fum_lost: int = 0
    fg_att: int = 0
    fg_made: int = 0
    third_downs_cmp: int = 0
    third_downs_att: int = 0
    third_downs_ratio: float = 0.0
    fourth_downs_cmp: int = 0
    fourth_downs_att: int = 0
    fourth_downs_ratio: float = 0.0
    total_plays: int = 0
    avg_gain: float = 0.0
    time_of_poss: int = 0.0

@dataclass
class IndivStat:
    id: int = 0
    pass_att: int = 0
    pass_cmp: int = 0
    pass_yds: int = 0
    pass_ypa: float = 0.0
    pass_td: int = 0
    pass_int: int = 0
    pass_lg: int = 0
    pass_sack: int = 0
    pass_rate: float = 0.0
    rush_att: int = 0
    rush_yds: int = 0
    rush_avg: float = 0.0
    rush_lg: int = 0
    rush_td: int = 0
    rush_fd: int = 0
    rec_rec: int = 0
    rec_yds: int = 0
    rec_avg: float = 0.0
    rec_lg: int = 0
    rec_td: int = 0
    rec_fd: int = 0
    rec_tar: int = 0
    rec_yac: int = 0
    punt_ret_num: int = 0
    punt_ret_yds: int = 0
    punt_ret_avg: float = 0.0
    punt_ret_fc: int = 0
    punt_ret_lg: int = 0
    punt_ret_td: int = 0
    punt_punts: int = 0
    punt_yds: int = 0
    punt_avg: float = 0.0
    punt_lg: int = 0
    punt_tb: int = 0
    punt_in20: int = 0
    punt_ob: int = 0
    punt_fc: int = 0
    punt_dwn: int = 0
    punt_blk: int = 0
    punt_net: float = 0.0
    kick_pat_att: int = 0
    kick_pat_made: int = 0
    kick_fg_att: int = 0
    kick_fg_made: int = 0
    kickoff_num: int = 0
    kickoff_yds: int = 0
    kickoff_avg: float = 0.0
    kickoff_lg: int = 0
    kickoff_tb: int = 0
    kickoff_ob: int = 0
    def_int: int = 0
    def_yds: int = 0
    def_avg: float = 0.0
    def_lg: int = 0
    def_td: int = 0
    def_solo: int = 0
    def_ast: int = 0
    def_tot: int = 0
    def_sack: float = 0.0
    def_yds_lost: int = 0
    fum_fum: int = 0
    fum_lost: int = 0
    fum_forced: int = 0
    fum_own: int = 0
    fum_opp: int = 0
    fum_tot: int = 0
    fum_yds: int = 0
    fum_td: int = 0

@dataclass
class GameTeam:
    id: int = 0
    game: Game = Game
    team: Team = Team
    stat: Stat = Stat

@dataclass
class GamePlayer:
    id: int = 0
    game: Game = Game
    player: Player = Player
    indiv_stat: IndivStat = IndivStat
    weight: int = 0