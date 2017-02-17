import unittest
import random
import data.utils as utils
from bs4 import BeautifulSoup
from urllib import request, error
from imdbsoup import IMDbSoup


class TestIMDbSoup(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                    'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869', 'tt0000019',
                    'tt0000025', 'tt0010781', 'tt0000481', 'tt0000012', 'tt0000399']

    imdb_url_format = "http://www.imdb.com/title/{}/"

    def __init__(self, *args, **kwargs):
        super(TestIMDbSoup, self).__init__(*args, **kwargs)

    def test_extract_title_and_year(self):
        """
        test the extractor of movie title and production year
        1. title is not nullable
        2. production year is nullable
        :return:
        """
        self.assertEqual(IMDbSoup(self.test_id_list[0]).extract_title_and_year(), ('Carmencita', 1894))
        self.assertEqual(IMDbSoup(self.test_id_list[1]).extract_title_and_year(), ('The Top 14 Perform', None))
        self.assertEqual(IMDbSoup(self.test_id_list[2]).extract_title_and_year(), ('Hot Properties', None))
        self.assertEqual(IMDbSoup(self.test_id_list[3]).extract_title_and_year(), ('Episode dated 24 March 2004', None))
        self.assertEqual(IMDbSoup(self.test_id_list[7]).extract_title_and_year(), ('La La Land', 2016))

