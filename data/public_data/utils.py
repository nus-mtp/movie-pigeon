from enum import Enum
from datetime import datetime, timedelta
from pytz import timezone
from urllib import request
from bs4 import BeautifulSoup

import time
import json


def get_geocode(address):
    """
    return the latitude and longtitude of an address,
    given by google geocode api
    :param address: string
    :return: float, float
    """
    address = _parse_special_cinema(address)

    time.sleep(1)  # important to avoid violating google api limit

    web_result = _get_json_result_from_google_geocode(address)
    location = web_result['results'][0]['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']
    return latitude, longitude


def _parse_special_cinema(address):
    """
    parse the name of special cinemas, so it
    can be used for google API
    :param address: string
    :return: string
    """
    address += "Singapore"  # ensure the search is in Singapore
    if ',' in address:
        address = address.split(",")[-1].strip()  # special cinema will be determined by their location
    if '(' in address:
        address = address.split('(')[0].strip()  # remove stalls
    address = address.replace(" ", '%20')  # replace space for html encoding
    return address


def _get_json_result_from_google_geocode(address):
    GOOGLE_GEOCODE_API = 'http://maps.google.com/maps/api/geocode/json?address={}'

    url = GOOGLE_GEOCODE_API.format(address)
    json_content = request.urlopen(url).read().decode('utf-8')
    web_result = json.loads(json_content)
    return web_result


class UrlFormatter(Enum):

    IMDB_URL_FORMAT = "http://www.imdb.com/title/{}/"


class InvalidMovieTypeException(Exception):
    pass


class InvalidCinemaTypeException(Exception):
    pass


class InvalidMatchedIMDbIdException(Exception):
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


def build_soup_from_url(url):
    web_content = request.urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(web_content, "lxml")
    return soup


def build_soup_from_file(directory):
    io_wrapper = open(directory, encoding="utf8")
    soup = BeautifulSoup(io_wrapper, "lxml")
    io_wrapper.close()
    return soup


def get_singapore_date(n):
    """
    get the date of n days from now in SGT
    :param n: integer
    :return: string
    """
    some_day = (datetime.fromtimestamp(time.time(), timezone("Singapore"))
                + timedelta(days=n)).strftime("%Y-%m-%d")
    return some_day


