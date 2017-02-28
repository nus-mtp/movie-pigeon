"""
given title and some additional information of a movie
match certain id (e.g. imdb id)
"""
from urllib import request, error
from bs4 import BeautifulSoup
from selenium import webdriver, common
from pytz import timezone
from datetime import datetime, timedelta
from difflib import SequenceMatcher

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
    def _parse_imdb_search_text(text):
        """parse out the searched text generated from imdb search
        query, two variable will be returned. First is a list that
        consists of the movie title obtained, possibly more than one.
        Second return is a list that contains all possible
        information stored in a bracket, such as year, type and
        other strange information
        :return list, list
        """
        title_list = []
        info_list = []

        segments = text.split("aka")
        segments = [segment.strip() for segment in segments]  # remove extra white space

        for segment in segments:
            first_bracket_index = segment.find("(")

            # title list
            title_found = segment[:first_bracket_index].strip().replace("\"", "")
            title_list.append(title_found)

            # info list
            infos = segment[first_bracket_index:].split(")")[:-1]
            infos = [info.replace("(", "").strip() for info in infos]
            info_list.extend(infos)
        return title_list, info_list

    @staticmethod
    def _build_soup(url):
        soup = BeautifulSoup(request.urlopen(url).read().decode("utf-8"), "lxml")
        return soup

    @staticmethod
    def _imdb_search_query_builder(movie_title):
        """parse the movie title according to the query"""
        return movie_title.lower()

    @staticmethod
    def _get_similarity(origin, searched):
        """find the string similarity between the original
        title and searched title"""
        return SequenceMatcher(None, origin, searched).ratio()

