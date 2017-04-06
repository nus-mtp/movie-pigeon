import recommedation_algo.database as database
import logging


class MovieSimilarity:
    """
        this class handles operations related to the calculation
        of similarity between movies

        It will select all distinct movies from user histories,
        and calculate each one of them against every movie in time descending
        order, and stored in databases for recommendation use.
    """

    # pre-set weights for each similarity
    GENRE_WEIGHT = 0.30
    ACTOR_WEIGHT = 0.30
    DIRECTOR_WEIGHT = 0.30
    RUNTIME_WEIGHT = 0.10

    def __init__(self):
        self.db = database.DatabaseHandler()

    def calculate_similarity_table(self):
        """
        main logic for calculating similarity and
        storing the results
        :return:
        """
        logging.info("initialise similarity matrix calculation ...")
        user_history_objects = self._get_user_histories()
        movie_objects = self._get_compared_movies()
        logging.info("user history object count: " + str(len(user_history_objects)))
        logging.info("movie objects count: " + str(len(movie_objects)))

        for user_history_object in user_history_objects:
            for movie_object in movie_objects:
                first_movie_id = user_history_object['movie_id']
                second_movie_id = movie_object['movie_id']

                if first_movie_id != second_movie_id:
                    current_similarity = self._calculate_similarity(user_history_object, movie_object)
                    self.db.save_similarity(first_movie_id, second_movie_id, current_similarity)

        logging.info("current iteration complete.")

    def _get_user_histories(self):
        logging.debug("generating user histories ...")
        user_histories = self.db.get_user_history_object()
        logging.debug(str(len(user_histories)) + " movies are found.")
        return user_histories

    def _get_compared_movies(self):
        logging.debug("generating movie pool ...")
        movie_pool = self.db.get_movie_pool_object()
        logging.debug(str(len(movie_pool)) + " movies are found.")
        return movie_pool

    def _calculate_similarity(self, first_movie_object, second_movie_object):
        """
        1. get a list of existing pairs, check repetition, skip repetition
        2. calculate
        3. return
        :param first_movie_object:
        :param second_movie_object:
        :return:
        """
        genre_similarity = self._calculate_genre_similarity(first_movie_object['genre'],
                                                            second_movie_object['genre'])

        actor_similarity = self._calculate_genre_similarity(first_movie_object['actors'],
                                                            second_movie_object['actors'])

        director_similarity = self._calculate_genre_similarity(first_movie_object['director'],
                                                            second_movie_object['director'])

        runtime_similarity = self._calculate_genre_similarity(first_movie_object['runtime'],
                                                              second_movie_object['runtime'])

        return genre_similarity + actor_similarity + runtime_similarity + director_similarity

    def _calculate_genre_similarity(self, first_genre, second_genre):
        """
        calculate similarity of genres between two movies
        :return: float
        """
        targets = self._tokenize_string(first_genre)
        sources = self._tokenize_string(second_genre)
        average_count = (len(targets) + len(sources)) / 2
        similarity = len(set(sources).intersection(targets)) / average_count
        return self.GENRE_WEIGHT * similarity

    def _calculate_actor_similarity(self, first_actor, second_actor):
        """
        calculate similarity of actors between two movies
        :return:
        """
        targets = self._tokenize_string(first_actor)
        sources = self._tokenize_string(second_actor)
        average_count = (len(targets) + len(sources)) / 2
        similarity = len(set(sources).intersection(targets)) / average_count
        return self.ACTOR_WEIGHT * similarity

    def _calculate_director_similarity(self, first_director, second_director):
        """
        calculate similarity of actors between two movies
        :return:
        """
        targets = self._tokenize_string(first_director)
        sources = self._tokenize_string(second_director)
        average_count = (len(targets) + len(sources)) / 2
        similarity = len(set(sources).intersection(targets)) / average_count
        return self.DIRECTOR_WEIGHT * similarity

    def _calculate_runtime_similarity(self, first_runtime, second_runtime):
        """
        calculate similarity of runtime between two movies
        based on the difference in runtime as a percentage
        of the source movie
        :return: float
        """
        target_runtime = int(first_runtime)
        source_runtime = int(second_runtime)
        difference = abs(target_runtime - source_runtime)
        similarity = 1 - (difference / source_runtime)
        return self.RUNTIME_WEIGHT * similarity

    @staticmethod
    def _tokenize_string(genre):
        tokens = genre.split(",")
        return [token.strip() for token in tokens]


