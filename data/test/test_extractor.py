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
    #




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

    # def test_extract_plot(self):
    #     extractor = Extractor(None)
    #     # complete plot
    #     self.assertEqual(extractor.extract_plot(self.build_soup(self.test_id_list[0])),
    #                      "Performing on what looks like a small wooden stage, wearing a dress with a hoop skirt and "
    #                      "white high-heeled pumps, Carmencita does a dance with kicks and twirls, a smile always on "
    #                      "her face.")
    #
    #     # incomplete plot
    #     self.assertEqual(extractor.extract_plot(self.build_soup(self.test_id_list[1])),
    #                      "Host Cat Deeley promised at the outset that the final 14 dancers will face some changes and"
    #                      " the competition would get more difficult for the final seven couples...")
    #
    #     # none plot
    #     self.assertEqual(extractor.extract_plot(self.build_soup(self.test_id_list[3])), None)

    def build_soup(self, test_id):
        url = self.imdb_url_format.format(test_id)
        request_result = request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(request_result, "lxml")  # soup builder
        return soup
