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
from movie_id_matcher.matcher import MovieIDMatcher


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
            title: {
                "imdb_id": ...
                "content": [
                    {
                        "cinema_id": ...
                        "schedule": [...]
                        "type": ...
                    }
                ]
            }
        }

        IMDb ID is obtained using MovieMatcher module
        """
        cinema_schedule_data = {}

        # retrieve schedule
        cinema_list = self.loader.get_cinema_list()
        self._cinema_schedule_retrieve(cinema_list, cinema_schedule_data)

        # match id and check existence
        matcher = MovieIDMatcher()
        for title, content in cinema_schedule_data.items():
            imdb_id = matcher.match_imdb_id_for_cinema_schedule(title)
            content['imdb_id'] = imdb_id
            print(title, imdb_id)
            self._update_movie_data_if_not_exist(imdb_id)

        # load data
        self.loader.load_cinema_schedule(cinema_schedule_data)

    @staticmethod
    def _cinema_schedule_retrieve(cinema_list, cinema_schedule_data):
        for cinema in cinema_list:
            cinema_id, cinema_name, provider, cinema_url = cinema
            cinema_schedule = CinemaSchedule(cinema_name, cinema_url, provider)
            current_schedules = cinema_schedule.extract_cinema_schedule()

            # parse schedules and update data
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

    def _update_movie_data_if_not_exist(self, movie_id):
        movie_list = self.loader.get_movie_id_list()
        if movie_id not in movie_list:
            data_model = MovieData(movie_id)
            try:
                data_model.build_soup(data_model.get_html_content())
                data_model.extract_process()
            except:
                print(movie_id)
            self.loader.load_movie_data(data_model.get_movie_data())

if __name__ == '__main__':
    controller = ETLController()
    controller.update_cinema_schedule()

