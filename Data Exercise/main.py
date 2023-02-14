import copy
import csv
import datetime
import enum
from pathlib import Path
from itertools import groupby
from typing import List, Optional

#######GLOBAL FUNCTIONS##########################################################################
def read_csv_file(input_file: str) -> List[List[str]]:
    return [row for row in
            csv.reader(Path(input_file).read_text(encoding="utf-8").splitlines(), delimiter=',')]


def parse_year(v:str) -> datetime.date.year:
    return datetime.datetime.strptime(v, "%Y-%m-%d").year


Team = enum.Enum("Team", {team_name: team_name for team_name in set(list(map(lambda el: el[0], read_csv_file("football_results.csv")[1:])) +
                                                                    list(map(lambda el: el[1], read_csv_file("football_results.csv")[1:])))})

#######ZAD 1#####################################################################################
def total_matches_by_year(year: datetime.date.year, team: Optional[Team] = None) -> int:
    file_content = read_csv_file("football_results.csv")[1:]
    if team is None:
        total_matches = list(filter(lambda el: parse_year(el[2]) == year, file_content))
        return len(total_matches)
    else:
        total_matches = list(filter(lambda el: (parse_year(el[2]) == year) and (el[0] == team.value or el[1] == team.value), file_content))
        return len(total_matches)

#######ZAD 2#####################################################################################
def most_goals(records: int) -> List[tuple]:
    file_content = read_csv_file("football_results.csv")[1:]
    sort_key = lambda el: (el[0], el[3])
    matches = sorted(list(map(lambda el: (el[2], el[0], el[1], int(el[3]) + int(el[4])), file_content)), key = sort_key, reverse = True)
    return matches[:records]


#######ZAD 3#####################################################################################
def team_matches_stats_per_year(team: Team) -> dict:
    file_content = read_csv_file("football_results.csv")[1:]
    group_by_key = lambda el: el[0]
    stats = {"w": 0, "l": 0, "d": 0, "p": 0}
    total_matches = {}

    years = sorted(list(map(lambda el: (parse_year(el[2]), el[0], el[1], el[3], el[4], el[5]), filter(lambda el: (el[0] == team.value or el[1] == team.value), file_content))), key= group_by_key)

    iterator1 = groupby(years, group_by_key)
    for key, group in iterator1:
        total_matches.update({str(key): copy.copy(stats)})
        w = filter(lambda el: (el[0] == key and ((el[1] == team.value and int(el[3]) > int(el[4])) or (el[2] == team.value and int(el[3]) < int(el[4])))), group)
        total_matches[str(key)]['w'] = len(list(w))

    iterator2 = groupby(years, group_by_key)
    for key, group in iterator2:

        l = filter(lambda el: (el[0] == key and ((el[1] == team.value and int(el[3]) < int(el[4])) or (el[2] == team.value and int(el[3]) > int(el[4])))), group)
        total_matches[str(key)]['l'] = len(list(l))

    iterator3 = groupby(years, group_by_key)
    for key, group in iterator3:

        d = filter(lambda el: (el[0] == key and ((el[1] == team.value and int(el[3]) == int(el[4])) or (el[2] == team.value and int(el[3]) == int(el[4])))), group)
        total_matches[str(key)]['d'] = len(list(d))

    iterator4 = groupby(years, group_by_key)
    for key, group in iterator4:
        p = filter(lambda el: (el[0] == key and ((el[1] == team.value and el[5] == "P") or (el[2] == team.value and el[5] == "P"))), group)
        total_matches[str(key)]['p'] = len(list(p))

    return total_matches


