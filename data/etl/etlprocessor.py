import extractor
import logging


class ETLProcessor:

    def __init__(self):
        self.extractor = extractor.Extractor()

        self.imdb_prefix = "tt"

    def updating_movie_data(self):
        """
        updates movie data from omdb databases
        :return:
        """
        logging.info("Initiating movie data extraction process...")
        for i in range(1, 5):
            # extraction
            current_imdb_number = "{0:0=7d}".format(i)
            imdb_id = self.imdb_prefix + current_imdb_number
            extraction_result = self.extractor.extract_omdb(imdb_id)
            print(extraction_result)

            # transforming
            imdb_votes = extraction_result['imdbVotes']  # remove comma
            production_year = extraction_result['Released']
            runtime = extraction_result['Runtime']  # remove units
            imdb_rating = extraction_result['imdbRating']
            rated = extraction_result['Rated']
            actors = extraction_result['Actors']  # split into list and store in tables
            director = extraction_result['Director']

            # loading
            break

    def updating_movie_rating(self):
        """
        updates movie rating from various websites
        :return:
        """
        pass

if __name__ == '__main__':
    processor = ETLProcessor()
    processor.updating_movie_data()

