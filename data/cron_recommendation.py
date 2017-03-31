from recommedation_algo.recommender import Recommender

import logging
import warnings


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")  # ignore lapack related warning
    logging.basicConfig(level=logging.INFO)
    recommender = Recommender()
    recommender.run()
