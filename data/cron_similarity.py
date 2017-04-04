from recommedation_algo import similarity
from apscheduler.schedulers.blocking import BlockingScheduler

import logging


def run():
    scheduler = BlockingScheduler()
    ms = similarity.MovieSimilarity()

    # cron for similarity matrix, run at interval of 5 mins
    scheduler.add_job(ms.calculate_similarity_table, trigger='interval', minutes=1)
    scheduler.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
