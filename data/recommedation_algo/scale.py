"""
    Using multi-linear regression to calculate the weight of each rating
    source for one user
"""
from sklearn import linear_model
from database import DatabaseHandler
from data.public_data.controller import ETLController


class UserScale:

    DEFAULT_WEIGHT = 1 / 3

    def __init__(self, user_id):
        self.user_id = user_id
        self.db = DatabaseHandler()
        self.controller = ETLController()

    def get_user_weight(self):
        """
        fit public ratings and user rating to
        a linear regression model, obtain and
        return the coefficients
        :return:
        """
        user_rating_records = self.db.get_user_ratings(self.user_id)  # join public rating remove None

        if len(user_rating_records) == 0:  # no user rating / history for this user
            return self.DEFAULT_WEIGHT, self.DEFAULT_WEIGHT, self.DEFAULT_WEIGHT

        regressors = []
        responses = []
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
        return regression.coef_




