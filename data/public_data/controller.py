"""
    Core objective of this etl framework. This is the highest level API.

    Each one of them will be run in backend on server, at designated
    time intervals.

    It includes four main methods in total:
        1. update movie data
        2. update movie public rating
        3. update the list of cinemas in Singapore
        4. update cinema schedule for each cinema available
"""
from cinema import CinemaList, CinemaSchedule
from movie import MovieData, MovieRating
from loader import Loader
from movie_id_matcher.matcher import MovieIDMatcher
from urllib import error
from transformer import GeneralTransformer
from http import client
from apscheduler.schedulers.blocking import BlockingScheduler

import utils
import time
import logging
import psycopg2


class ETLController:

    def __init__(self):
        self.loader = Loader()

    def run(self):
        scheduler = BlockingScheduler()
        existing_movies_id = self.loader.get_movie_id_list()

        # cron for movie data
        logging.warning("Initialise movie data retrieval process ...")
        # scheduler.add_job(self.update_movie_data, args=[336913, 1000000, 0])
        # scheduler.add_job(self.update_movie_data, args=[1172158, 2000000, 5])
        # scheduler.add_job(self.update_movie_data, args=[2033967, 3000000, 10])
        # scheduler.add_job(self.update_movie_data, args=[3052760, 4000000, 15])

        # cron for movie rating
        # logging.warning("Initialise movie rating update process ...")
        # total_length = len(existing_movies_id)
        # split = int(total_length / 4)
        # scheduler.add_job(self.update_movie_rating, args=[existing_movies_id[:split]])
        # scheduler.add_job(self.update_movie_rating, args=[existing_movies_id[split:split * 2]])
        # scheduler.add_job(self.update_movie_rating, args=[existing_movies_id[split * 2:split * 3]])
        # scheduler.add_job(self.update_movie_rating, args=[existing_movies_id[split * 3:]])

        # # cron for cinema rating
        scheduler.add_job(self.update_cinema_schedule, trigger='cron', minute='12', hour='16')

        scheduler.start()

    def update_movie_data(self, lower, upper, delay):
        """
        updates movie data from IMDb
        :param lower: integer
        :param upper: integer
        :param delay: integer
        :return: None
        """
        logging.warning("Range: " + str(lower) + " to " + str(upper) + ", starting in " + str(delay) + "s ...")

        time.sleep(delay)  # delay to avoid database transaction lock during multi-thread process
        existing_movies_id = self.loader.get_movie_id_list()

        for index in range(lower, upper):  # iterate all possible titles
            current_imdb_id = GeneralTransformer.build_imdb_id(index)

            if index % 1000 == 0:  # id monitor
                logging.warning("Currently at: " + current_imdb_id)

            if current_imdb_id in existing_movies_id:
                continue

            try:
                self._update_single_movie_data(current_imdb_id)
            except error.HTTPError:  # invalid id will cause an 404 error
                continue
            except utils.InvalidMovieTypeException:  # ignore all non-movie types
                continue
            except psycopg2.InterfaceError:  # database connection lost after a long time
                logging.error("Reestablishing database connection")
                self.loader = Loader()
                continue
            except ConnectionResetError or TimeoutError or client.IncompleteRead:
                logging.error("Connection reset by remote host, reconnecting in 5s ...")
                time.sleep(5)

                # try again
                try:
                    self._update_single_movie_data(current_imdb_id)
                except:  # skip any error
                    continue
            except Exception as e:  # unknown error
                logging.error("Unknown error occurs. Please examine.")
                logging.error(e)
                logging.error(current_imdb_id)

    def update_movie_rating(self, movie_ids):
        """
        updates movie rating for a list of movie ids
        from various websites
        :param movie_ids: list
        :return: None
        """
        logging.warning("Starting from id: " + movie_ids[0])

        for current_id in movie_ids:
            self._update_single_movie_rating(current_id)

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
        logging.warning("Initialise cinema schedule update process ...")

        logging.warning("Deleting outdated schedules ...")
        self.loader.delete_outdated_schedules()
        logging.warning("Deleting outdated schedules complete!")

        cinema_schedule_data = {}  # declare data object
        self._get_all_cinema_schedules(cinema_schedule_data)  # rearrange
        self._match_movie_titles(cinema_schedule_data)  # insert imdb id
        self.loader.load_cinema_schedule(cinema_schedule_data)  # load data

        logging.warning("Cinema schedule update process complete.")

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

            imdb_id = matcher.match_imdb_id_for_cinema_schedule(title)
            if imdb_id is None:
                logging.error("IMDb ID matched is invalid!")
                invalid_titles.append(title)
                continue

            content['imdb_id'] = imdb_id  # add in matched imdb id
            self._update_single_movie_data(imdb_id)
            logging.warning("matching successful!")

        for invalid_title in invalid_titles:
            cinema_schedule_data.pop(invalid_title)

    def _get_all_cinema_schedules(self, cinema_schedule_data):
        """
        rearrange all schedules such that the highest level of the
        dictionary is movie title
        :param cinema_schedule_data: dictionary
        :return: None
        """
        cinema_list = self.loader.get_cinema_list()
        for cinema in cinema_list:
            cinema_id, cinema_name, provider, cinema_url = cinema

            logging.warning("retrieving schedule from: " + cinema_name)

            cinema_schedule = CinemaSchedule(cinema_name, cinema_url, provider)
            current_schedules = cinema_schedule.get_cinema_schedule()

            # parse each cinema's schedule and update data object
            for movie in current_schedules:
                current_title = movie['title']
                if movie['title'] not in cinema_schedule_data:
                    cinema_schedule_data[current_title] = {}
                    current_title = cinema_schedule_data[current_title]
                    current_title['content'] = []
                else:
                    current_title = cinema_schedule_data[current_title]

                del movie['title']
                movie['cinema_id'] = cinema_id
                current_title['content'].append(movie)

            logging.warning("retrieval successful!")

    def _update_single_movie_data(self, imdb_id):
        """
        given imdb id, extract movie data and store it in database
        :param imdb_id: string
        :return: None
        """
        data_model = MovieData(imdb_id)
        current_movie_data = data_model.get_movie_data()
        self.loader.load_movie_data(current_movie_data)

    def _update_single_movie_rating(self, current_id):
        """
        given imdb id, extract movie ratings from various sources and
        store them in database
        :param current_id: string
        :return: None
        """
        data_model = MovieRating(current_id)
        movie_rating = data_model.get_movie_ratings()
        self.loader.load_movie_rating(movie_rating)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    controller = ETLController()
    controller.run()

