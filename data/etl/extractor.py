"""Façade class for various lower level extractors"""
from etl.moviedata import MovieData
from etl.movierating import MovieRating
from etl.cinemalist import CinemaList
from etl.movieshowing import MovieShowing


class Extractor:

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def extract_movie_data(movie_id):
        """given imdb_id, return the metadata of that movie from imdb"""
        data_model = MovieData(movie_id)
        data_model.build_soup(data_model.get_html_content())
        data_model.extract_process()
        return data_model.get_movie_data()

    @staticmethod
    def extract_movie_rating(movie_id):
        """given imdb_id, return a list of dictionaries that contain respective
        rating and votes from each ratings sources
        """
        data_model = MovieRating(movie_id)
        return data_model.get_movie_ratings()

    @staticmethod
    def extract_cinema_list():
        """return a list of dictionaries contains all the cinema names and its
        respective urls
        """
        data_model = CinemaList()
        final_list = []
        final_list.extend(data_model.get_golden_village_cinema_list())
        final_list.extend(data_model.get_cathay_cinema_list())
        final_list.extend(data_model.get_shaw_brother_cinema_list())
        return final_list

    @staticmethod
    def extract_cinema_schedule(cinema):
        data_model = MovieShowing(cinema)
        data_model.generic_cinema_extractor()
        return







