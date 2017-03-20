import database


class MovieSimilarity:

    # pre-set weights for each similarity
    GENRE_WEIGHT = 0.5
    ACTOR_WEIGHT = 0.25
    RUNTIME_WEIGHT = 0.25

    def __init__(self, target, source):
        """
        construct with 2 movie ids
        :param target: string
        :param source: string
        """
        self.target = target
        self.source = source

        self.db = database.DatabaseHandler()
        self.target_data = self.db.get_movie_data_by_id(self.target)
        self.source_data = self.db.get_movie_data_by_id(self.source)

    def get_similarity(self):
        """
        calculate similarity of two movies based
        on different fields
        :return: float
        """
        genre_sim = self._calculate_genre_similarity()
        actor_sim = self._calculate_actor_similarity()
        runtime_sim = self._calculate_runtime_similarity()

        final_similarity = genre_sim * self.GENRE_WEIGHT + actor_sim * self.ACTOR_WEIGHT + runtime_sim \
                                                                                           * self.RUNTIME_WEIGHT
        return final_similarity

    def _calculate_genre_similarity(self):
        """
        calculate similarity of genres between two movies
        :return: float
        """
        similarity = self._calculate_common_separated_string_similarity(5)
        return similarity

    def _calculate_actor_similarity(self):
        """
        calculate similarity of actors between two movies
        :return:
        """
        similarity = self._calculate_common_separated_string_similarity(3)
        return similarity

    def _calculate_runtime_similarity(self):
        """
        calculate similarity of runtime between two movies
        based on the difference in runtime as a percentage
        of the source movie
        :return: float
        """
        target_runtime = int(self.target_data[6])
        source_runtime = int(self.source_data[6])
        difference = abs(target_runtime - source_runtime)
        similarity = 1 - (difference / source_runtime)
        return similarity

    def _calculate_common_separated_string_similarity(self, index):
        """
        calculate similarity for string separated by comma,
        identified by data object index
        :param index: integer
        :return: float
        """
        target_string = self.target_data[index]
        source_string = self.source_data[index]
        targets = self._tokenize_genre(target_string)
        sources = self._tokenize_genre(source_string)
        average_count = (len(targets) + len(sources)) / 2
        similarity = len(set(sources).intersection(targets)) / average_count
        return similarity

    @staticmethod
    def _tokenize_genre(genre):
        tokens = genre.split(",")
        return [token.strip() for token in tokens]

if __name__ == '__main__':
    ms = MovieSimilarity("tt0330373", "tt0295297")
    ms.get_similarity()

