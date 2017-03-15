from enum import Enum
from datetime import datetime


class UrlFormatter(Enum):

    IMDB_URL_FORMAT = "http://www.imdb.com/title/{}/"


class InvalidMovieTypeException(Exception):
    pass


def split_release_and_country_imdb(release_country):
    """
    given a string containing released date and country of a movie, return both fields
    :param release_country: string
    :return: string, string
    """
    released, country = release_country.replace(")", "").split("(")
    released = released.strip()  # remove last white space
    return released, country


def transform_time_imdb(runtime):
    """
    given a string of time in various format from imdb, return in minutes
    :param runtime: string
    :return: string
    """
    runtime = runtime.replace(" ", "").replace("min", "")
    if "h" in runtime:
        [hours, minutes] = runtime.split("h")
        if minutes == "":
            minutes = 0
        runtime = int(hours) * 60 + int(minutes)
    return str(runtime)


def transform_date_imdb(input_text):
    """
    given a date of string from imdb, return date in %Y-%m-%d format
    :param input_text: string
    :return: string
    """
    length_of_date = len(input_text.split(" "))
    if length_of_date == 3:
        input_text = datetime.strptime(input_text, '%d %B %Y').strftime('%Y-%m-%d')
    elif length_of_date == 2:
        input_text = datetime.strptime(input_text, '%B %Y').strftime('%Y-%m-%d')
    elif length_of_date == 1:
        if input_text == "":
            return None
        else:
            input_text = datetime.strptime(input_text, '%Y').strftime('%Y-%m-%d')
    return input_text


def get_movie_data_dict(actors, country, director, genre, imdb_id, language, plot, poster_url, production_year, rated,
                        released, runtime, title, type):
    """
    this is the data model of movie data.
    :param actors: string
    :param country: string
    :param director: string
    :param genre: string
    :param imdb_id: string
    :param language: string
    :param plot: string
    :param poster_url: string
    :param production_year: integer
    :param rated: string
    :param released: datetime
    :param runtime: string
    :param title: string
    :param type: string
    :return: dictionary
    """
    movie_data = {
        "movie_id": imdb_id,
        "title": title,
        "production_year": production_year,
        "rated": rated,
        "plot": plot,
        "actors": actors,
        "language": language,
        "country": country,
        "runtime": runtime,
        "poster_url": poster_url,
        "genre": genre,
        "director": director,
        "released": released,
        "type": type
    }
    return movie_data


def get_movie_rating_dict(score, votes, imdb_id, rating_source):
    """
        this is the data model of movie rating
    """
    rating_sources = {
        "IMDb": '1',
        "Douban": '2',
        "Trakt": '3'
    }

    movie_rating = {
        "movie_id": imdb_id,
        "source_id": rating_sources[rating_source],
        "score": score,
        "votes": votes
    }
    return movie_rating





