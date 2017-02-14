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
    3. update movie data in public theatres of Singapore
    """

    def __init__(self):
        self.logger = utils.initialise_logger()
        self.logger.info("Initialise ETL process ...")

        self.extractor = extractor.Extractor(self.logger)
        self.loader = loader.Loader(self.logger)
        self.transformer = transformer.Transformer(self.logger)

    def retrieve_movie_data(self):
        """
        updates movie data from databases (potentially more than one source)
        it is a one time process, i.e. data will not be updated constantly
        """
        self.logger.info("Initialise movie data retrieval process ...")

        existing_movies_id = self.loader.get_movie_id_list()
        logging.info("Initiating movie data extraction process...")

        for index in range(1, 9999999):  # iterate all possible titles
            imdb_id = utils.imdb_id_builder(index)

            if imdb_id in existing_movies_id:
                continue

            movie_data = self.extractor.extract_imdb_data(imdb_id)

            if movie_data:
                self.loader.load_movie_data(movie_data)
            time.sleep(1)

    def updating_movie_rating(self):
        """
        updates movie rating from popcorn movies (may have to change to raaw implementation in the future)
        it is a continuous process and data will be updated constantly
        """
        self.logger.info("Initialise movie rating update process ...")

        # get list of existing movies
        id_list = self.loader.get_movie_id_list()

        for current_movie_id in id_list:
            self.update_rating_simple(current_movie_id, "IMDb")
            self.update_rating_simple(current_movie_id, "Douban")
            self.update_rating_simple(current_movie_id, "Trakt")

            # metacritic
            # letterboxd
            # rotten tomatoes
            # validation_info = self.loader.get_movie_validation_info(current_movie_id)
            # print(validation_info)

            # break
        self.logger.info("Movie rating update process complete.")

    def updating_movie_showing(self):
        """
        updates movie rating from various theatres official page
        it is a continuous process and data will be updated constantly
        """
        self.logger.info("Initialise movie showing update process ...")
        self.logger.info("Movie showing update process complete.")
        pass

    # ===========================
    #   helper (private methods)
    # ===========================
    def update_rating_simple(self, current_movie_id, source_name):
        if source_name == "IMDb":
            rating, votes = self.extractor.extract_imdb_rating(current_movie_id)
        elif source_name == "Douban":
            rating, votes = self.extractor.extract_douban_rating(current_movie_id)
        elif source_name == "Trakt":
            rating, votes = self.extractor.extract_trakt_rating(current_movie_id)
        else:
            self.logger.error("The input source name is not valid!")
            raise Exception("There is no such source name.")

        movie_rating = utils.get_movie_rating_dict(rating, votes, current_movie_id, source_name)
        self.loader.load_movie_rating(movie_rating)

# ==================
#   run main logic
# ==================
if __name__ == '__main__':
    processor = ETLProcessor()
    processor.retrieve_movie_data()

