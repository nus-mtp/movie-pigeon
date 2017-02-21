import config
import psycopg2
import logging


class Loader:

    def __init__(self, logger):
        self.cursor, self.conn = config.database_connection()
        self.logger = logger

    # ========
    #   LOAD
    # ========
    def load_movie_data(self, movie_data):
        try:
            self.cursor.execute("INSERT INTO movies (movie_id, title, production_year, rated, plot, actors, "
                                "language, country, runtime, poster_url, genre, director, released, type) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (movie_data['movie_id'], movie_data['title'], movie_data['production_year'],
                                 movie_data['rated'],  movie_data['plot'], movie_data['actors'], movie_data['language'],
                                 movie_data['country'], movie_data['runtime'], movie_data['poster_url'],
                                 movie_data['genre'], movie_data['director'], movie_data['released'], movie_data['type']))
        except psycopg2.IntegrityError:
            logging.error("UNIQUE CONSTRAINT violated in Table: movies")

        self.conn.commit()

    def load_movie_rating(self, movie_rating):
        self.cursor.execute("INSERT INTO public_ratings (vote, score, movie_id, source_id) VALUES (%s, %s, %s, %s) "
                            "ON CONFLICT (movie_id, source_id) "
                            "DO UPDATE SET (vote, score) = (%s, %s) "
                            "WHERE public_ratings.movie_id=%s AND public_ratings.source_id=%s",
                            (movie_rating['votes'], movie_rating['score'], movie_rating['movie_id'],
                             movie_rating['source_id'], movie_rating['votes'], movie_rating['score'],
                             movie_rating['movie_id'], movie_rating['source_id']))
        self.conn.commit()

    # ========
    #   GET
    # ========
    def get_movie_id_list(self):
        self.cursor.execute("SELECT movie_id FROM movies")
        data_object = self.cursor.fetchall()
        id_list = []
        for item in data_object:
            id_list.append(item[0])
        return id_list

    def get_movie_validation_info(self, movie_id):
        self.cursor.execute("SELECT title, released, director FROM movies WHERE movie_id=%s", (movie_id, ))
        data_object = self.cursor.fetchone()
        return data_object
