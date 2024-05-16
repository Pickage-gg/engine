"""
Generate player URIs as a dict.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time


def get_dict(letters):
    """
    Takes a string of letters to get player names of.

    Returns a dict of player names like 'letter' : 'list of names'
    """

    _dict = {}

    for letter in letters:
        _url = f"https://www.basketball-reference.com/players/{letter}/"
        _html = (requests.get(_url)).text
        _parser_obj = BeautifulSoup(_html, "html.parser")

        player_names = [
            ((h.find("a", href=True)).get("href"))[11:-5]
            for s in _parser_obj.find_all("tr")
            for h in s.find_all("strong")
        ]

        if player_names:
            _dict[letter] = player_names
        else:
            print(f"No player names found for letter: {letter}")

        time.sleep(3.1)
    return _dict


def dict_to_json():
    """
    Saves URI dict as JSON in ../data/URI.json
    """

    dict = get_dict("abcdefghijklmnopqrstuvwxyz")
    urijson_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "URI.json")
    )

    os.makedirs(os.path.dirname(urijson_path), exist_ok=True)

    if all(map(bool, dict.values())):
        try:
            with open(urijson_path, "w") as fp:
                json.dump(dict, fp)
            print(f"Successfully wrote to {urijson_path}")

        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")
            return None
    else:
        print("The dictionary contains empty values.")
        return None


dict_to_json()