#######ZAD 4#####################################################################################
def teams_summary(records: Optional = None) -> List[dict]:
    file_content = read_csv_file("football_results.csv")[1:]
    group_by_key_home = lambda el: el[0]
    group_by_key_away = lambda el: el[1]
    stats = {"team": "", "played": 0, "won": 0, "draw": 0, "lost": 0, "for": 0, "against": 0, "gd": 0, "points": 0}
    summary = []
    home_teams = sorted(list(map(lambda el: (el[0], el[1], el[3], el[4]), file_content)), key=group_by_key_home)

    iterator_home1 = groupby(home_teams, group_by_key_home)
    for key, group in iterator_home1:
        stats['team'] = key
        played = filter(lambda el: (el[0] == key), group)
        stats['played'] = len(list(played))
        summary.append(copy.copy(stats))

    iterator_home2 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home2:
        won = filter(lambda el: (el[0] == key and int(el[2]) > int(el[3])), group)
        summary[idx]['won'] = len(list(won))
        idx += 1

    iterator_home3 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home3:
        draw = filter(lambda el: (el[0] == key and int(el[2]) == int(el[3])), group)
        summary[idx]['draw'] = len(list(draw))
        idx += 1

    iterator_home4 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home4:
        lost = filter(lambda el: (el[0] == key and int(el[2]) < int(el[3])), group)
        summary[idx]['lost'] = len(list(lost))
        idx += 1

    iterator_home5 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home5:
        goals = list(map(lambda el: int(el[2]), filter(lambda el: (el[0] == key), group)))
        summary[idx]['for'] = sum(goals)
        idx += 1

    iterator_home6 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home6:
        against = list(map(lambda el: int(el[3]), filter(lambda el: (el[0] == key), group)))
        summary[idx]['against'] = sum(against)
        idx += 1

    iterator_home7 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home7:
        gd = int(summary[idx]['for']) - int(summary[idx]['against'])
        summary[idx]['gd'] = gd
        idx += 1

    iterator_home8 = groupby(home_teams, group_by_key_home)
    idx = 0
    for key, group in iterator_home8:
        points = 3*int(summary[idx]['won']) + int(summary[idx]['draw'])
        summary[idx]['points'] = points
        idx += 1

    team_away = sorted(list(map(lambda el: (el[0], el[1], el[3], el[4]), file_content)), key=group_by_key_away)
    iterator_away1 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away1:
        if not any(s['team'] == key for s in summary):
            stats['team'] = key
            played = filter(lambda el: (el[1] == key), group)
            stats['played'] = len(list(played))
            summary.append(copy.copy(stats))
        else:
            played = filter(lambda el: (el[1] == key), group)
            team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
            summary[team_idx]['played'] += len(list(played))

    iterator_away2 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away2:
        won = filter(lambda el: (el[1] == key and int(el[2]) < int(el[3])), group)
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        summary[team_idx]['won'] += len(list(won))

    iterator_away3 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away3:
        draw = filter(lambda el: (el[1] == key and int(el[2]) == int(el[3])), group)
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        summary[team_idx]['draw'] += len(list(draw))

    iterator_away4 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away4:
        lost = filter(lambda el: (el[1] == key and int(el[2]) > int(el[3])), group)
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        summary[team_idx]['lost'] += len(list(lost))

    iterator_away5 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away5:
        goals = list(map(lambda el: int(el[3]), filter(lambda el: (el[1] == key), group)))
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        summary[team_idx]['for'] += sum(goals)

    iterator_away6 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away6:
        against = list(map(lambda el: int(el[2]), filter(lambda el: (el[1] == key), group)))
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        summary[team_idx]['against'] += sum(against)

    iterator_away7 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away7:
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        gd = int(summary[team_idx]['for']) - int(summary[team_idx]['against'])
        summary[team_idx]['gd'] = gd

    iterator_away8 = groupby(team_away, group_by_key_away)
    for key, group in iterator_away8:
        team_idx = next((index for (index, s) in enumerate(summary) if s["team"] == key), None)
        points = 3 * int(summary[team_idx]['won']) + int(summary[team_idx]['draw'])
        summary[team_idx]['points'] = points

    summary = sorted(summary, key=lambda s: s['points'], reverse = True)

    if records is None:
        return summary
    else:
        return summary[:records]


#######TESTY#####################################################################################
zad_1 = total_matches_by_year(1950, Team("Liverpool FC"))
print(zad_1)

zad_2 = most_goals(10)
print(zad_2)

zad_3 = team_matches_stats_per_year(Team("Queens Park FC"))
print(zad_3)

zad_4 = teams_summary(10)
print(zad_4)

#AUTOR: MATEUSZ GAJDA GRUPA: WCY20IJ1S1