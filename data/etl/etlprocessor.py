import extractor
import logging


class ETLProcessor:

    def __init__(self):
        self.extractor = extractor.Extractor()

    @staticmethod
    def updating_movie_data(self):
        """
        updates movie data from omdb databases
        :return:
        """
        logging.info("Initiating movie data extraction process...")
        imdb_prefix = "tt"
        for i in range(1, 5):
            imdb_number = "{0:0=7d}".format(i)
            imdb_id = imdb_prefix + imdb_number
            extraction_result = self.extractor.extract_omdb(imdb_id)
            print(extraction_result)

    @staticmethod
    def updating_movie_rating(self):
        """
        updates movie rating from various websites
        :return:
        """
        pass

if __name__ == '__main__':
    processer = ETLProcessor()
    processer.updating_movie_data()

