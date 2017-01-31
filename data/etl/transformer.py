import datetime


class Transformer:

    def __init__(self):
        pass

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
        return runtime

    @staticmethod
    def movie_data_na_to_none(general):
        if general == "N/A":
            return None
        return general
    # ================
    #   Movie Rating
    # ================
    # ================
    #   Now Showing
    # ================
