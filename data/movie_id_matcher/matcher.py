"""
    given title and some additional information of a movie
    match certain id (e.g. imdb id)
"""
from selenium import webdriver
from datetime import datetime


class MovieIDMatcher:

    IMDB_SEARCH_URL_FORMAT_EXACT = "http://www.imdb.com/find?&q={}&s=tt&ttype=ft&exact=true"

    IMDB_SEARCH_URL_FORMAT_FUZZY = "http://www.imdb.com/find?q={}&s=tt&ref_=fn_tt"

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def match_imdb_id_from_title_recent(self, title):
        """
        return the MOST possible imdb id of the movie,
        usage for RECENT showing movies only!
        :param title: string
        :return: string
        """
        possible_result = []
        possible_imdb_list = self._extract_imdb_possible(title)

        for movie in possible_imdb_list:
            movie_id, movie_title = movie
            titles, infos = self._parse_search_results(movie_title)

            # check year
            current_year = datetime.now().strftime("%Y")
            last_year = str(int(current_year) - 1)
            next_year = str(int(current_year) + 1)

            if current_year in infos or next_year in infos or last_year in infos:
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
        """
        return a list of possible imdb id in string format
        :param title: string
        :return: list
        """
        possible_list = []

        search_text = self._parse_search_text(title)

        self.driver.get(url)

        elements = self.driver.find_elements_by_class_name("findResult")
        for element in elements:
            td = element.find_element_by_class_name("result_text")
            current_imdb = td.find_element_by_css_selector("a").get_attribute("href").split("/")[4]
            current_text = td.text.strip()
            possible_list.append((current_imdb, current_text))

        if len(possible_list) == 0:
            url = self.IMDB_SEARCH_URL_FORMAT_FUZZY.format(search_query)
            self.driver.get(url)
            elements = self.driver.find_elements_by_class_name("findResult")
            for element in elements:
                td = element.find_element_by_class_name("result_text")
                current_imdb = td.find_element_by_css_selector("a").get_attribute("href").split("/")[4]
                current_text = td.text.strip()
                possible_list.append((current_imdb, current_text))

        return possible_list[:3]

    @staticmethod
    def _parse_search_text(text):
        """
        pre-processing of movie before building the URL
        parse the input title in to the required search format
        :param text: string
        :return: string
        """
        text = text.lower()  # lower letter
        text = text.replace(" :", ":")  # standardized colon
        return text

    @staticmethod
    def _parse_search_results(text):
        """
        parse out the searched text generated from imdb search
        query, two variable will be returned.
        First is a list that consists of the movie title obtained,
        possibly more than one.

        Second return is a list that contains all possible
        information stored in a bracket, such as year, type and
        other additional information

        :param text: string
        :return: list
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

    def _build_exact_search_url(self, search_text):
        """
        build the exact search url from search text
        :param search_text:
        :return:
        """
        url = self.IMDB_SEARCH_URL_FORMAT_EXACT.format(search_text)
        return url

    def _build_fuzzy_search_url(self, search_text):
        """
        build the fuzzy search url from saerch text
        :param search_text:
        :return:
        """
        url = self.IMDB_SEARCH_URL_FORMAT_FUZZY.format(search_text)
        return url
