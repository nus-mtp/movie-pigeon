import database
import difflib


class MovieSimilarity:
    """
        Content based recommendation algorithm
    """
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
        # assume weight
        pass

    def _calculate_genre_similarity(self):
        """
        calculate similarity of genres between two movies
        :return: float
        """
        target_genre_string = self.target_data[5]
        source_genre_string = self.source_data[5]
        target_genres = self._tokenize_genre(target_genre_string)
        source_genres = self._tokenize_genre(source_genre_string)

        average_genre_count = (len(target_genres) + len(source_genres)) / 2
        similarity = len(set(source_genres).intersection(target_genres)) / average_genre_count

        return similarity

    def _calculate_actor_similarity(self):
        target_runtime = self.target_data[3]
        source_runtime = self.source_data[3]
        target_token = target_runtime
        print(target_token)

    def _calculate_runtime_similarity(self):
        target_runtime = self.target_data[6]
        source_runtime = self.source_data[6]
        print(target_runtime, source_runtime)

    @staticmethod
    def _tokenize_genre(genre):
        tokens = genre.split(",")
        return [token.strip() for token in tokens]

if __name__ == '__main__':
    ms = MovieSimilarity("tt3731562", "tt0360717")
    ms._calculate_genre_similarity()

