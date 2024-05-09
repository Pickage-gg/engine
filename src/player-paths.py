"""
Generate player URIs as a dict.
"""

import requests
from bs4 import BeautifulSoup
import json
import os


def get_dict(letters):
    """
    Takes a string of letters to get player names of.

    Returns a dict of player names like 'letter' : 'list of names'
    """

    _dict = {}

    for _ in letters:
        _url = f"https://www.basketball-reference.com/players/{_}/"
        _html = (requests.get(_url)).text
        _parser_obj = BeautifulSoup(_html, "html.parser")

        _dict[f"{_}"] = [
            (h.find("a", href=True)).get("href")
            for s in _parser_obj.find_all("tr")
            for h in s.find_all("strong")
        ]

    return _dict


def dict_to_json():
    """
    Saves URI dict as JSON in ../data/URI.json
    """

    dict = get_dict("abcdefghijklmnopqrstuvwxyz")
    urijson_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "URI.json")
    )
    if all(map(bool, dict.values())):
        try:
            with open(urijson_path, "w") as fp:
                json.dump(dict, fp)

        except:
            return None
    else:
        return None
