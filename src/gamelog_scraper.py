"""
Scrape gamelogs
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_gamelog(playerid):
    """
    Given a player id scrape that NBA player's season game log data from basketball-reference.com
    """
    url = f"https://www.basketball-reference.com/players/a/{playerid}/gamelog/2024"
    r = requests.get(url)
    soup_parser = BeautifulSoup(r.content, "html.parser")
    gamelog_table = soup_parser.find(name="table", attrs={"id": "pgl_basic"})

    if gamelog_table is None:
        print(f"No game log table found at {url}")
        return None

    player_gamelog = []

    # column names : data-stat attributes
    columns = {
        "Rk": "ranker",
        "G": "game_season",
        "Date": "date_game",
        "Age": "age",
        "Tm": "team_id",
        "loc": "game_location",
        "Opp": "opp_id",
        "Res": "game_result",
        "GS": "gs",
        "MP": "mp",
        "FG": "fg",
        "FGA": "fga",
        "FG%": "fg_pct",
        "3P": "fg3",
        "3PA": "fg3a",
        "3P%": "fg3_pct",
        "FT": "ft",
        "FTA": "fta",
        "FT%": "ft_pct",
        "ORB": "orb",
        "DRB": "drb",
        "TRB": "trb",
        "AST": "ast",
        "STL": "stl",
        "BLK": "blk",
        "TOV": "tov",
        "PF": "pf",
        "PTS": "pts",
        "GmSc": "game_score",
        "+/-": "plus_minus",
    }

    for row in gamelog_table.tbody.find_all("tr", attrs={"class": None}):

        # Case for when player Did Not Play
        if row.find("td", {"data-stat": "reason"}):
            continue

        player = {}

        for column_name, data_stat in columns.items():
            if column_name == "Rk":
                player[column_name] = row.find("th", {"data-stat": data_stat}).text
            else:
                player[column_name] = row.find("td", {"data-stat": data_stat}).text

        player_gamelog.append(player)

    df = pd.DataFrame(player_gamelog)
    if not df.empty:
        df.set_index("Rk", inplace=True)
    return df
