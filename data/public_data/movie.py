from bs4 import BeautifulSoup
from urllib import request

import html
import public_data.utils as utils


class MovieData:
    """
    This class handles all operations related to movie data
    extraction
    """
    # statics

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
        """
        It takes an imdb_id to instantiate a MovieData object, upon instantiation,
        it will get relevant html content and store as instance attribute
        :param imdb_id:
        """
        self.imdb_id = imdb_id
        if imdb_id != "mock-id":  # special identifier for test cases. i.e. normal instantiation
            self._build_soup(self._get_html_content())
            self._extract_process()

    def get_movie_data(self):
        """
        return a dict that contains all data to extractor
        :return: dictionary of data in various type
        """
        movie_data = utils.get_movie_data_dict(self.actors, self.country, self.director, self.genre, self.imdb_id,
                                               None, self.plot, self.poster_url, self.production_year, self.rated,
                                               self.released, self.runtime, self.title, self.type)
        return movie_data

    def _extract_process(self):
        """
        main logic for extraction of imdb data
        :return:
        """
        self._extract_subtext()
        self._extract_release()
        self._extract_rated()
        self._extract_genre()
        self._extract_release()
        self._extract_runtime()
        self._extract_title_and_year()
        self._extract_poster()
        self._extract_credits()
        self._extract_plot()

    def _get_html_content(self):
        """
        get html source based on imdb_id
        :return: string
        """
        url = utils.UrlFormatter.IMDB_URL_FORMAT.value.format(self.imdb_id)
        request_result = html.unescape(request.urlopen(url).read().decode("utf-8"))
        return request_result

    def _build_soup(self, request_result):
        """
        build soup based on html content in string format
        :param request_result:
        :return:
        """
        self.soup = BeautifulSoup(request_result, "lxml")  # soup builder

    def _build_soup_for_test(self, html_file_io_wrapper):
        self.soup = BeautifulSoup(html_file_io_wrapper, "lxml")

    def _extract_title_and_year(self):
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

    def _extract_poster(self):
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

    def _extract_credits(self):
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

    def _extract_plot(self):
        """
        return the plot of one movie
        :return: plot in string format or None
        """
        try:
            self.plot = self.soup.find("div", {"class": "summary_text"}).text.replace("\n", "").strip().split("    ")[0]
        except AttributeError:
            self.plot = None

        if "Add a Plot" in self.plot:
            self.plot = None
        return self.plot

    def _extract_subtext(self):
        """
        retrieve the subtext tag for other extraction nodes
        :return:
        """
        self.subtext = self.soup.find("div", {"class": "subtext"})

    def _extract_rated(self):
        """
        return the rating of a movie
        :return:
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
        :return:
        """
        self.type = 'movie'  # default movie type
        anchors = self.subtext.find_all("a")
        for anchor in anchors:
            if anchor.has_attr('title'):
                release_text = anchor.text
                if "Episode aired" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "TV Series" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "TV Episode" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "TV Special" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "Video Game" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "Video game released" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "Video" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "TV Mini-Series" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "TV Movie" in release_text:
                    raise utils.InvalidMovieTypeException
                elif "TV Short" in release_text:
                    raise utils.InvalidMovieTypeException
                release_text = release_text.replace("\n", "").strip()
                self.released, self.country = utils.split_release_and_country_imdb(release_text)
                self.released = utils.transform_date_imdb(self.released)
        return self.released, self.country, self.type

    def _extract_genre(self):
        """
        parse the html content and return the genre of the movie
        :return:
        """
        genre_list = []
        spans = self.subtext.find_all("span", {"class": "itemprop"})
        for span in spans:
            genre_list.append(span.text)
        if len(genre_list) > 0:
            self.genre = ", ".join(genre_list)
        return self.genre

    def _extract_runtime(self):
        """
        parse the html content and return the runtime of the movie
        :return:
        """
        time_tag = self.subtext.find("time")
        try:
            time_text = time_tag['datetime']
            self.runtime = int(time_text.replace("PT", "").replace("M", "").replace(",", ""))
        except TypeError:
            return None
        return self.runtime


class MovieRating:

    trakt_header = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }

    wemakesites_api_key = "5a7e0693-af96-4d43-89a3-dc8ca00cf355"

    imdb_url_format = "http://www.imdb.com/title/{}/"

    # omdb setup
    omdb_plot_option = "full"  # attribute for omdb

    omdb_content_type = "json"  # return type for omdb requests

    # douban
    douban_url_format = "https://movie.douban.com/subject_search?search_text={}"
    metacritic_url_format = "http://www.metacritic.com/search/movie/{}/results"

    def __init__(self, movie_id):
        self.movie_id = movie_id

    def get_movie_ratings(self):
        movie_ratings = []

        rating, votes = self.extract_trakt_rating()
        movie_ratings.append(utils.get_movie_rating_dict(rating, votes, self.movie_id, 'Trakt'))

        rating, votes = self.extract_imdb_rating()
        movie_ratings.append(utils.get_movie_rating_dict(rating, votes, self.movie_id, 'IMDb'))

        rating, votes = self.extract_douban_rating()
        movie_ratings.append(utils.get_movie_rating_dict(rating, votes, self.movie_id, 'Douban'))
        return movie_ratings

    def extract_trakt_rating(self):
        """
        given imdb_id, return the current rating and total number of votes of this movie in trakt.tv database
        :param movie_id:
        :return: rating and votes in STRING format
        """
        request_result = request.Request('https://api.trakt.tv/movies/{}/ratings'.format(self.movie_id),
                                          headers=self.trakt_header)
        try:
            json_result = json.loads(request.urlopen(request_result).read().decode("utf-8"))
        except error.HTTPError:
            return None, None

        return str(json_result['rating']), str(json_result['votes'])

    def extract_imdb_rating(self):
        """
        given imdb_id, return the current rating and total number of votes of this movie in imdb database
        :param movie_id:
        :return: rating and votes in STRING format
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

    def extract_douban_rating(self):
        """
        given imdb_id, return the current rating and total number of votes of this movie in douban database
        :param movie_id:
        :return: rating and votes in STRING format
        """
        url = self.douban_url_format.format(self.movie_id)
        request_result = request.urlopen(url).read()
        soup = BeautifulSoup(request_result, "lxml")

        try:
            rating = soup.find("span", {'class': 'rating_nums'}).text
            votes = soup.find("span", {'class': 'pl'}).text.replace("人评价","")[1: -1].replace(",", "")  # remove parenthesis and words
        except AttributeError:
            return None, None

        return rating, votes

    # def extract_metacritic_rating(self, imdb_id, search_string, director, release_date):
    #     # bad request, on hold, need to use selenium
    #     url = self.metacritic_url_format.format(html.escape(search_string))
    #     call_result = request.urlopen(url).read()
    #     soup = BeautifulSoup(call_result, "lxml")
    #     results = soup.find('li', {'class': 'result'})
    #     print(results)
    #     pass
    #
    # def extract_rotten_tomatoes_rating(self, imdb_id):
    #     pass
    #
    # def extract_letterboxd_rating(self, movie_id):
    #     pass

