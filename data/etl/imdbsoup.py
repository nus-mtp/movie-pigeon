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
        :return: title in string, production year in integer or None
        """
        title_wrapper = self.soup.find("h1").text.split("\xa0")
        self.title = title_wrapper[0]
        self.production_year = title_wrapper[1].replace("(", "").replace(")", "").replace(" ", "")
        if self.production_year == "":
            return self.title, None
        return self.title, int(self.production_year)

    def extract_poster(self):
        """
        return the url of poster of one movie
        :return:
        """
        poster = self.soup.find("div", {"class": "poster"})
        try:
            self.poster_url = poster.find("img")['src']
        except AttributeError:
            self.poster_url = None
        return self.poster_url

    def extract_credits(self):
        """
        return the directors and actors of the movie. If there is more than
        one director or actor, it will display a string with multiple tokens,
        separated by comma
        :return: credits info in string format or None
        """
        credits_text = self.soup.find_all("div", {"class": "credit_summary_item"})
        for item in credits_text:
            current_text = item.text
            if "Directors:" in current_text:
                self.director = current_text.replace("Directors:", "").split("|")[0].replace("\n", "").\
                    replace("  ", "").strip()
            elif "Director:" in current_text:
                self.director = current_text.replace("Director:", "").strip()
            elif "Stars" in current_text:
                self.actors = current_text.replace("Stars:", "").split("|")[0].replace("\n", "").\
                    replace("  ", "").strip()
            elif "Star" in current_text:
                self.actors = current_text.replace("Star:", "").strip()
        return self.actors, self.director



