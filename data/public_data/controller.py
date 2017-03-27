"""
    Core objective of this etl framework. This is the highest level API.

    Each one of them will be run in backend on server, at designated
    time intervals.

    It includes four main methods in total:
        1. update movie data
        2. update movie public rating
        3. update the list of cinemas in Singapore (manual from script only, since it will not be updated frequently)
        4. update cinema schedule for each cinema available

    AND a run() function, the only public function,
    to be called from command line.

    It includes all the scheduled time for the above four tasks
"""
from cinema import CinemaList, CinemaSchedule
from movie import MovieData, MovieRating
from loader import Loader
from movie_id_matcher.matcher import MovieIDMatcher
from urllib import error
from transformer import GeneralTransformer
from http import client

import utils
import time
import logging
import psycopg2


class ETLController:

    def __init__(self):
        self.loader = Loader()

    def update_movie_data(self, lower, upper, existing_movies_id):
        """
        updates a range of movie data from IMDb, given the
        lower and upper index of an imdb id
        :param lower: integer
        :param upper: integer
        :param existing_movies_id: list
        :return: None
        """
        logging.warning("initialise movie data retrieval process ..." + " Range: " + str(lower) + " to " + str(upper))

        for index in range(lower, upper):  # iterate all possible titles
            current_imdb_id = GeneralTransformer.build_imdb_id(index)

            if index % 1000 == 0:  # id monitor
                logging.warning("currently at: " + current_imdb_id)

            if current_imdb_id in existing_movies_id:  # skip if data exists
                continue

            try:
                self.update_single_movie_data(current_imdb_id)
            except error.HTTPError:  # invalid id will cause an 404 error
                continue
            except utils.InvalidMovieTypeException:  # ignore all non-movie types
                continue
            except psycopg2.InterfaceError:  # database connection lost after a long time
                logging.error("re-establishing database connection")
                time.sleep(5)
                self.loader = Loader()
                continue
            except ConnectionResetError or TimeoutError or client.IncompleteRead:
                logging.error("connection reset, reconnecting in 5s ...")
                time.sleep(5)
                try:
                    self.update_single_movie_data(current_imdb_id)
                except:  # skip any error in second try
                    continue

        logging.warning("movie data update process completed.")

    def update_movie_rating(self, movie_ids):
        """
        updates movie rating for a list of movie ids
        from various websites
        :param movie_ids: list
        :return:
        """
        logging.warning("initialise movie rating retrieval process ...")

        for current_imdb_id in movie_ids:
            try:
                self.update_single_movie_rating(current_imdb_id)
            except error.HTTPError:  # invalid id will cause an 404 error
                continue
            except ConnectionResetError or TimeoutError or client.IncompleteRead or error.URLError:
                logging.error("connection reset, reconnecting in 5s ...")
                time.sleep(5)
                try:
                    self.update_single_movie_data(current_imdb_id)
                except:  # skip any error in second try
                    continue

        logging.warning("Movie rating update process completed.")

    def update_cinema_list(self):
        """
        Update cinema list from various theatres websites
        :return: None
        """
        logging.warning("Initialise cinema list update process ...")

        cinema_list_object = CinemaList()
        cinema_list = cinema_list_object.get_latest_cinema_list()
        self.loader.load_cinema_list(cinema_list)

        logging.warning("Cinema list update process complete.")

    def update_cinema_schedule(self):
        """
        Update latest cinema schedule from cinema list.

        It passes an empty dictionary to each cinema schedule object,
        every iteration it will append that cinema's schedule to the
        dictionary.

        IMDb ID is obtained using MovieMatcher module in the process.


        The dictionary should be structured using title and imdb_id
        as the top level keys, follow by other data.

        {
            title: {
                "imdb_id": ...
                "content": [{
                        "cinema_id": ...
                        "schedule": [...]
                        "type": ...
                    }
                ]
            }
        }
        """
        logging.warning("initialise cinema schedule update process ...")

        logging.warning("deleting outdated schedules ...")

        self.loader.delete_outdated_schedules()

        logging.warning("deleting outdated schedules complete!")

        cinema_schedule = CinemaSchedule()
        cinema_schedule_data = {}  # declare data object

        logging.warning("retrieving and merging cathay schedules ...")
        cathay_schedule = cinema_schedule.get_cathay_schedule()
        self._merge_schedules(cinema_schedule_data, cathay_schedule)

        logging.warning("retrieving and merging golden village schedules ...")
        gv_schedule = cinema_schedule.get_gv_schedule()
        self._merge_schedules(cinema_schedule_data, gv_schedule)

        logging.warning("retrieving and merging shaw brother schedules ...")
        sb_schedule = cinema_schedule.get_sb_schedule()
        self._merge_schedules(cinema_schedule_data, sb_schedule)

        self._match_movie_titles(cinema_schedule_data)  # insert imdb id
        self.loader.load_cinema_schedule(cinema_schedule_data)  # load data

        logging.warning("cinema schedule update process complete.")

    def update_single_movie_data(self, imdb_id):
        """
        given imdb id, extract movie data and store it in database
        :param imdb_id: string
        :return: None
        """
        data_model = MovieData(imdb_id)
        data_model.extract_all()
        current_movie_data = data_model.get_movie_data()
        self.loader.load_movie_data(current_movie_data)

    def update_single_movie_rating(self, current_id):
        """
        given imdb id, extract movie ratings from various sources and
        store them in database
        :param current_id: string
        :return: None
        """
        data_model = MovieRating(current_id)
        movie_rating = data_model.get_movie_ratings()
        self.loader.load_movie_rating(movie_rating)

    # ==========
    #   helper
    # ==========
    @staticmethod
    def _merge_schedules(result, provider_schedule):
        for title, value in provider_schedule.items():
            if title in result:
                result[title].extend(value)
            else:
                result[title] = value

    def _match_movie_titles(self, cinema_schedule_data):
        """
        this process matched all movies title in the data object
        with its most probable imdb id
        :param cinema_schedule_data: dictionary
        :return: None
        """
        matcher = MovieIDMatcher()
        invalid_titles = []
        for title, content in cinema_schedule_data.items():

            logging.warning("Matching movie: " + title)

            imdb_id = matcher.match_imdb_id_from_title_recent(title)
            if imdb_id is None:
                logging.error("IMDb ID matched is invalid!")
                invalid_titles.append(title)
                continue

            cinema_schedule_data[title] = {
                'imdb_id': imdb_id,
                'content': content
            }
            self.update_single_movie_data(imdb_id)
            logging.warning("matching successful!")

        for invalid_title in invalid_titles:
            cinema_schedule_data.pop(invalid_title)


