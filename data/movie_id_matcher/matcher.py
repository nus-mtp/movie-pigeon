"""
given title and some additional information of a movie
match certain id (e.g. imdb id)
"""
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver


class MovieIDMatcher:

    _IMDB_SEARCH_URL_FORMAT = "http://www.imdb.com/find?&q={}&s=tt&ttype=ft&exact=true"

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def match_imdb_id_for_cinema_schedule(self, title):
        """return the MOST possible imdb id of the movie from all recent showing"""
        possible_result = []
        possible_imdb_list = self._extract_imdb_possible(title)

        for movie in possible_imdb_list:
            movie_id, movie_title = movie
            titles, infos = self._parse_imdb_search_text(movie_title)
            # check year
            if "2016" in infos or "2017" in infos:
                possible_result.append(movie_id)
            # check type is not tv
            if "Short" is not infos and "TV" is not infos:
                possible_result.append(movie_id)

        # use the first
        try:
            imdb_id = possible_result[0]
        except IndexError:
            return None
        return imdb_id

    def _extract_imdb_possible(self, title):
        """return a list of possible imdb id in string format"""
        if " :" in title:
            title = title.replace(" :", ":")
        possible_list = []
        search_query = self._imdb_search_query_builder(title)
        url = self._IMDB_SEARCH_URL_FORMAT.format(search_query)
        self.driver.get(url)
        elements = self.driver.find_elements_by_class_name("findResult")
        for element in elements:
            td = element.find_element_by_class_name("result_text")
            current_imdb = td.find_element_by_css_selector("a").get_attribute("href").split("/")[4]
            current_text = td.text.strip()
            possible_list.append((current_imdb, current_text))

        return possible_list[:3]

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
            tags = segment[first_bracket_index:].split(")")[:-1]
            tags = [info.replace("(", "").strip() for info in tags]
            info_list.extend(tags)
        return title_list, info_list

    @staticmethod
    def _build_soup(url):
        soup = BeautifulSoup(request.urlopen(url).read().decode("utf-8"), "lxml")
        return soup

    @staticmethod
    def _imdb_search_query_builder(movie_title):
        """parse the movie title according to the query"""
        return movie_title.lower()
