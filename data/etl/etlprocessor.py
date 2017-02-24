"""
    Core objective of this etl framework. This is the highest level API.
    Each one of them will be run in backend on server, at desginated
    time intervals.

    It includes four main methods in total:
        1. update movie data
        2. update movie public rating
        3. update the list of cinemas in Singapore
        4. update cinema schedule for each cinema available
"""
import etl.extractor as extractor
import etl.transformer as transformer
import etl.loader as loader

import utils
import psycopg2


from urllib import error


class ETLProcessor:

    def __init__(self):
        self.logger = utils.initialise_logger()
        self.logger.info("Initialise ETL process ...")

        self.extractor = extractor.Extractor(self.logger)
        self.loader = loader.Loader(self.logger)
        self.transformer = transformer.Transformer(self.logger)

    def update_movie_data(self):
        """updates movie data from databases (potentially more than one source)
            it is a one time process, i.e. data will not be updated constantly
        """
        self.logger.info("Initialise movie data retrieval process ...")
        existing_movies_id = self.loader.get_movie_id_list()

        for index in range(1, 9999999):  # iterate all possible titles
            imdb_id = utils.imdb_id_builder(index)
            if imdb_id in existing_movies_id:
                continue

            try:
                movie_data = self.extractor.extract_movie_data(imdb_id)
            except error.HTTPError:
                self.logger.error("Movie ID is not valid." + imdb_id)
                continue
            except:  # need to find out the exact error type
                self.logger.error("Movie ID type is not registered." + imdb_id)
                continue
            try:
                self.loader.load_movie_data(movie_data)
            except psycopg2.DataError:
                self.logger.error("Invalid insertion! Due to the subtext are partially parsed.")
                self.logger.error(movie_data)
                continue

        self.logger.info("Movie data update process complete.")

    def update_movie_rating(self):
        """updates movie rating from popcorn movies (may have to change to raaw implementation in the future)
        it is a continuous process and data will be updated constantly
        """
        self.logger.info("Initialise movie rating update process ...")

        # get list of existing movies
        id_list = self.loader.get_movie_id_list()

        self.logger.info("Movie rating update process complete.")

    def update_cinema_schedule(self):
        """
        updates movie rating from various theatres official page
        it is a continuous process and data will be updated constantly
        """
        self.logger.info("Initialise movie showing update process ...")
        self.logger.info("Movie showing update process complete.")
        pass

    def update_cinema_list(self):
        """update cinema list from various theatres websites"""
        self.logger.info("Initialise cinema list update process ...")
        cinema_list = self.extractor.extract_cinema_list()
        self.loader.load_cinema_list(cinema_list)
        self.logger.info("Cinema list update process complete.")


