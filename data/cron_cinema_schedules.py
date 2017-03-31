from public_data import controller
from apscheduler.schedulers.blocking import BlockingScheduler

import logging


def update_cinema_list(con):
    con.update_cinema_list()


def run(connection):
    scheduler = BlockingScheduler()

    # cron for cinema schedule, run at 0:00 everyday
    scheduler.add_job(connection.update_cinema_schedule, trigger='cron', hour=18, minute=5, second=0)
    scheduler.start()

if __name__ == '__main__':
    con = controller.ETLController()
    logging.basicConfig(level=logging.INFO)
    update_cinema_list(con)
