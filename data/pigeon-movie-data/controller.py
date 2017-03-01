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
from cinema import CinemaList
from loader import Loader


class ETLController:

    def __init__(self):
        # basic class
        self.loader = Loader()

        self.cinema_list_object = CinemaList()

    def update_cinema_list(self):
        """update cinema list from various theatres websites"""
        cinema_list = self.cinema_list_object.get_latest_cinema_list()
        self.loader.load_cinema_list(cinema_list)

if __name__ == '__main__':
    controller = ETLController()
    controller.update_cinema_list()

