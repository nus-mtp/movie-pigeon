import logging
import datetime

def initialise_logger():
    logger = logging.getLogger("general_logger")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('general.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def initialise_test_logger():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    return logger

# ==============
#   Movie Data
# ==============
def get_movie_data_dict(actors, country, director, genre, imdb_id, language, plot, poster_url,
                        production_year, rated, released, runtime, title, type):
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


def imdb_id_builder(i):
    current_imdb_number = "{0:0=7d}".format(i)
    imdb_id = "tt" + current_imdb_number
    return imdb_id

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
        input_text = datetime.datetime.strptime(input_text, '%d %B %Y').strftime('%Y-%m-%d')
    elif length_of_date == 2:
        input_text = datetime.datetime.strptime(input_text, '%B %Y').strftime('%Y-%m-%d')
    elif length_of_date == 1:
        if input_text == "":
            return None
        else:
            input_text = datetime.datetime.strptime(input_text, '%Y').strftime('%Y-%m-%d')
    return input_text