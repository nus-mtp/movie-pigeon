from pytz import timezone
from datetime import datetime, timedelta

import time


class Transformer:

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def split_release_and_country_imdb(release_country):
        """
        given a string containing released date and country of a movie, return both fields
        :param release_country: string
        :return: string, string
        """
        released, country = release_country.replace(")", "").split("(")
        released = released.strip()  # remove last white space
        return released, country

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def movie_rating_votes(votes):
        votes = votes.replace(",", "")
        return votes


class GeneralTransformer:

    @staticmethod
    def get_singapore_date(n):
        """get the date of n days from now in SGT"""
        today = (datetime.fromtimestamp(time.time(), timezone("Singapore")) + timedelta(days=n)).strftime(
            "%Y-%m-%d")
        return today

    @staticmethod
    def convert_12_to_24_hour_time(time_string):
        """
        convert time in 12 hour string format to 24 hour string format
        :param time_string: string
        :return: string
        """
        return datetime.strptime(time_string, "%I:%M%p").strftime("%H:%M:%S")

    @staticmethod
    def build_imdb_id(i):
        """
        this function takes in an integer and converts it to an imdb id
        :param i: integer
        :return: string
        """
        current_imdb_number = "{0:0=7d}".format(i)
        imdb_id = "tt" + current_imdb_number
        return imdb_id


class CinemaScheduleTransformer:

    @staticmethod
    def get_id_from_cathay_cinema_name(cinema_name):
        """get cathay internal id from their cinema name for web elements"""
        mapper = {
            "Cathay Cineplex Amk Hub": "",
            "Cathay Cineplex Causeway Point": "1",
            "Cathay Cineplex Cineleisure Orchard": "2",
            "Cathay Cineplex Downtown East": "3",
            "Cathay Cineplex Jem": "4",
            "The Cathay Cineplex": "5",
            "Cathay Cineplex West Mall": "6"
        }
        return mapper[cinema_name]

    def parse_cinema_object_to_data(self, cinema_object):
        """
        parse the cinema object in the format:
        (based on self.provider, parsing strategy may vary)
        {
            movie_title: a list of movie schedule
        }
        to the format that can be consumed by loader class and
        subsequently being stored into the database
        {
            "title": ...,
            "schedule": [...],
            "type": ...

        In the process, it will complete 2 additional tasks
        besides rearranging the dictionary -- parse the movie
        title into title and additional information such as
        "3D" "Dolby Digital", and match the title to imdb id

        It will also return another list of imdb id found in this
        process and subjected to movie data extraction process if
        imdb id is not present in database
        :return: dictionary
        """
        data_object = []

        # parse title
        for key, value in cinema_object.items():
            if "Zen Zone" in key:  # strange thing in gv
                continue
            title, additional_info = self._movie_title_parser(key)
            data_object.append(
                {
                    "title": title,
                    "schedule": value,
                    "type": additional_info
                })
        return data_object

    def _movie_title_parser(self, title):
        additional_info = []
        if self.provider == "gv":
            if "`" in title:
                title = title.replace("`", "\'")
            if "*" in title:
                title = title.replace("*", "")
                additional_info.append("No free pass")
            if "(Eng Sub)" in title:
                title = title.replace("(Eng Sub)", "")
                additional_info.append("English sub only")
            if "(Atmos)" in title:
                title = title.replace("(Atmos)", "")
                additional_info.append("Atmos")
            if "Dessert Set" in title:
                title = title.replace("Dessert Set", "")
                additional_info.append("Dessert Set")
            if "(D-Box)" in title:
                title = title.replace("(D-Box)", "")
                additional_info.append("(D-Box)")
        elif self.provider == "cathay":
            if "*" in title:
                title = title.replace("*", "")
                # have not figure out the meaning of *
            if "(Dolby Digital)" in title:
                tokens = title.split(" ")
                splitter = tokens.index("(Dolby")
                title = " ".join(tokens[:splitter - 1])
                additional_info.append("Dolby Digital")
            if "(Dolby Atmos)" in title:
                tokens = title.split(" ")
                splitter = tokens.index("(Dolby")
                title = " ".join(tokens[:splitter - 1])
                additional_info.append("Dolby Atmos")
                title = title.replace("Atmos", "")
        elif self.provider == "sb":
            # special rules
            if "Kungfu" in title:
                title = title.replace("Kungfu", "Kung-fu")

            # general rules
            if "`" in title:
                title = title.replace("`", "\'")
            if "[D]" in title:
                title = title.replace("[D]", "")
                additional_info.append("Digital")
            if "[IMAX]" in title:
                title = title.replace("[IMAX]", "")
                additional_info.append("IMAX")
            if "[M]" in title:
                title = title.replace("[M]", "")
            if "[IMAX 3D]" in title:
                title = title.replace("[IMAX 3D]", "")
                additional_info.append("IMAX")
                additional_info.append("3D")

        else:
            raise Exception("Invalid cinema provider")

        title = title.strip()
        additional_info = ",".join(additional_info)
        return title, additional_info



