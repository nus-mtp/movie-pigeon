from bs4 import BeautifulSoup
from urllib import request, error
import html
import data.utils as utils


class IMDbSoup:

    # statics
    IMDB_URL_FORMAT = "http://www.imdb.com/title/{}/"

    title = None
    production_year = None
    rated = None
    plot = None
    actors = None
    language = None
    country = None
    genre = None
    poster_url = None
    released = None
    runtime = None
    director = None
    type = None

    def __init__(self, imdb_id):
        self.imdb_id = imdb_id
        self.soup = self.build_soup(self.imdb_id)

    def build_soup(self, test_id):
        url = self.IMDB_URL_FORMAT.format(test_id)
        request_result = html.unescape(request.urlopen(url).read().decode("utf-8"))
        soup = BeautifulSoup(request_result, "lxml")  # soup builder
        return soup

    def get_movie_data(self):
        """
        return a dict that contains all data to extractor
        :return: dictionary of data in various type
        """
        pass

    def extract_title_and_year(self):
        """
        return title and production year of a movie
        :param soup:
        :return: title in string, production year in integer or None
        """
        title_wrapper = self.soup.find("h1").text.split("\xa0")
        title = title_wrapper[0]
        production_year = title_wrapper[1].replace("(", "").replace(")", "").replace(" ", "")
        if production_year == "":
            return title, None
        return title, int(production_year)




