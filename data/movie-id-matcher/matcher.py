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

    _IMDB_SEARCH_URL_FORMAT = "http://www.imdb.com/find?&q={}"

    def __init__(self, title):
        self.title = title

    def match_imdb_id(self):
        """return the MOST possible imdb id of the movie from all recent showing"""
        # extract possible list
        # conditional checks
        # return imdb id
        pass

    def extract_imdb_possible(self):
        """return a list of possible imdb id in string format"""
        possible_list = []
        search_query = self._imdb_search_query_builder(self.title)
        url = self._IMDB_SEARCH_URL_FORMAT.format(search_query)
        soup = self._build_soup(url)
        elements = soup.find_all("tr", {"class": "findResult"})
        for element in elements:
            td = element.find("td", {"class": "result_text"})
            # imdb id
            current_imdb = td.find("a")['href'].split("/")[2]
            current_text = td.text.strip()

            if "tt" in current_imdb:  # simple check

                possible_list.append((current_imdb, current_text))
        return possible_list[:3]  # first 3 options

    @staticmethod
    def _build_soup(url):
        soup = BeautifulSoup(request.urlopen(url).read().decode("utf-8"), "lxml")
        return soup

    @staticmethod
    def _imdb_search_query_builder(movie_title):
        """parse the movie title according to the query"""
        return movie_title.lower()
