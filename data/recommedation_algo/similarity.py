import db_handler


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

        self.db = db_handler.DatabaseHandler()
        self.target_data = self.db.get_movie_data_by_id(self.target)
        self.source_data = self.db.get_movie_data_by_id(self.source)

    def get_similarity(self):
        # assume weight
        pass

    def calculate_plot_similarity(self):
        pass

    def calculate_genre_similarity(self):
        pass

    def calculate_actor_similarity(self):
        pass

    def calculate_runtime_similarity(self):
        pass

if __name__ == '__main__':
    ms = MovieSimilarity("tt3731562", "tt0360717")

