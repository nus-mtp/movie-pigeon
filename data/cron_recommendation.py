from recommedation_algo.recommender import Recommender
from apscheduler.schedulers.blocking import BlockingScheduler

import logging
import warnings


def run():
    scheduler = BlockingScheduler()
    recommender = Recommender()

    # cron for cinema schedule, run at 0:00 everyday
    scheduler.add_job(recommender.update_user_recommendations,
                      trigger='interval', seconds=30)
    scheduler.start()


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")  # ignore lapack related warning
    logging.basicConfig(level=logging.INFO)
    run()
