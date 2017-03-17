"""
    Main class for recommendation operations
"""
import logging


class Recommender:

    def __init__(self, user_id):
        pass

    def run(self):
        pass

    def update_recommendations(self):
        """
        update the general recommendation list in the database
        :return:
        """
        # calculate raw score
            # get all user_rating
            # get all public rating
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
    recommender = Recommender('')

