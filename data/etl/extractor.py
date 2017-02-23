from etl.moviedata import MovieData
from etl.movierating import MovieRating
from etl.cinemalist import CinemaList

class Extractor:

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

    def __init__(self, logger):
        self.logger = logger

    # ==========
    #   data
    # ==========
    @staticmethod
    def extract_movie_data(movie_id):
        """
        given imdb_id, return the metadata of that movie from imdb
        :param movie_id:
        :return: rating and votes in STRING format or False if it is a bad request
        """
        data_model = MovieData(movie_id)
        data_model.build_soup(data_model.get_html_content())
        data_model.extract_process()
        return data_model.get_movie_data()

    # ==========
    #   rating
    # ==========
    @staticmethod
    def extract_movie_rating(movie_id):
        """
        given imdb_id, return a list of dictionaries that contain respective rating and votes from
        each ratings sources
        :param movie_id:
        :return:
        """
        data_model = MovieRating(movie_id)
        return data_model.get_movie_ratings()

    # ===========
    #   showing
    # ===========
    @staticmethod
    def extract_cinema_list():
        """return a list of dictionaries contains all the cinema names annd its respective urls"""
        data_model = CinemaList()
        final_list = []
        final_list.extend(data_model.get_golden_village_cinema_list())
        final_list.extend(data_model.get_cathay_cinema_list())
        final_list.extend(data_model.get_shaw_brother_cinema_list())
        return final_list











