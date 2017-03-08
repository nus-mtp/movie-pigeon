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
        self.loader = Loader()

        self.cinema_list_object = CinemaList()

    def update_movie_data(self, lower, upper, delay):
        """updates movie data from databases (potentially more than one source)
            it is a one time process, i.e. data will not be updated constantly
        """
        self.logger.info("Initialise movie data retrieval process ...")

        time.sleep(delay)  # delay to avoid conflict
        existing_movies_id = self.loader.get_movie_id_list()

        for index in range(lower, upper):  # iterate all possible titles
            imdb_id = utils.imdb_id_builder(index)

            if imdb_id in existing_movies_id:
                continue

            try:
                movie_data = self.extractor.extract_movie_data(imdb_id)
            except error.HTTPError:
                self.logger.error("Movie ID is not valid." + imdb_id)
                continue
            except Exception as e:  # need to find out the exact error type
                self.logger.error("Movie ID type is not registered." + imdb_id)
                self.logger.error(e)
                continue

            try:
                self.loader.load_movie_data(movie_data)
            except psycopg2.DataError:
                self.logger.error("Invalid insertion! Due to the subtext are partially parsed.")
                continue

        self.logger.info("Movie data update process complete.")

    def update_movie_rating(self):
        """updates movie rating from popcorn movies (may have to change to raaw implementation in the future)
        it is a continuous process and data will be updated constantly
        """
        self.logger.info("Initialise movie rating update process ...")

        # get list of existing movies
        id_list = self.loader.get_movie_id_list()

        self.logger.info("Movie rating update process complete.")

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
                data_model._build_soup(data_model._get_html_content())
                data_model.extract_process()
            except:
                print(movie_id)
            self.loader.load_movie_data(data_model.get_movie_data())

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
        final_list.extend(data_model._extract_gv_cinema_list())
        final_list.extend(data_model._extract_cathay_cinema_list())
        final_list.extend(data_model._extract_sb_cinema_list())
        return final_list

    @staticmethod
    def extract_cinema_schedule(cinema):
        data_model = MovieShowing(cinema)
        data_model.generic_cinema_extractor()
        return

if __name__ == '__main__':
    controller = ETLController()
    controller.update_cinema_schedule()

