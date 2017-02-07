import datetime


class Transformer:

    def __init__(self, logger):
        self.logger = logger

    # ==============
    #   Movie Data
    # ==============
    @staticmethod
    def movie_data_date(raw_date):
        if raw_date == "N/A":
            return None
        production_year = datetime.datetime.strptime(raw_date, '%d %b %Y').strftime('%Y-%m-%d')
        return production_year

    @staticmethod
    def movie_data_rated(rating):
        if rating == "N/A" or rating == "NOT RATED" or rating == "UNRATED":
            return None
        return rating

    @staticmethod
    def movie_data_runtime(runtime):
        if runtime == "N/A":
            return None
        runtime = runtime.replace(" min", "")
        if "h" in runtime:
            [hours, minutes] = runtime.split("h")
            runtime = int(hours.rstrip()) * 60 + int(minutes.rstrip())
        return runtime

    @staticmethod
    def movie_data_na_to_none(general):
        if general == "N/A":
            return None
        return general
    # ================
    #   Movie Rating
    # ================

    @staticmethod
    def movie_rating_votes(votes):
        votes = votes.replace(",", "")
        return votes


    # ================
    #   Now Showing
    # ================
