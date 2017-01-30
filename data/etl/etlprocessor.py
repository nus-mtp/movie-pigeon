import extractor
import transformer
import loader
import logging
import data.utils as utils
import time


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
        for i in range(1, 50):
            # extraction
            current_imdb_number = "{0:0=7d}".format(i)
            imdb_id = self.imdb_prefix + current_imdb_number
            extraction_result = self.extractor.extract_omdb(imdb_id)

            # transforming
            # movies table data
            title = extraction_result['Title']
            production_year = utils.convert_na_to_none(extraction_result['Released'])  # to integer
            rated = extraction_result['Rated']
            plot = extraction_result['Plot']
            actors = extraction_result['Actors']
            language = extraction_result['Language']
            country = extraction_result['Country']

            runtime = extraction_result['Runtime']
            runtime = runtime.replace(" min", "")

            poster_url = extraction_result['Poster']
            genre = extraction_result['Genre']
            director = extraction_result['Director']
            released = utils.convert_na_to_none(extraction_result['Released'])

            movie_data = utils.get_movie_data_dict(actors, country, director, genre, imdb_id, language, plot,
                                                   poster_url, production_year, rated, released, runtime, title)

            # others
            imdb_votes = extraction_result['imdbVotes']  # remove comma
            imdb_rating = extraction_result['imdbRating']

            # unused : metascore, awards

            # loading
            self.loader.load_movie_data(movie_data)
            time.sleep(2)

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

