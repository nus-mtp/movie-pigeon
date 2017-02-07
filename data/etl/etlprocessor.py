import extractor
import transformer
import loader
import logging
import data.utils as utils
import time


class ETLProcessor:
    """
    Core object of this etl framework. Logic of each main process listed below are included:
    1. update movie data
    2. update movie public rating
    """

    def __init__(self):
        # initialisation
        logger = logging.getLogger("general_logger")

        self.extractor = extractor.Extractor()
        self.loader = loader.Loader()
        self.transformer = transformer.Transformer()

        self.imdb_prefix = "tt"

    def updating_movie_data(self):
        """
        updates movie data from omdb databases (potentially more sources)
        """
        # preparation
        existing_movies = self.loader.get_movie_id_list()

        logging.info("Initiating movie data extraction process...")
        for i in range(1, 9999999):  # iterate all possible titles
            # 1. construct imdb_id
            current_imdb_number = "{0:0=7d}".format(i)
            imdb_id = self.imdb_prefix + current_imdb_number

            # validate repetition
            token = (imdb_id, )
            if token in existing_movies:
                continue

            # 2. extracting call api
            extraction_result = self.extractor.extract_omdb_data(imdb_id)

            # validate response
            if extraction_result['Response'] == "False":
                logging.warning(imdb_id + "| incorrect response returned")
                continue

            # 3. transforming
            title = extraction_result['Title']
            type = extraction_result['Type']
            rated = self.transformer.movie_data_rated(extraction_result['Rated'])
            plot = self.transformer.movie_data_na_to_none(extraction_result['Plot'])
            actors = self.transformer.movie_data_na_to_none(extraction_result['Actors'])
            language = self.transformer.movie_data_na_to_none(extraction_result['Language'])
            country = self.transformer.movie_data_na_to_none(extraction_result['Country'])
            runtime = self.transformer.movie_data_runtime(extraction_result['Runtime'])
            poster_url = self.transformer.movie_data_na_to_none(extraction_result['Poster'])
            genre = self.transformer.movie_data_na_to_none(extraction_result['Genre'])
            director = self.transformer.movie_data_na_to_none(extraction_result['Director'])
            released = self.transformer.movie_data_date(extraction_result['Released'])
            production_year = self.transformer.movie_data_date(extraction_result['Released'])

            movie_data = utils.get_movie_data_dict(actors, country, director, genre, imdb_id, language, plot,
                                                   poster_url, production_year, rated, released, runtime, title, type)

            # 4. loading
            self.loader.load_movie_data(movie_data)

            # friendly api call
            time.sleep(1)

    def updating_movie_rating(self):
        """
        updates movie rating from various websites
        """
        # list of existing movies
        id_list = self.loader.get_movie_id_list()
        for current_movie_id in id_list:
            self.update_rating_simple(current_movie_id, "IMDb")
            self.update_rating_simple(current_movie_id, "Douban")
            self.update_rating_simple(current_movie_id, "Trakt")

            # metacritic
            # validation_info = self.loader.get_movie_validation_info(current_movie_id)
            # print(validation_info)

    # ==========
    #   helper
    # ==========
    def update_rating_simple(self, current_movie_id, source_name):
        if source_name == "IMDb":
            rating, votes = self.extractor.extract_imdb_rating(current_movie_id)
        elif source_name == "Douban":
            rating, votes = self.extractor.extract_douban_rating(current_movie_id)
        elif source_name == "Trakt":
            rating, votes = self.extractor.extract_trakt_rating(current_movie_id)
        else:
            raise Exception("There is no such source name.")

        votes = self.transformer.movie_rating_votes(str(votes))
        movie_rating = utils.get_movie_rating_dict(rating, votes, current_movie_id, source_name)
        self.loader.load_movie_rating(movie_rating)


# ==================
#   run main logic
# ==================
if __name__ == '__main__':
    processor = ETLProcessor()
    processor.updating_movie_rating()

