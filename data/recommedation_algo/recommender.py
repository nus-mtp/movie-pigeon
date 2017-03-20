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
from sklearn import linear_model
from datetime import datetime
from scale import UserScale
from similarity import MovieSimilarity


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
        result_list = []
        current_year = int(datetime.now().strftime("%Y"))

        while True:
            movie_pool = self.db.get_movie_id_by_year(current_year)
            user_pool = self.db.get_user_ratings(user_id)
            for user_rating in user_pool:
                movie_id, score = user_rating
                if score >= 8.0:  # consider as favorable movie
                    print(movie_id)
                    for target in movie_pool:
                        target_id = target[0]
                        movie_similarity = MovieSimilarity(target_id, movie_id)

                        try:
                            similarity = movie_similarity.get_similarity()
                        except ValueError:
                            continue

                        if similarity > 0.5:
                            result_list.append(target_id)
                            print(target_id)
                            break
            current_year -= 1
            break
        scale = UserScale(user_id)


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")  # ignore lapack related warning
    recommender = Recommender()
    recommender.update_single_user_recommendations('8')
