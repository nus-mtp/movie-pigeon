import unittest
import random
import data.utils as utils
from bs4 import BeautifulSoup
from urllib import request, error
from data.etl.movierating import MovieRating


class TestMovieRating(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                    'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869', 'tt0000019',
                    'tt0000025', 'tt0010781', 'tt0000481', 'tt0000012', 'tt0000399', 'tt0039624', 'tt0030298',
                    'tt0039445']

    def __init__(self, *args, **kwargs):
        super(TestMovieRating, self).__init__(*args, **kwargs)

    def test_extract_trakt_tv_ratings(self):
        self.assertEqual(MovieRating(self.test_id_list[0])._extract_trakt_rating(), ('4.66667', '9'))
        self.assertEqual(MovieRating(self.test_id_list[1])._extract_trakt_rating(), ('0.0', '0'))
        self.assertEqual(MovieRating(self.test_id_list[2])._extract_trakt_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[3])._extract_trakt_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[4])._extract_trakt_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[7])._extract_trakt_rating(), ('7.92902', '4973'))

        # new movie data for type validation
        rating, votes = MovieRating(self.test_id_list[7])._extract_douban_rating()
        self.assertTrue(utils.is_numeric(rating.isnumeric()))
        self.assertTrue(utils.is_numeric(votes.isnumeric()))

    def test_extract_imdb_rating(self):
        self.assertEqual(MovieRating(self.test_id_list[0])._extract_imdb_rating(), ('5.8', '1232'))
        self.assertEqual(MovieRating(self.test_id_list[1])._extract_imdb_rating(), ('5.3', '13'))
        self.assertEqual(MovieRating(self.test_id_list[2])._extract_imdb_rating(), ('6.4', '227'))
        self.assertEqual(MovieRating(self.test_id_list[3])._extract_imdb_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[4])._extract_imdb_rating(), ('8.5', '4265'))
        self.assertEqual(MovieRating(self.test_id_list[7])._extract_imdb_rating(), ('8.5', '170403'))

        # new movie data for type validation
        rating, votes = MovieRating(self.test_id_list[7])._extract_douban_rating()
        self.assertTrue(utils.is_numeric(rating.isnumeric()))
        self.assertTrue(utils.is_numeric(votes.isnumeric()))

    def test_extract_douban_rating(self):
        # old movie data for value validation
        self.assertEqual(MovieRating(self.test_id_list[0])._extract_douban_rating(), ('7.1', '164'))
        self.assertEqual(MovieRating(self.test_id_list[1])._extract_douban_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[2])._extract_douban_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[3])._extract_douban_rating(), (None, None))
        self.assertEqual(MovieRating(self.test_id_list[4])._extract_douban_rating(), ('7.5', '5416'))

        # new movie data for type validation
        rating, votes = MovieRating(self.test_id_list[7])._extract_douban_rating()
        self.assertTrue(utils.is_numeric(rating.isnumeric()))
        self.assertTrue(utils.is_numeric(votes.isnumeric()))
