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
        """update latest cinema schedule from cinema list"""
        cinema_list = self.loader.get_cinema_list()
        for cinema in cinema_list:
            cinema_id, cinema_name, provider, cinema_url = cinema

            # get schedule
            cinema_schedule = CinemaSchedule(cinema_name, cinema_url, provider)
            current_schedules = cinema_schedule.extract_cinema_schedule()

            # load schedule
            self.loader.load_cinema_schedule(cinema_id, current_schedules)

if __name__ == '__main__':
    controller = ETLController()
    controller.update_cinema_schedule()

