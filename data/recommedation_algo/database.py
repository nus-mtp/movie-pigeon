"""handles all interactions with database"""
import recommedation_algo.config as config
import datetime

from psycopg2 import extras


class DatabaseHandler:

    def __init__(self):
        self.cursor, self.conn = config.database_connection()
        self.dict_cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)

    def get_users(self):
        self.dict_cursor.execute("SELECT id FROM users")
        return self.dict_cursor.fetchall()

    def get_user_history(self, user_id):
        self.cursor.execute("SELECT DISTINCT(u.movie_id), u.score FROM user_ratings u, public_ratings p "
                            "WHERE user_id=%s AND u.movie_id = p.movie_id and p.score is not NULL", (user_id, ))
        return self.cursor.fetchall()

    def get_public_rating_dict(self, movie_id):
        self.dict_cursor.execute("SELECT * FROM public_ratings WHERE movie_id=%s AND score is not NULL", (movie_id, ))
        return self.dict_cursor.fetchall()

    def get_public_rating(self, movie_id):
        self.cursor.execute("SELECT * FROM public_ratings WHERE movie_id=%s AND score is not NULL", (movie_id, ))
        return self.cursor.fetchall()

    def get_movie_id_by_year(self, year):
        today = datetime.datetime.now().strftime("%m-%d")
        upper = str(year) + "-" + today
        lower = str(year - 1) + "-" + today
        self.cursor.execute("SELECT movie_id, actors, genre, runtime, director "
                            "FROM movies "
                            "WHERE released <= %s AND released >= %s "
                            "AND actors is not null "
                            "and genre is not null "
                            "and runtime is not null "
                            "and runtime <> '' "
                            "and director is not null", (upper, lower))
        return self.cursor.fetchall()

    def get_movie_data_by_id(self, movie_id):
        self.cursor.execute("SELECT movie_id, rated, plot, actors, language, genre, runtime, director "
                            "FROM movies "
                            "WHERE movie_id=%s "
                            "AND actors is not null "
                            "and genre is not null "
                            "and runtime is not null "
                            "and runtime <> '' "
                            "and director is not null", (movie_id, ))
        return self.cursor.fetchone()

    def get_10_popular_movies(self):
        self.cursor.execute("SELECT m.movie_id, r.score FROM movies m, public_ratings r "
                            "WHERE m.movie_id = r.movie_id AND r.vote is not null "
                            "AND r.score is not null ORDER BY r.vote DESC LIMIT 10")
        return self.cursor.fetchall()

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

    def save_recommendations(self, recommendations, user_id):
        for recommendation in recommendations:
            movie_id, score = recommendation
            self.cursor.execute(
                "INSERT INTO recommendations (user_id, movie_id, score) "
                "VALUES (%s, %s, %s) "
                "ON CONFLICT (user_id, movie_id)"
                "DO UPDATE SET score=%s "
                "WHERE recommendations.user_id =%s AND recommendations.movie_id=%s",
                (
                    user_id, movie_id, score, score, user_id, movie_id
                )
            )
        self.conn.commit()

    def get_similarity_of_movies(self, target_movie, source_movie):
        self.cursor.execute("SELECT value FROM similarity WHERE id_1=%s AND id_2=%s", (target_movie, source_movie))
        return self.cursor.fetchone()[0]

    def get_user_history_object(self):
        self.dict_cursor.execute(
            "SELECT DISTINCT(u.movie_id), m.genre, m.actors, m.runtime, m.director "
            "FROM user_ratings u, movies m "
            "WHERE u.movie_id = m.movie_id "
            "AND m.genre IS NOT NULL "
            "AND m.actors IS NOT NULL "
            "AND m.runtime IS NOT NULL "
            "AND m.director IS NOT NULL "
            "AND m.genre <> '' "
            "AND m.actors <> '' "
            "AND m.runtime <> '' "
            "AND m.director <> '' "
        )
        return self.dict_cursor.fetchall()

    def get_movie_pool_object(self):
        self.dict_cursor.execute(
            "SELECT movie_id, genre, actors, director, runtime "
            "FROM movies "
            "WHERE genre IS NOT NULL "
            "AND actors IS NOT NULL "
            "AND runtime IS NOT NULL "
            "AND director IS NOT NULL "
            "AND genre <> '' "
            "AND actors <> '' "
            "AND runtime <> '' "
            "AND director <> '' "
            "AND released < now() "
            "ORDER BY released DESC LIMIT 5000"
        )
        return self.dict_cursor.fetchall()

    def load_similarity(self, movie_id_1, movie_id_2, similarity):
        self.cursor.execute(
            "INSERT INTO similarity (id_1, id_2, similarity_value) VALUES (%s, %s, %s)",
            (
                movie_id_1, movie_id_2, similarity
            )
        )
        self.cursor.execute(
            "INSERT INTO similarity (id_1, id_2, similarity_value) VALUES (%s, %s, %s)",
            (
                movie_id_2, movie_id_1, similarity
            )
        )
        self.conn.commit()

    def get_similarity_matrix_pair(self):
        self.cursor.execute("SELECT id_1, id_2 FROM similarity")
        return self.cursor.fetchall()
