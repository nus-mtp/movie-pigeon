"""
    Main class for recommendation operations

    # calculate raw score

    # get relevant movies pool (crude criteria) (waiting to be classified)

    # for every movie in pool
        # calculate multiplier : classification (logistic regression)
        # obtain final score (expected output)
        # sort and rank
        # store in database

"""
from database import DatabaseHandler
from public_data.controller import ETLController
from datetime import datetime
from scale import UserScale
from similarity import MovieSimilarity

import logging
import warnings


class Recommender:

    def __init__(self):
        self.controller = ETLController()
        self.db = DatabaseHandler()

    def run(self):
        # for every user update scale
        # for every user generate recommendation if not enough
        pass

    def update_single_user_recommendations(self, user_id):
        # 1. get all liked movies by the users -> act as source to get recommended movies
        # 2. get a pool of similar movies based the seeds
        # 3. rank the pool using scales, recommend tops
        logging.warning("generating user movie pool ...")
        user_pool = self.db.get_user_ratings(user_id)
        user_list = []
        for user_rating in user_pool:
            movie_id, score = user_rating
            if score >= 8.0:  # consider as favorable movie
                user_list.append(movie_id)

        print(user_list)

        return

        result_list = []
        current_year = int(datetime.now().strftime("%Y"))

        scale = UserScale(user_id)



        while True:
            logging.warning("initialising movie pool selection ...")
            movie_pool = self.db.get_movie_id_by_year(current_year)
            logging.warning("size of pool:" + str(len(movie_pool)))
            for movie in movie_pool:
                movie_id = movie[0]
                logging.debug("current movie is: " + movie_id)
                public_ratings = self.db.get_public_rating(movie_id)
                if not public_ratings:
                    self.controller.update_single_movie_rating(movie_id)
                    public_ratings = self.db.get_public_rating(movie_id)

                if any(None in element for element in public_ratings):
                    logging.debug("continued")
                    continue

                imdb_rating, douban_rating, trakt_rating = public_ratings
                regressors = [imdb_rating[3], douban_rating[3], trakt_rating[3]]
                expected_score = scale.predict_user_score(regressors)[0]

                if expected_score > 7.5:
                    result_list.append(movie_id)

            current_year -= 1
            break

            # user_pool = self.db.get_user_ratings(user_id)
            # for user_rating in user_pool:
            #     movie_id, score = user_rating
            #     if score >= 8.0:  # consider as favorable movie
            #         print(movie_id)
            #         for target in movie_pool:
            #             target_id = target[0]
            #             movie_similarity = MovieSimilarity(target_id, movie_id)
            #
            #             try:
            #                 similarity = movie_similarity.get_similarity()
            #             except ValueError:
            #                 continue
            #
            #             if similarity > 0.5:
            #                 result_list.append(target_id)
            #                 print(target_id)
            #                 break


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")  # ignore lapack related warning
    logging.basicConfig(level=logging.DEBUG)
    recommender = Recommender()
    recommender.update_single_user_recommendations('8')
