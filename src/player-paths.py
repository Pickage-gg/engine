"""
Generate player URIs as a dict.
"""

import requests
from bs4 import BeautifulSoup



def get_dict(letters):
    """
    Takes a string of letters to get player names of.

    Returns a dict of player names like 'letter' : 'list of names'
    """

    _dict = {}

    for _ in (letters):
        _url = f"https://www.basketball-reference.com/players/{_}/"
        _html = (requests.get(_url)).text
        _parser_obj = BeautifulSoup(_html, "html.parser")

        _dict[f"{_}"] = [(h.find("a", href=True)).get("href") for s in _parser_obj.findAll("tr") for h in s.findAll("strong")]

    return _dict
