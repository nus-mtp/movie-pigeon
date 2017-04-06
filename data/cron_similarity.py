from recommedation_algo import similarity
from apscheduler.schedulers.blocking import BlockingScheduler

import logging


def run():
    ms = similarity.MovieSimilarity()

    scheduler = BlockingScheduler()

    # cron for cinema schedule, run at 0:00 everyday
    scheduler.add_job(ms.calculate_similarity_table, trigger='interval', days=1,
                      start_date='2017-04-06 19:57:00')
    scheduler.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
