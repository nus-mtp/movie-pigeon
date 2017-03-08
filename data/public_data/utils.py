from enum import Enum
from datetime import datetime


class UrlFormatter(Enum):

    IMDB_URL_FORMAT = "http://www.imdb.com/title/{}/"


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