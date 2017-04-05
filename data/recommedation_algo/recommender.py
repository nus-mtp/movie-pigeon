"""
    main class for recommendation operations
"""
from recommedation_algo.database import DatabaseHandler
from public_data.controller import ETLController
from datetime import datetime, timedelta
from recommedation_algo.scale import UserScale
from recommedation_algo.similarity import MovieSimilarity

import logging


class Recommender:

    USER_RATINGS_CRITERION = 8.0  # 4 stars or above can be considered a good seed for generating similar movies

    SIMILARITY_CRITERION = 0.5  # similarity index above 0.5 means roughly more than one similar feature

    RECOMMEND_CRITERION = 7.0  # user ratings are limited, a relatively lower criterion is good to generate more recom

    SIMILAR_MOVIE_POOL_SIZE = 50  # iteration wise, 50 similar movies will be selected and subjected to recommendation

    ANOMALY_CRITERION = 20

    def __init__(self):
        self.controller = ETLController()
        self.db = DatabaseHandler()

    def update_user_recommendations(self):
        """
        for each user, generate recommendations and store them
        :return: None
        """
        users = self.db.get_users()

        for user in users:
            user_id = user['id']
            logging.info("initialise recommending process for user: " + str(user_id))

            recommender_list = self._get_single_user_recommendations(user_id)

            self.db.save_recommendations(recommender_list, user_id)

            logging.info(str(len(recommender_list)) + " movies stored and recommended.")

    def _get_single_user_recommendations(self, user_id):
        """
        The recommendation logic is as follows:
            1. get all liked movies by the users,
               which will act as a selection criteria
               to get similar movies
            2. based the above criterion, select up to
               n movies from the database, order by their
               release time in descending order (recommending)
               new movies first
            3. predict the expected output using regression
               the user's historical ratings, select and recommend
               to users
        :param user_id: string
        :return: list
        """
        logging.debug("STEP 1: get user favorite movies")
        user_history = self.db.get_user_history(user_id)
        similarity_seeds = self._generate_recommend_seeds(user_history)
        logging.debug(str(len(similarity_seeds)) + " favorite movies found.")

        logging.debug("STEP 2: get similar movies")
        similar_list = self._generate_similar_movies_new(similarity_seeds)
        logging.debug(str(len(similar_list)) + " similar movies found.")

        logging.debug("STEP 3: get good movies")
        recommend_list = self._generate_recommend_list(similar_list, user_id)
        logging.debug(str(len(recommend_list)) + " potentially good movies found.")

        return recommend_list

    def _generate_similar_movies_new(self, user_list):
        """
        given a list of user's favorite movies,
        return a list of similar movies
        :param user_list: list
        :return: list
        """
        result = set()
        for seed in user_list:
            similar_movies = self.db.get_similar_movies_by_id(seed)
            result |= set([movie[0] for movie in similar_movies])

        return result

    def _generate_recommend_seeds(self, user_pool):
        """
        given user watching history, generate similar
        movies that may be recommended
        :param user_pool: list
        :return: list
        """
        user_list = []
        for user_rating in user_pool:
            movie_id, score = user_rating
            if score >= self.USER_RATINGS_CRITERION:  # consider as favorable movie
                user_list.append(movie_id)
        return user_list

    def _generate_recommend_list(self, similar_list, user_id):
        logging.debug("initialising predicting process ...")

        scale = UserScale(user_id)

        recommend_list = []

        logging.debug("size of similar list: " + str(len(similar_list)))
        for potential in similar_list:
            public_ratings = self.db.get_public_rating_dict(potential)

            if len(public_ratings) == 0:
                continue

            if len(public_ratings) == 3:
                # check rating relevancy, pick any updated date for one movie
                if public_ratings[0]['updated_at'] < datetime.now() - timedelta(days=2):
                    logging.debug("rating may be outdated, re-extracting ratings ...")
                    self.controller.update_single_movie_rating(potential)
                    public_ratings = self.db.get_public_rating_dict(potential)

                regressors = self._construct_regressors(public_ratings)
                expected_score = scale.predict_user_score(regressors)[0]

                if expected_score > self.ANOMALY_CRITERION:
                    continue

                if expected_score > self.RECOMMEND_CRITERION:
                    recommend_list.append([potential, expected_score])

        return recommend_list

    @staticmethod
    def _construct_regressors(public_ratings):
        regressors = [0, 0, 0]
        for rating in public_ratings:
            if rating['source_id'] == '1':
                regressors[0] = rating['score']
            elif rating['source_id'] == '2':
                regressors[1] = rating['score']
            elif rating['source_id'] == '3':
                regressors[2] = rating['score']
        return regressors


