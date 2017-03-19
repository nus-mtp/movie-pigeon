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
        possible_imdb_list = self._get_search_results(title)

        for movie in possible_imdb_list:
            movie_id, movie_title = movie
            titles, additional_info = self._parse_search_results(movie_title)

            if not self._is_recent(additional_info):
                continue

            if not self._is_correct_type(additional_info):
                continue

            possible_result.append(movie_id)

        # use the first based on imdb
        try:
            imdb_id = possible_result[0]
        except IndexError:
            return None

        return imdb_id

    @staticmethod
    def _is_recent(additional_info):
        """
        check whether a search result is recent (in last, this or next year)
        :param additional_info:
        :return:
        """
        current_year = datetime.now().strftime("%Y")
        last_year = str(int(current_year) - 1)
        next_year = str(int(current_year) + 1)
        return any(year in additional_info for year in [current_year, last_year, next_year])

    @staticmethod
    def _is_correct_type(additional_info):
        """
        check whether a search result is of correct type
        :param additional_info:
        :return:
        """
        for item in additional_info:
            if "Short" in item or "TV" in item:
                return False
        return True

    def _get_search_results(self, title):
        """
        return a list of possible imdb id in string format
        :param title: string
        :return: list
        """
        search_text = self._parse_search_text(title)

        # find exact results
        exact_url = self._build_exact_search_url(search_text)
        self.driver.get(exact_url)
        elements = self.driver.find_elements_by_class_name("findResult")
        possible_list = self._get_possible_results(elements)

        # if no exact result find
        if len(possible_list) == 0:
            fuzzy_url = self._build_fuzzy_search_url(search_text)
            self.driver.get(fuzzy_url)
            elements = self.driver.find_elements_by_class_name("findResult")
            possible_list = self._get_possible_results(elements)

        return possible_list[:3]  # return top 3

    @staticmethod
    def _get_possible_results(elements):
        """
        given html web elements of a imdb search query,
        return all the results in list format
        :param elements:
        :return:
        """
        possible_list = []

        for element in elements:
            td = element.find_element_by_class_name("result_text")
            current_imdb = td.find_element_by_css_selector("a").get_attribute("href").split("/")[4]
            current_text = td.text.strip()
            possible_list.append((current_imdb, current_text))

        return possible_list

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
        return text.strip()

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

        segments = text.split("aka")  # in case of multiple names
        segments = [segment.strip() for segment in segments]  # remove extra white space

        for segment in segments:  # for each name entity
            first_bracket_index = segment.find("(")

            # title list
            title_found = segment[:first_bracket_index].strip().replace("\"", "")
            title_list.append(title_found)

            # info list
            tags = segment[first_bracket_index:].split(")")[:-1]  # split by )
            tags = [info.replace("(", "").strip() for info in tags]  # remove ( and trim
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
