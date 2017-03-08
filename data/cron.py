from controller import ETLController
from apscheduler.schedulers.blocking import BlockingScheduler

import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scheduler = BlockingScheduler()
    controller = ETLController()
    scheduler.add_job(controller.update_movie_data, args=[1, 1000000, 0])
    scheduler.add_job(controller.update_movie_data, args=[1000000, 2000000, 5])
    scheduler.add_job(controller.update_movie_data, args=[2000000, 3000000, 10])
    scheduler.add_job(controller.update_movie_data, args=[3000000, 4000000, 15])
    scheduler.start()
