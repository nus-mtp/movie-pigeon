import unittest
import random
import data.utils as utils
from bs4 import BeautifulSoup
from urllib import request, error
from extractor import Extractor


class TestExtractor(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                    'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869', 'tt0000019',
                    'tt0000025', 'tt0010781', 'tt0000481', 'tt0000012', 'tt0000399']

    imdb_url_format = "http://www.imdb.com/title/{}/"

    def __init__(self, *args, **kwargs):
        super(TestExtractor, self).__init__(*args, **kwargs)

    # ============
    #  Main tests
    # ============
    # def test_extract_title_and_year(self):
    #     """
    #     :return: integer!, string!
    #     """
    #     extractor = Extractor(None)
    #     self.assertEqual(extractor.extract_title_and_year(self.build_soup(self.test_id_list[0])), (1894, 'Carmencita'))
    #     self.assertEqual(extractor.extract_title_and_year(self.build_soup(self.test_id_list[1])),
    #                      (None, 'The Top 14 Perform'))
    #     self.assertEqual(extractor.extract_title_and_year(self.build_soup(self.test_id_list[2])),
    #                      (None, 'Hot Properties'))
    #     self.assertEqual(extractor.extract_title_and_year(self.build_soup(self.test_id_list[3])),
    #                      (None, 'Episode dated 24 March 2004'))
    #     self.assertEqual(extractor.extract_title_and_year(self.build_soup(self.test_id_list[7])), (2016, 'La La Land'))

    # def test_extract_poster(self):
    #     extractor = Extractor(None)
    #     self.assertEqual(extractor.extract_poster(self.build_soup(self.test_id_list[0])),
    #                      "https://images-na.ssl-images-amazon.com/"
    #                      "images/M/MV5BMjAzNDEwMzk3OV5BMl5BanBnXkFtZTcwOTk4OTM5Ng@@._V1_UY268_CR6,0,182,268_AL_.jpg")
    #     self.assertEqual(extractor.extract_poster(self.build_soup(self.test_id_list[1])),
    #                      "https://images-na.ssl-images-amazon.com/"
    #                      "images/M/MV5BMTMxMjU0MTMxMl5BMl5BanBnXkFtZTcwNjY4Mjc3MQ@@._V1_UY268_CR2,0,182,268_AL_.jpg")
    #     self.assertEqual(extractor.extract_poster(self.build_soup(self.test_id_list[13])), None)
    #     self.assertEqual(extractor.extract_poster(self.build_soup(self.test_id_list[14])), None)

    # def test_extract_credits(self):
    #     extractor = Extractor(None)
    #
    #     # None, None
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[16])),
    #                      (None, None))
    #     # None, Director
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[14])),
    #                      (None, "Birt Acres"))
    #     # None, Directors
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[17])),
    #                      (None, "Auguste Lumière, Louis Lumière"))
    #     # Actor, None
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[3])),
    #                      ("Agustín Bravo", None))
    #     # Actors, None
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[5])),
    #                      ("Grant Gustin, Candice Patton, Danielle Panabaker", None))
    #     # Actor, Director
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[0])),
    #                      ("Carmencita", "William K.L. Dickson"))
    #     # Actors, Director
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[1])),
    #                      ("Joshua Allen, Stephen Boss, Cat Deeley", "Don Weiner"))
    #     # Actor, Directors
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[18])),
    #                      ("Thomas White", "George S. Fleming, Edwin S. Porter"))
    #     # Actors, Directors
    #     self.assertEqual(extractor.extract_credits(self.build_soup(self.test_id_list[15])),
    #                      ("Ruth Roland, George Larkin, Mark Strong", "Robert Ellis, Louis J. Gasnier"))

    # def test_extract_subtext(self):
    #     extractor = Extractor(utils.initialise_test_logger())
    #
    #     # test movie with 2, 3, 4 subtextes
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[0]), self.test_id_list[0]),
    #                      ('USA', 'Documentary, Short', None, '1894-03-10', '1', 'movie'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[7]), self.test_id_list[7]),
    #                      ('Singapore', 'Comedy, Drama, Musical', 'PG13', '2016-12-08', '128', 'movie'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[8]), self.test_id_list[8]),
    #                      ('France', 'Animation, Short', None, '1892-10-28', None, 'movie'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[9]), self.test_id_list[8]),
    #                      (None, 'Short, Sport', None, None, '1', 'movie'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[10]), self.test_id_list[8]),
    #                      (None, None, None, None, '100', 'movie'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[11]), self.test_id_list[8]),
    #                      ('Germany', None, None, '1913-01-10', None, 'movie'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[12]), self.test_id_list[8]),
    #                      (None, None, None, None, None, 'movie'))
    #
    #     # test episode with 2, 3, 4 subtextes
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[1]), self.test_id_list[8]),
    #                      (None, 'Game-Show, Music, Reality-TV', None, '2008-07-02', '60', 'episode'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[3]), self.test_id_list[8]),
    #                      (None, None, None, '2004-03-24', '75', 'episode'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[4]), self.test_id_list[8]),
    #                      (None, 'Action, Adventure, Drama', 'PG', '2015-10-06', '43', 'episode'))
    #
    #     # test tv with 2, 3, 4 subtextes
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[5]), self.test_id_list[8]),
    #                      (None, 'Action, Adventure, Drama', 'PG', None, '43', 'tv'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[2]), self.test_id_list[8]),
    #                      (None, 'Comedy', None, None, '30', 'tv'))
    #     self.assertEqual(extractor.extract_subtext(self.build_soup(self.test_id_list[6]), self.test_id_list[8]),
    #                      (None, None, None, None, '75', 'tv'))

    def build_soup(self, test_id):
        url = self.imdb_url_format.format(test_id)
        request_result = request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(request_result, "lxml")  # soup builder
        return soup
