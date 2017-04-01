from public_data import controller

import logging


def update_cinema_list(etl_controller):
    etl_controller.update_cinema_list()


if __name__ == '__main__':
    con = controller.ETLController()
    logging.basicConfig(level=logging.INFO)
    update_cinema_list(con)
