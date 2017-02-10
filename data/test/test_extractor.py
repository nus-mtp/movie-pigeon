import unittest
import random
import data.utils as utils
from bs4 import BeautifulSoup
from urllib import request, error
from extractor import Extractor


class TestExtractor(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678']

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
        extractor = Extractor(None)
        self.assertEqual(extractor.extract_subtext(self.test_soup_list[0]), ('USA', 'Documentary, Short', None, '1894-03-10', '1'))
        self.assertEqual(extractor.extract_subtext(self.test_soup_list[1]), (None, 'Game-Show, Music, Reality-TV', None, '2008-07-02', '60'))
        self.assertEqual(extractor.extract_subtext(self.test_soup_list[2]), (None, 'Comedy', None, '2005-01-01', '30'))
        self.assertEqual(extractor.extract_subtext(self.test_soup_list[3]), (None, None, None, '2014-03-24', '75'))
