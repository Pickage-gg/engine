import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_gamelog(url, table_id):
    """
    Scrape specific NBA player's season game log data from basketball-reference.com when given a url and html table id
    """
    r = requests.get(url)
    soup_parser = BeautifulSoup(r.content, "html.parser")
    gamelog_table = soup_parser.find(name="table", attrs={"id": table_id})

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
    df.set_index("Rk", inplace=True)
    return df


"""
def get_gamelog(url, table_id):

    r = requests.get(url)
    soup_parser = BeautifulSoup(r.content, "html.parser")
    gamelog_table = soup_parser.find(name="table", attrs={"id": table_id})

    player_gamelog = []

    for row in gamelog_table.tbody.find_all("tr", attrs={"class": None}):

        # case for the when player Did Not Play
        if row.find("td", {"data-stat": "reason"}):
            continue

        player = {}

        player["Rk"] = row.find("th", {"data-stat": "ranker"}).text
        player["G"] = row.find("td", {"data-stat": "game_season"}).text
        player["Date"] = row.find("td", {"data-stat": "date_game"}).text
        player["Age"] = row.find("td", {"data-stat": "age"}).text
        player["Tm"] = row.find("td", {"data-stat": "team_id"}).text
        player["loc"] = row.find("td", {"data-stat": "game_location"}).text
        player["Opp"] = row.find("td", {"data-stat": "opp_id"}).text
        player["Res"] = row.find("td", {"data-stat": "game_result"}).text
        player["GS"] = row.find("td", {"data-stat": "gs"}).text
        player["MP"] = row.find("td", {"data-stat": "mp"}).text
        player["FG"] = row.find("td", {"data-stat": "fg"}).text
        player["FGA"] = row.find("td", {"data-stat": "fga"}).text
        player["FG%"] = row.find("td", {"data-stat": "fg_pct"}).text
        player["3P"] = row.find("td", {"data-stat": "fg3"}).text
        player["3PA"] = row.find("td", {"data-stat": "fg3a"}).text
        player["3P%"] = row.find("td", {"data-stat": "fg3_pct"}).text
        player["FT"] = row.find("td", {"data-stat": "ft"}).text
        player["FTA"] = row.find("td", {"data-stat": "fta"}).text
        player["FT%"] = row.find("td", {"data-stat": "ft_pct"}).text
        player["ORB"] = row.find("td", {"data-stat": "orb"}).text
        player["DRB"] = row.find("td", {"data-stat": "drb"}).text
        player["TRB"] = row.find("td", {"data-stat": "trb"}).text
        player["AST"] = row.find("td", {"data-stat": "ast"}).text
        player["STL"] = row.find("td", {"data-stat": "stl"}).text
        player["BLK"] = row.find("td", {"data-stat": "blk"}).text
        player["TOV"] = row.find("td", {"data-stat": "tov"}).text
        player["PF"] = row.find("td", {"data-stat": "pf"}).text
        player["PTS"] = row.find("td", {"data-stat": "pts"}).text
        player["GmSc"] = row.find("td", {"data-stat": "game_score"}).text
        player["+/-"] = row.find("td", {"data-stat": "plus_minus"}).text

        player_gamelog.append(player)

    df = pd.DataFrame(player_gamelog)
    df.set_index("Rk", inplace=True)
    return df
"""
