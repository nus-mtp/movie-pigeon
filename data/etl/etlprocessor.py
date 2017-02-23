import etl.extractor as extractor
import etl.transformer as transformer
import etl.loader as loader
import utils
import psycopg2


from urllib import error


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

    def update_movie_data(self):
        """
            updates movie data from databases (potentially more than one source)
            it is a one time process, i.e. data will not be updated constantly
        """
        self.logger.info("Initialise movie data retrieval process ...")
        existing_movies_id = self.loader.get_movie_id_list()

        for index in range(105000, 9999999):  # iterate all possible titles
            imdb_id = utils.imdb_id_builder(index)
            if imdb_id in existing_movies_id:
                continue

            # soup
            try:
                movie_data = self.extractor.extract_movie_data(imdb_id)
            except error.HTTPError:
                self.logger.error("Movie ID is not valid." + imdb_id)
                continue
            except:
                self.logger.error("Movie ID type is not registered." + imdb_id)
                continue
            try:
                self.loader.load_movie_data(movie_data)
            except psycopg2.DataError:
                self.logger.error("Invalid insertion!")
                self.logger.error(movie_data)
                continue

        self.logger.info("Movie data update process complete.")

    def update_movie_rating(self):
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

    def update_movie_showing(self):
        """
        updates movie rating from various theatres official page
        it is a continuous process and data will be updated constantly
        """
        self.logger.info("Initialise movie showing update process ...")
        self.logger.info("Movie showing update process complete.")

    def update_cinema_list(self):
        """update cinema list from various theatres websites"""
        self.logger.info("Initialise cinema list update process ...")
        cinema_list = self.extractor.extract_cinema_list()
        self.loader.load_cinema_list(cinema_list)
        self.logger.info("Cinema list update process complete.")

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

