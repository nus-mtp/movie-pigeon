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
