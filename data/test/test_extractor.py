import unittest
import random
import data.utils as utils
from bs4 import BeautifulSoup
from urllib import request, error
from extractor import Extractor


class TestExtractor(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                    'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869']

    test_soup_list = []

    imdb_url_format = "http://www.imdb.com/title/{}/"

    def __init__(self, *args, **kwargs):
        super(TestExtractor, self).__init__(*args, **kwargs)
        for test_id in self.test_id_list:
            url = self.imdb_url_format.format(test_id)
            request_result = request.urlopen(url).read()
            soup = BeautifulSoup(request_result, "lxml")  # soup builder
            self.test_soup_list.append(soup)

    # def test_extract_title_and_year(self):
    #     extractor = Extractor(None)
    #     self.assertEqual(extractor.extract_title_and_year(self.test_soup_list[0]), (1894, 'Carmencita'))
    #     self.assertEqual(extractor.extract_title_and_year(self.test_soup_list[1]), (None, 'The Top 14 Perform'))
    #     self.assertEqual(extractor.extract_title_and_year(self.test_soup_list[2]), (None, 'Hot Properties'))
    #     self.assertEqual(extractor.extract_title_and_year(self.test_soup_list[3]), (None, 'Episode dated 24 March 2004'))
    #
    # def test_is_episode(self):
    #     extractor = Extractor(None)
    #     self.assertEqual(extractor.is_episode(self.test_soup_list[0]), False)
    #     self.assertEqual(extractor.is_episode(self.test_soup_list[1]), True)
    #     self.assertEqual(extractor.is_episode(self.test_soup_list[2]), False)
    #     self.assertEqual(extractor.is_episode(self.test_soup_list[3]), True)
    #
    # def test_extract_type(self):
    #     extractor = Extractor(None)
    #     self.assertEqual(extractor.extract_type(self.test_soup_list[0]), None)
    #     self.assertEqual(extractor.extract_type(self.test_soup_list[1]), "episode")
    #     self.assertEqual(extractor.extract_type(self.test_soup_list[2]), None)
    #     self.assertEqual(extractor.extract_type(self.test_soup_list[3]), "episode")

    def test_extract_subtext(self):
        extractor = Extractor(utils.initialise_test_logger())

        # test movie with 2, 3, 4 subtextes
        self.assertEqual(extractor.extract_subtext(self.test_soup_list[0], self.test_id_list[0]), ('USA', 'Documentary, Short', None, '1894-03-10', '1', 'movie'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[7], self.test_id_list[7]), ('USA', 'Comedy, Drama, Musical', 'PG-13', '2016-12-25', '128', 'movie'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[8], self.test_id_list[8]), ('France', 'Animation, Short', None, '1892-10-28', None, 'movie'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[9], self.test_id_list[9]), (None, 'Short, Sport', None, None, '1', 'movie'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[10], self.test_id_list[10]), (None, None, None, None, '100', 'movie'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[11], self.test_id_list[11]), ('Germany', None, None, '1913-01-10', None, 'movie'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[12], self.test_id_list[12]), (None, None, None, None, None, 'movie'))



        # test episode with 2, 3, 4 subtextes
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[1], self.test_id_list[1]), (None, 'Game-Show, Music, Reality-TV', None, '2008-07-02', '60', 'episode'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[3], self.test_id_list[3]), (None, None, None, '2004-03-24', '75', 'episode'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[4], self.test_id_list[4]), (None, 'Action, Adventure, Drama', 'PG', '2015-10-06', '43', 'episode'))

        # test tv with 2, 3, 4 subtextes
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[5], self.test_id_list[5]), (None, 'Action, Adventure, Drama', 'PG', None, '43', 'tv'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[2], self.test_id_list[2]), (None, 'Comedy', None, None, '30', 'tv'))
        # self.assertEqual(extractor.extract_subtext(self.test_soup_list[6], self.test_id_list[6]), (None, None, None, None, '75', 'tv'))

