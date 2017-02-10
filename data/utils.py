import logging


def initialise_logger():
    logger = logging.getLogger("general_logger")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('general.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
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