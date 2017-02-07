

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
        "IMDb": 1,
        "Douban": 2,
        "Trakt": 3
    }

    movie_rating = {
        "movie_id": imdb_id,
        "source_id": rating_sources[rating_source],
        "score": score,
        "votes": votes
    }
    return movie_rating