"""handles all interactions with database"""
import logging
import time
import psycopg2
import utils
import config


class DatabaseHandler:

    def __init__(self):
        self.cursor, self.conn = config.database_connection()

    def get_user_ratings(self, user_id):
        self.cursor.execute("SELECT movie_id, score FROM user_ratings WHERE user_id=%s", (user_id, ))
        return self.cursor.fetchall()

    def get_public_rating(self, movie_id):
        self.cursor.execute("SELECT * FROM public_ratings WHERE movie_id=%s", (movie_id, ))
        return self.cursor.fetchall()

    def get_movie_data_by_year(self, year):
        self.cursor.execute("SELECT movie_id, rated, plot, actors, language, genre, runtime, director "
                            "FROM movies WHERE production_year=%s", (year, ))
        return self.cursor.fetchall()

    def get_movie_data_by_id(self, movie_id):
        self.cursor.execute("SELECT movie_id, rated, plot, actors, language, genre, runtime, director "
                            "FROM movies WHERE movie_id=%s", (movie_id, ))
        return self.cursor.fetchone()

    def load_weights(self, weights, user_id):
        source_id = 1
        for weight in weights:
            self.cursor.execute(
                "INSERT INTO scales (user_id, source_id, weight) "
                "VALUES (%s, %s, %s) "
                "ON CONFLICT (user_id, source_id)"
                "DO UPDATE SET weight=%s "
                "WHERE scales.user_id=%s AND scales.source_id=%s",
                (
                    user_id, str(source_id), weight,
                    weight, user_id, str(source_id)
                )
            )
            source_id += 1
        self.conn.commit()