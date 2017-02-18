"""
    data class for all imdb movies
"""
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
    subtext = None
    soup = None

    def __init__(self, imdb_id):
        self.imdb_id = imdb_id
        self.build_soup()
        self.extract_process()

    # main logic
    def build_soup(self):
        url = self.IMDB_URL_FORMAT.format(self.imdb_id)
        request_result = html.unescape(request.urlopen(url).read().decode("utf-8"))
        self.soup = BeautifulSoup(request_result, "lxml")  # soup builder

    def extract_process(self):
        self.extract_title_and_year()
        self.extract_poster()
        self.extract_credits()
        self.extract_plot()
        self.extract_subtext()
        self.extract_rated()
        self.extract_genre()
        self.extract_release()
        self.extract_runtime()

    # get
    def get_movie_data(self):
        """
        return a dict that contains all data to extractor
        :return: dictionary of data in various type
        """
        movie_data = utils.get_movie_data_dict(self.actors, self.country, self.director, self.genre, self.imdb_id,
                                               None, self.plot, self.poster_url, self.production_year, self.rated,
                                               self.released, self.runtime, self.title, self.type)
        return movie_data

    # extraction nodes
    def extract_title_and_year(self):
        """
        return title and production year of a movie
        :return: title in string, production year in integer or None
        """
        title_wrapper = self.soup.find("h1").text.split("\xa0")
        self.title = title_wrapper[0]
        self.production_year = title_wrapper[1].replace("(", "").replace(")", "").replace(" ", "")
        if self.production_year == "":
            self.production_year = None
            return self.title, self.production_year
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
                self.director = current_text.replace("Directors:", "").split("|")[0]\
                    .replace("\n", "").replace("  ", "").strip()
            elif "Director:" in current_text:
                self.director = current_text.replace("Director:", "").strip()
            elif "Stars" in current_text:
                self.actors = current_text.replace("Stars:", "").split("|")[0]\
                    .replace("\n", "").replace("  ", "").strip()
            elif "Star" in current_text:
                self.actors = current_text.replace("Star:", "").strip()
        return self.actors, self.director

    def extract_plot(self):
        """
        return the plot of one movie
        :return: plot in string format or None
        """
        self.plot = self.soup.find("div", {"class": "summary_text"}).text.replace("\n", "").strip().split("    ")[0]
        if "Add a Plot" in self.plot:
            self.plot = None
        return self.plot

    def extract_subtext(self):
        """
        retrieve the subtext tag for other extraction nodes
        :return:
        """
        self.subtext = self.soup.find("div", {"class": "subtext"})

    def extract_rated(self):
        """
        return the rating of a movie
        :return:
        """
        metas = self.subtext.find_all("meta")
        for meta in metas:
            if meta['itemprop'] == "contentRating":
                self.rated = meta['content']
        return self.rated

    def extract_release(self):
        self.type = 'movie'  # default movie type
        anchors = self.subtext.find_all("a")
        for anchor in anchors:
            if anchor.has_attr('title'):
                release_text = anchor.text
                if "Episode aired" in release_text:
                    self.type = "episode"
                    release_text = release_text.replace("Episode aired", "").replace("\n", "").strip()
                    self.released = utils.transform_date_imdb(release_text)
                elif "TV Series" in release_text:
                    self.type = "tv"
                elif "TV Movie" in release_text:
                    self.type = "tv-movie"
                    release_text = release_text.replace("TV Movie", "").replace("\n", "").strip()
                    self.released = utils.transform_date_imdb(release_text)
                else:
                    release_text = release_text.replace("\n", "").strip()
                    self.released, self.country = utils.split_release_and_country_imdb(release_text)
                    self.released = utils.transform_date_imdb(self.released)
        return self.released, self.country, self.type

    def extract_genre(self):
        genre_list = []
        spans = self.subtext.find_all("span", {"class": "itemprop"})
        for span in spans:
            genre_list.append(span.text)
        if len(genre_list) > 0:
            self.genre = ", ".join(genre_list)
        return self.genre

    def extract_runtime(self):
        time_tag = self.subtext.find("time")
        try:
            time_text = time_tag['datetime']
            self.runtime = int(time_text.replace("PT", "").replace("M", ""))
        except TypeError:
            return None
        return self.runtime
