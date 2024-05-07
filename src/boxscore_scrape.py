# main
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


class game_stats:
    def get_boxscore(url, table_id):
        """
        The purpose of this function is to scrape NBA boxscore data from basketball-reference.com when given a url and html table id
        """
        r = requests.get(url)
        soup_parser = BeautifulSoup(r.content, "html.parser")
        game_boxscore_table = soup_parser.find(name="table", attrs={"id": table_id})

        team_stats = []

        for index, row in enumerate(game_boxscore_table.find_all("tr")[2:20], start=2):
            # case for the Reserves Header in table
            if row.find("tr", {"class": "thead"}):
                continue
            # case for the when player Did Not Plat
            if row.find("td", {"data-stat": "reason"}):
                continue
            player = {}
            # Case for the table footer/team totals
            if row.parent.name == "tfoot":
                player["Name"] = row.find("th", {"data-stat": "player"}).text
            else:
                player["Name"] = row.find("a").text.strip()

            player["Mins Played"] = row.find("td", {"data-stat": "mp"}).text
            player["Field Goal %"] = row.find("td", {"data-stat": "fg_pct"}).text
            player["Rebounds"] = row.find("td", {"data-stat": "trb"}).text
            player["Assists"] = row.find("td", {"data-stat": "ast"}).text
            player["Steals"] = row.find("td", {"data-stat": "stl"}).text
            player["Blocks"] = row.find("td", {"data-stat": "blk"}).text
            player["Turnovers"] = row.find("td", {"data-stat": "tov"}).text
            player["Points"] = row.find("td", {"data-stat": "pts"}).text
            team_stats.append(player)

        return pd.DataFrame(team_stats)
