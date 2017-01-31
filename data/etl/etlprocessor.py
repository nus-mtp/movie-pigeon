import extractor
import transformer
import loader
import logging
import data.utils as utils
import time
import datetime

class ETLProcessor:

    def __init__(self):
        self.extractor = extractor.Extractor()
        self.loader = loader.Loader()
        self.transformer = transformer.Transformer()

        self.imdb_prefix = "tt"

    def updating_movie_data(self):
        """
        updates movie data from omdb databases
        :return:
        """

        logging.info("Initiating movie data extraction process...")
        for i in range(50, 1000):
            # extraction
            current_imdb_number = "{0:0=7d}".format(i)
            imdb_id = self.imdb_prefix + current_imdb_number
            extraction_result = self.extractor.extract_omdb(imdb_id)

            # transforming
            # movies table data
            title = extraction_result['Title']
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
            production_year = self.transformer.movie_data_date(extraction_result['Released'])  # to integer

            movie_data = utils.get_movie_data_dict(actors, country, director, genre, imdb_id, language, plot,
                                                   poster_url, production_year, rated, released, runtime, title)

            # others
            imdb_votes = extraction_result['imdbVotes']  # remove comma
            imdb_rating = extraction_result['imdbRating']

            # unused : metascore, awards

            # loading
            self.loader.load_movie_data(movie_data)

    @staticmethod
    def updating_movie_rating(self):
        """
        updates movie rating from various websites
        :return:
        """
        pass


if __name__ == '__main__':
    processor = ETLProcessor()
    processor.updating_movie_data()

