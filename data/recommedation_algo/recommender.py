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
import logging
from db_handler import DatabaseHandler
from public_data.controller import ETLController
from sklearn import linear_model
from datetime import datetime


import warnings


class Recommender:

    def __init__(self, user_id):
        self.controller = ETLController()
        self.db = DatabaseHandler()
        self.user_id = user_id

    def run(self):
        # for every user update scale
        # for every user generate recommendation if not enough
        pass

    def update_user_scale(self):
        """
        update the user scale in the database
        :return:
        """
        regressors = []
        responses = []

        # calculate raw score
        user_rating_records = self.db.get_user_ratings(self.user_id)  # join public rating remove None
        for record in user_rating_records:
            current_id = record[0]

            # regressors
            public_rating_records = self.db.get_public_rating(current_id)
            if not public_rating_records:
                self.controller.update_single_movie_rating(current_id)  # update rating
                public_rating_records = self.db.get_public_rating(current_id)

            public_rating_records = sorted(public_rating_records, key=lambda x: x[1])  # sort records -> replace by sql
            current_set = []
            for regressor in public_rating_records:
                current_set.append(regressor[3])
            regressors.append(current_set)

            # response
            user_rating = record[1]
            responses.append(user_rating)

        regression = linear_model.LinearRegression()
        regression.fit(regressors, responses)
        weights = regression.coef_

        self.db.load_weights(weights, self.user_id)

    def update_user_recommendation(self):
        """
        update the recommendations in database,
        each user will be generated up to 10 recommended movies
        upon executing this function

        Consider at least 8.0 to be recommended
        :return:
        """
        result_list = []
        current_year = datetime.now().strftime("%Y")

        while True:
            if len(result_list) == 10:
                break
            user_ratings = self.db.get_user_ratings(self.user_id)

            # get training data to fit model
            # labelling
            label = []
            for user_rating in user_ratings:
                movie_id, score = user_rating
                if score >= 8.0:  # consider as favorable movie
                    label.append([movie_id, 1])
                else:
                    label.append([movie_id, 0])

            # TODO: quantify available data fields, make logistic regression model
            # TODO: after classification, iterate through movie pools by year and store recommendation

            break


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")  # ignore lapack related warning
    recommender = Recommender('8')
    recommender.update_user_recommendation()
