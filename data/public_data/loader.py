"""handles all interactions with database"""
import logging
import time
import psycopg2
import utils
import config


class Loader:

    def __init__(self):
        self.cursor, self.conn = config.database_connection()

    # ========
    #   LOAD
    # ========
    def load_movie_data(self, movie_data):
        """
        load movie data into database, if movie_id exists, it will update accordingly
        :param movie_data: dictionary
        :return: None
        """
        if movie_data['type'] != "movie":  # does not store any non movie content
            return

        self.cursor.execute(
            "INSERT INTO movies (movie_id, title, production_year, rated, plot, actors, "
            "language, country, runtime, poster_url, genre, director, released, type) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (movie_id) "
            "DO UPDATE SET (title, production_year, rated, plot, actors, "
            "language, country, runtime, poster_url, genre, director, released, type) = "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            "WHERE movies.movie_id=%s",
            (
                movie_data['movie_id'], movie_data['title'], movie_data['production_year'],
                movie_data['rated'],  movie_data['plot'], movie_data['actors'], movie_data['language'],
                movie_data['country'], movie_data['runtime'], movie_data['poster_url'],
                movie_data['genre'], movie_data['director'], movie_data['released'],
                movie_data['type'],
                movie_data['title'], movie_data['production_year'],
                movie_data['rated'], movie_data['plot'], movie_data['actors'], movie_data['language'],
                movie_data['country'], movie_data['runtime'], movie_data['poster_url'],
                movie_data['genre'], movie_data['director'], movie_data['released'],
                movie_data['type'],
                movie_data['movie_id']
            )
        )
        self.conn.commit()

    def load_movie_rating(self, movie_ratings):
        for movie_rating in movie_ratings:
            self.cursor.execute(
                "INSERT INTO public_ratings (vote, score, movie_id, source_id) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (movie_id, source_id) "
                "DO UPDATE SET (vote, score) = (%s, %s) "
                "WHERE public_ratings.movie_id=%s AND public_ratings.source_id=%s",
                (
                    movie_rating['votes'], movie_rating['score'], movie_rating['movie_id'],
                    movie_rating['source_id'], movie_rating['votes'], movie_rating['score'],
                    movie_rating['movie_id'], movie_rating['source_id']
                )
            )
        self.conn.commit()

    def load_cinema_list(self, cinema_list):
        for cinema in cinema_list:
            self.cursor.execute(
                "INSERT INTO cinemas (cinema_name, url, provider, location_x, location_y) VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (cinema_name) "
                "DO UPDATE SET (url, provider, location_x, location_y) = (%s, %s, %s, %s)"
                "WHERE cinemas.cinema_name=%s",
                (
                    cinema['cinema_name'], cinema['url'], cinema['provider'], str(cinema['location_x']),
                    str(cinema['location_y']),
                    cinema['url'], cinema['provider'], str(cinema['location_x']), str(cinema['location_y']),
                    cinema['cinema_name']
                )
            )
            self.conn.commit()

    def load_cinema_schedule(self, cinema_schedule):
        for title, cinema_content in cinema_schedule.items():
            movie_id = cinema_content['imdb_id']
            for cinema in cinema_content['content']:
                cinema_id = cinema['cinema_id']
                additional_info = cinema['additional_info']
                schedule_list = cinema['schedule']
                for timing in schedule_list:
                    self.cursor.execute(
                        "INSERT INTO showings (cinema_id, movie_id, type, schedule) "
                        "VALUES (%s, %s, %s, %s) "
                        "ON CONFLICT (cinema_id, movie_id, type, schedule) "
                        "DO UPDATE SET (cinema_id, movie_id, type, schedule) = (%s, %s, %s, %s) "
                        "WHERE showings.cinema_id=%s AND showings.movie_id=%s "
                        "AND showings.type=%s",
                        (
                            cinema_id, movie_id, additional_info, timing,
                            cinema_id, movie_id, additional_info, timing,
                            cinema_id, movie_id, additional_info
                        )
                    )
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

    def get_cinema_list(self):
        self.cursor.execute("SELECT cinema_id, cinema_name, provider, url FROM cinemas")
        data_object = self.cursor.fetchall()
        return data_object

    def get_movie_id_list_without_rating(self):
        self.cursor.execute("SELECT movie_id FROM movies WHERE movie_id NOT IN (SELECT movie_id FROM public_ratings)")
        data_object = self.cursor.fetchall()
        id_list = []
        for item in data_object:
            id_list.append(item[0])
        return id_list

    def get_cinema_id_from_name(self, cinema_name):
        self.cursor.execute("SELECT cinema_id FROM cinemas WHERE cinema_name=%s", (cinema_name, ))
        return self.cursor.fetchone()[0]

    # delete
    def delete_outdated_schedules(self):
        """
        delete all outdated movies
        :return: None
        """
        self.cursor.execute("DELETE FROM showings WHERE schedule < now() + interval '1 hour' * 8;")
        self.conn.commit()
