"""
    Main class for recommendation operations
"""
import logging
from db_handler import DatabaseHandler


class Recommender:

    def __init__(self, user_id):
        self.db = DatabaseHandler()
        self.user_id = user_id

    def run(self):
        pass

    def update_recommendations(self):
        """
        update the general recommendation list in the database
        :return:
        """
        print(self.db.get_user_ratings(self.user_id))
        # calculate raw score
            # get all user_rating
            # get all public rating (call rating extractor if necessary)
            # multi linear regression
            # store weight

        # get relevant movies pool (crude criteria) (waiting to be classified)

        # for every movie in pool
            # calculate multiplier : classification (logistic regression)
            # obtain final score (expected output)
            # sort and rank
            # store in database
        pass

if __name__ == '__main__':
    recommender = Recommender('8')
    recommender.update_recommendations()
