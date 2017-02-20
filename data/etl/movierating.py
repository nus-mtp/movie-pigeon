from urllib import request, error
from bs4 import BeautifulSoup

import data.utils as utils
import json


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