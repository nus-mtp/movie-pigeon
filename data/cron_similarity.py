from recommedation_algo import similarity
from apscheduler.schedulers.blocking import BlockingScheduler

import logging


def run():
    ms = similarity.MovieSimilarity()
    ms.calculate_similarity_table()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
