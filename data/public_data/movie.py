from bs4 import BeautifulSoup
from urllib import request, error

import public_data.utils as utils
import json


class MovieData:
    """
    This class handles all operations related to movie data
    extraction
    """
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

    def __init__(self, imdb_id, test=False):
        """
        It takes an imdb_id to instantiate a MovieData object, upon instantiation,
        it will get relevant html content and store as instance attribute
        :param imdb_id:
        """
        self.imdb_id = imdb_id

        if test:
            self.soup = utils.build_soup_from_file("test/data_movie_data/{}.html".format(imdb_id))
        else:
            self.soup = utils.build_soup_from_url(self.IMDB_URL_FORMAT.format(imdb_id))

        self._extract_subtext()

    def get_movie_data(self):
        """
        return a dict that contains all data to extractor
        :return: dictionary of data in various type
        """
        # TODO : refactor packaging under same class
        movie_data = utils.get_movie_data_dict(self.actors, self.country, self.director, self.genre, self.imdb_id,
                                               None, self.plot, self.poster_url, self.production_year, self.rated,
                                               self.released, self.runtime, self.title, self.type)
        return movie_data

    def extract_all(self):
        self._extract_release()
        self._extract_rated()
        self._extract_genre()
        self._extract_release()
        self._extract_runtime()
        self._extract_title_and_year()
        self._extract_poster()
        self._extract_credits()
        self._extract_plot()

    def _extract_title_and_year(self):
        """
        return title and production year of a movie
        :return: string or None, int or None
        """
        headers = self.soup.find_all("h1")
        for header in headers:
            try:
                if header['itemprop'] == 'name':
                    title_wrapper = header.text.split("\xa0")
                    self.title = title_wrapper[0]
                    self.production_year = title_wrapper[1].replace("(", "").replace(")", "").replace(" ", "")
                    if self.production_year == "":
                        self.production_year = None
                        return self.title, self.production_year
                    return self.title, int(self.production_year)
            except KeyError:
                continue

    def _extract_poster(self):
        """
        return the url of poster of one movie
        :return: string or None
        """
        poster = self.soup.find("div", {"class": "poster"})
        try:
            self.poster_url = poster.find("img")['src']
        except AttributeError:
            self.poster_url = None
        return self.poster_url

    def _extract_credits(self):
        """
        return the directors and actors of the movie. If there is more than
        one director or actor, it will display a string with multiple tokens,
        separated by comma
        :return: string or None, string or None
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

    def _extract_plot(self):
        """
        return the plot of one movie
        :return: string or None
        """
        try:
            self.plot = self.soup.find("div", {"class": "summary_text"}).text.replace("\n", "").strip().split("    ")[0]
        except AttributeError:
            self.plot = None

        if self.plot is not None and "Add a Plot" in self.plot:
            self.plot = None
        return self.plot

    def _extract_subtext(self):
        """
        retrieve the subtext tag for other extraction nodes
        :return: None
        """
        self.subtext = self.soup.find("div", {"class": "subtext"})

    def _extract_rated(self):
        """
        return the rating(i.e. PG, R, M) of a movie
        Not to confused with user rating
        :return: string or None
        """
        metas = self.subtext.find_all("meta")
        for meta in metas:
            if meta['itemprop'] == "contentRating":
                self.rated = meta['content']
        return self.rated

    def _extract_release(self):
        """
        parse the last token in subtext element,
        determine the release date and country
        If it is not a movie, raise an exception
        :return: datetime or None, string or None, string
        """
        self.type = 'movie'  # default movie type
        anchors = self.subtext.find_all("a")
        for anchor in anchors:
            if anchor.has_attr('title'):
                release_text = anchor.text
                if "Episode aired" in release_text or "Episode airs" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "TV Series" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "TV Episode" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "TV Special" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "Video Game" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "Video game released" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "Video" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "TV Mini-Series" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "TV Movie" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                elif "TV Short" in release_text:
                    raise utils.InvalidMovieTypeException("Invalid movie type.")
                release_text = release_text.replace("\n", "").strip()
                self.released, self.country = utils.split_release_and_country_imdb(release_text)
                self.released = utils.transform_date_imdb(self.released)
        return self.released, self.country, self.type

    def _extract_genre(self):
        """
        parse the html content and return the genre of the movie
        :return: string or None
        """
        genre_list = []
        spans = self.subtext.find_all("span", {"class": "itemprop"})
        for span in spans:
            genre_list.append(span.text)
        if len(genre_list) > 0:
            self.genre = ", ".join(genre_list)
            if 'Short' in self.genre:
                raise utils.InvalidMovieTypeException("Invalid movie type.")
        return self.genre

    def _extract_runtime(self):
        """
        parse the html content and return the runtime of the movie
        :return: int or None
        """
        time_tag = self.subtext.find("time")
        try:
            time_text = time_tag['datetime']
            self.runtime = int(time_text.replace("PT", "").replace("M", "").replace(",", ""))
        except TypeError:
            return None
        return self.runtime


class MovieRating:

    TRAKT_HEADER = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }

    imdb_url_format = "http://www.imdb.com/title/{}/"

    douban_url_format = "https://movie.douban.com/subject_search?search_text={}"

    metacritic_url_format = "http://www.metacritic.com/search/movie/{}/results"

    def __init__(self, movie_id):
        self.movie_id = movie_id

    def get_movie_ratings(self):
        """
        get a list of votes and ratings from each source
        :return: list
        """
        movie_ratings = []

        rating, votes = self._extract_trakt_rating()
        movie_ratings.append(utils.get_movie_rating_dict(rating, votes, self.movie_id, 'Trakt'))

        rating, votes = self._extract_imdb_rating()
        movie_ratings.append(utils.get_movie_rating_dict(rating, votes, self.movie_id, 'IMDb'))

        rating, votes = self._extract_douban_rating()
        movie_ratings.append(utils.get_movie_rating_dict(rating, votes, self.movie_id, 'Douban'))
        return movie_ratings

    def _extract_trakt_rating(self):
        """
        given imdb_id, return the current rating and total number of votes of this movie in trakt.tv database
        :return: string or None, string or None
        """
        request_result = request.Request('https://api.trakt.tv/movies/{}/ratings'.format(self.movie_id),
                                         headers=self.TRAKT_HEADER)
        try:
            json_result = json.loads(request.urlopen(request_result).read().decode("utf-8"))
        except error.HTTPError:
            return None, None

        return str(json_result['rating']), str(json_result['votes'])

    def _extract_imdb_rating(self):
        """
        given imdb_id, return the current rating and total number of votes of this movie in imdb database
        :return: string or None, string or None
        """
        url = self.imdb_url_format.format(self.movie_id)
        request_result = request.urlopen(url).read()
        soup = BeautifulSoup(request_result, "lxml")
        div = soup.find('div', {'class': 'ratingValue'})

        try:
            parse_list = div.find("strong")['title'].split(" based on ")
        except AttributeError:
            return None, None

        rating = parse_list[0]
        votes = parse_list[1].split(" ")[0].replace(",", "")
        return rating, votes

    def _extract_douban_rating(self):
        """
        given imdb_id, return the current rating and total number of votes of this movie in douban database
        :return: string or None, string or None
        """
        url = self.douban_url_format.format(self.movie_id)
        request_result = request.urlopen(url).read()
        soup = BeautifulSoup(request_result, "lxml")

        try:
            rating = soup.find("span", {'class': 'rating_nums'}).text

            # remove parenthesis and words
            votes = soup.find("span", {'class': 'pl'}).text.replace("人评价","")[1: -1].replace(",", "")
        except AttributeError:
            return None, None

        return rating, votes

