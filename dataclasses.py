from dataclasses import dataclass
from datetime import date

@dataclass
class Team:
    id: int
    name: str

@dataclass
class Stadium:
    id: int
    name: str
    elevation: int

@dataclass
class Player:
    id: int
    name: str
    height: int

@dataclass
class Report:
    id: int
    source: str
    description: str
    published: date

@dataclass
class TeamName:
    id: int
    name: str
    team: Team
    start_use_date: date
    end_use_date: date

@dataclass
class TeamStadium:
    id: int
    team: Team
    stadium: Stadium
    start_use_date: date
    end_use_date: date

@dataclass
class PlayerReport:
    id: int
    report: Report
    player: Player

@dataclass
class Game:
    id: int
    postseason: int
    home_teamstadium: TeamStadium
    home_elevation_diff: int
    away_teamstadium: TeamStadium
    away_elevation_diff: int
    date_played: date
    attendance: int

@dataclass
class Stat:
    id: int
    score: int
    first_downs: int
    rush_first_downs: int
    pass_first_downs: int
    pen_first_downs: int
    total_net_yards: int
    rush_net_yards: int
    rush_plays: int
    rush_avg_gain: float
    pass_net_yards: int
    pass_att: int
    pass_cmp: int
    pass_sack: int
    pass_sack_yds_lost: int
    pass_gross_yds: int
    pass_avg_gain: float
    punt_num: int
    punt_avg: float
    punt_block: int
    punt_return_num: int
    punt_return_yds: int
    kickoff_return_num: int
    kickoff_return_yds: int
    int_return_num: int
    int_return_yds: int
    pen_num: int
    pen_yds: int
    fum_num: int
    fum_lost: int
    fg_att: int
    fg_made: int
    third_downs_cmp: int
    third_downs_att: int
    third_downs_ratio: float
    fourth_downs_cmp: int
    fourth_downs_att: int
    fourth_downs_ratio: float
    total_plays: int
    avg_gain: float
    time_of_poss: int

@dataclass
class IndivStat:
    id: int
    pass_att: int
    pass_cmp: int
    pass_yds: int
    pass_ypa: float
    pass_td: int
    pass_int: int
    pass_lg: int
    pass_sack: int
    pass_rate: float
    rush_att: int
    rush_yds: int
    rush_avg: float
    rush_lg: int
    rush_td: int
    rush_fd: int
    rec_rec: int
    rec_yds: int
    rec_avg: float
    rec_lg: int
    rec_td: int
    rec_fd: int
    rec_tar: int
    rec_yac: int
    punt_ret_num: int
    punt_ret_yds: int
    punt_ret_avg: float
    punt_ret_fc: int
    punt_ret_lg: int
    punt_ret_td: int
    punt_punts: int
    punt_yds: int
    punt_avg: float
    punt_lg: int
    punt_tb: int
    punt_in20: int
    punt_ob: int
    punt_fc: int
    punt_dwn: int
    punt_blk: int
    punt_net: float
    kick_pat_att: int
    kick_pat_made: int
    kick_fg_att: int
    kick_fg_made: int
    kickoff_num: int
    kickoff_yds: int
    kickoff_avg: float
    kickoff_lg: int
    kickoff_tb: int
    kickoff_ob: int
    def_int: int
    def_yds: int
    def_avg: float
    def_lg: int
    def_td: int
    def_solo: int
    def_ast: int
    def_tot: int
    def_sack: float
    def_yds_lost: int
    fum_fum: int
    fum_lost: int
    fum_forced: int
    fum_own: int
    fum_opp: int
    fum_tot: int
    fum_yds: int
    fum_td: int

@dataclass
class GameTeam:
    id: int
    game: Game
    team: Team
    stat: Stat

@dataclass
class GamePlayer:
    id: int
    game: Game
    player: Player
    indiv_stat: IndivStat
    weight: int