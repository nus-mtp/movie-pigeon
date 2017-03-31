"""handles all interactions with database"""
import recommedation_algo.config as config
import datetime


class DatabaseHandler:

    def __init__(self):
        self.cursor, self.conn = config.database_connection()

    def get_users(self):
        self.cursor.execute("SELECT id FROM users")
        return self.cursor.fetchall()

    def get_user_history(self, user_id):
        self.cursor.execute("SELECT movie_id, score FROM user_ratings WHERE user_id=%s", (user_id, ))
        return self.cursor.fetchall()

    def get_public_rating(self, movie_id):
        self.cursor.execute("SELECT * FROM public_ratings WHERE movie_id=%s", (movie_id, ))
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
