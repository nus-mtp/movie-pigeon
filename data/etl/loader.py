import data.config as config
import psycopg2
import logging


class Loader:

    def __init__(self):
        self.cursor, self.conn = config.database_connection()

    def load_movie_data(self, movie_data):
        try:
            self.cursor.execute("INSERT INTO movies (movie_id, title, production_year, rated, plot, actors, "
                                "language, country, runtime, poster_url, genre, director, released) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (movie_data['movie_id'], movie_data['title'], movie_data['production_year'],
                                 movie_data['rated'],  movie_data['plot'], movie_data['actors'], movie_data['language'],
                                 movie_data['country'], movie_data['runtime'], movie_data['poster_url'], movie_data['genre'],
                                 movie_data['director'], movie_data['released']))
        except psycopg2.IntegrityError as e:
            print(e)
            logging.error("UNIQUE CONSTRAINT violated in Table: movies")

        self.conn.commit()
