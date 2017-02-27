"""
given title and some additional information of a movie
match certain id (e.g. imdb id)
"""
from urllib import request, error
from bs4 import BeautifulSoup
from selenium import webdriver, common
from pytz import timezone
from datetime import datetime, timedelta

import time
import html


class MovieIDMatcher:

    __IMDB_SEARCH_URL = "http://www.imdb.com/find?&q=harry+potter+and+deathly+hallows"

    def __init__(self, title, validation_info=None):
        """contructor requires movie title and an optional argument of validation info
        It should be a dictionary and it contains at most these following fields:
        {
            "director": ...
        }
        """
        self.title = title

        if validation_info is None:
            self.validation_info = None
        else:
            self.validation_info = validation_info

    def match_imdb_id(self):
        """return the MOST possible imdb id of the movie"""
        # extract possible list
        # conditional checks
        # return imdb id
        pass

    def extract_imdb_possible(self):
        """return a list of possible imdb id in string format"""
        soup = BeautifulSoup(request.urlopen(url).read().decode("utf-8"), "lxml")
        anchors = soup.find_all("a")
        for item in anchors:
            try:
                current_href = item['href']
            except KeyError:
                continue
            if "/title" in current_href:
                print(current_href)

    def match(self):
        print(self.build_search_url("Tu ying dang an"))

    def build_search_url(self, search_title):
        search_query = html.escape(search_title.lower())
        return self.imdb_search_format.format(search_query)

    def _imdb_search_query_builder(self):
        pass