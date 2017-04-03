from public_data import controller

import logging


def update_cinema_list(etl_controller):
    etl_controller.update_cinema_list()


def update_single_movie_data(etl_controller, movie_id):
    etl_controller.update_single_movie_data(movie_id)


if __name__ == '__main__':
    con = controller.ETLController()
    logging.basicConfig(level=logging.INFO)
    update_single_movie_data(con, "tt0926084")
