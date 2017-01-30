# ETL utils
def convert_na_to_none(data):
    if data == "N/A":
        return None
    return data


def get_movie_data_dict(actors, country, director, genre, imdb_id, language, plot, poster_url,
                        production_year, rated, released, runtime, title):
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
        "released": released
    }
    return movie_data