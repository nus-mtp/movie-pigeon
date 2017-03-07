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
from movie import MovieData
from loader import Loader


class ETLController:

    def __init__(self):
        # basic class
        self.loader = Loader()

        self.cinema_list_object = CinemaList()

    def update_cinema_list(self):
        """update cinema list from various theatres websites"""
        # get list
        cinema_list = self.cinema_list_object.get_latest_cinema_list()

        # load list
        self.loader.load_cinema_list(cinema_list)

    def update_cinema_schedule(self):
        """update latest cinema schedule from cinema list
        It passes an empty dictionary to each cinema schedule object,
        every iteration it will append that cinema's schedule to the
        dictionary.

        The dictionary should be structured using title and imdb_id
        as the top level keys, follow by other data
        {
            "title": ...
            "imdb_id": ...
            "content": {
                "cinema_id": ...
                "schedule": [...]
            }
        }

        IMDb ID is obtained using MovieMatcher module
        """
        cinema_schedule_data = {}

        cinema_list = self.loader.get_cinema_list()
        for cinema in cinema_list:
            cinema_id, cinema_name, provider, cinema_url = cinema

            # get schedule
            cinema_schedule = CinemaSchedule(cinema_name, cinema_url, provider)
            current_schedules = cinema_schedule.extract_cinema_schedule()

            # parse schedules and update data

            # load data
            # self.loader.load_cinema_schedule(cinema_id, current_schedules)
            break

    def _temp(self):
        movie_list = self.loader.get_movie_id_list()
        imdb_check_list = ['tt4846340', 'tt0498381', 'tt4465564', 'tt1691916', None, 'tt3783958',
                           'tt3315342', 'tt2763304', 'tt1753383', 'tt2126235']
        for new_imdb_id in imdb_check_list:
            if new_imdb_id not in movie_list and new_imdb_id is not None:
                data_model = MovieData(new_imdb_id)
                data_model.build_soup(data_model.get_html_content())
                data_model.extract_process()
                self.loader.load_movie_data(data_model.get_movie_data())

if __name__ == '__main__':
    controller = ETLController()
    controller.update_cinema_schedule()

