"""
    Main class for recommendation operations
"""
import logging
from db_handler import DatabaseHandler
from public_data.controller import ETLController

class Recommender:

    def __init__(self, user_id):
        self.controller = ETLController()
        self.db = DatabaseHandler()
        self.user_id = user_id

    def run(self):
        pass

    def update_recommendations(self):
        """
        update the general recommendation list in the database
        :return:
        """
        # calculate raw score
        user_rating_records = self.db.get_user_ratings(self.user_id)
        for record in user_rating_records:
            current_id = record[0]
            user_rating = record[1]
            public_rating_records = self.db.get_public_rating(current_id)
            if not public_rating_records:
                self.controller.update_single_movie_rating(current_id)  # update rating
                public_rating_records = self.db.get_public_rating(current_id)

            # multi linear regression


            print(public_rating_records)
            # store weight

            break


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
