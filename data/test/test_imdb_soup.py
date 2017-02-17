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

    def __init__(self, *args, **kwargs):
        super(TestIMDbSoup, self).__init__(*args, **kwargs)

    # def test_extract_title_and_year(self):
    #     """
    #     test the extractor of movie title and production year
    #     1. title is not nullable
    #     2. production year is nullable
    #     :return:
    #     """
    #     self.assertEqual(IMDbSoup(self.test_id_list[0]).extract_title_and_year(), ('Carmencita', 1894))
    #     self.assertEqual(IMDbSoup(self.test_id_list[1]).extract_title_and_year(), ('The Top 14 Perform', None))
    #     self.assertEqual(IMDbSoup(self.test_id_list[2]).extract_title_and_year(), ('Hot Properties', None))
    #     self.assertEqual(IMDbSoup(self.test_id_list[3]).extract_title_and_year(), ('Episode dated 24 March 2004', None))
    #     self.assertEqual(IMDbSoup(self.test_id_list[7]).extract_title_and_year(), ('La La Land', 2016))

    # def test_extract_poster(self):
    #     """
    #     test the extractor of movie poster url
    #     1. url is nullable
    #     :return:
    #     """
    #     self.assertEqual(IMDbSoup(self.test_id_list[0]).extract_poster(),
    #                      "https://images-na.ssl-images-amazon.com/"
    #                      "images/M/MV5BMjAzNDEwMzk3OV5BMl5BanBnXkFtZTcwOTk4OTM5Ng@@._V1_UY268_CR6,0,182,268_AL_.jpg")
    #     self.assertEqual(IMDbSoup(self.test_id_list[1]).extract_poster(),
    #                      "https://images-na.ssl-images-amazon.com/"
    #                      "images/M/MV5BMTMxMjU0MTMxMl5BMl5BanBnXkFtZTcwNjY4Mjc3MQ@@._V1_UY268_CR2,0,182,268_AL_.jpg")
    #     self.assertEqual(IMDbSoup(self.test_id_list[13]).extract_poster(), None)
    #     self.assertEqual(IMDbSoup(self.test_id_list[14]).extract_poster(), None)

    # def test_extract_credits(self):
    #     """
    #     test the extractor of credits
    #     1. actors can be nullable, one token or multiple tokens
    #     2. directors can be nullable, one token or multiple tokens
    #     :return:
    #     """
    #     # None, None
    #     self.assertEqual(IMDbSoup(self.test_id_list[16]).extract_credits(),
    #                      (None, None))
    #     # None, Director
    #     self.assertEqual(IMDbSoup(self.test_id_list[14]).extract_credits(),
    #                      (None, "Birt Acres"))
    #     # None, Directors
    #     self.assertEqual(IMDbSoup(self.test_id_list[17]).extract_credits(),
    #                      (None, "Auguste Lumière, Louis Lumière"))
    #     # Actor, None
    #     self.assertEqual(IMDbSoup(self.test_id_list[3]).extract_credits(),
    #                      ("Agustín Bravo", None))
    #     # Actors, None
    #     self.assertEqual(IMDbSoup(self.test_id_list[5]).extract_credits(),
    #                      ("Grant Gustin, Candice Patton, Danielle Panabaker", None))
    #     # Actor, Director
    #     self.assertEqual(IMDbSoup(self.test_id_list[0]).extract_credits(),
    #                      ("Carmencita", "William K.L. Dickson"))
    #     # Actors, Director
    #     self.assertEqual(IMDbSoup(self.test_id_list[1]).extract_credits(),
    #                      ("Joshua Allen, Stephen Boss, Cat Deeley", "Don Weiner"))
    #     # Actor, Directors
    #     self.assertEqual(IMDbSoup(self.test_id_list[18]).extract_credits(),
    #                      ("Thomas White", "George S. Fleming, Edwin S. Porter"))
    #     # Actors, Directors
    #     self.assertEqual(IMDbSoup(self.test_id_list[15]).extract_credits(),
    #                      ("Ruth Roland, George Larkin, Mark Strong", "Robert Ellis, Louis J. Gasnier"))

    # def test_extract_plot(self):
    #     # complete plot
    #     self.assertEqual(IMDbSoup(self.test_id_list[0]).extract_plot(),
    #                      "Performing on what looks like a small wooden stage, wearing a dress with a hoop skirt and "
    #                      "white high-heeled pumps, Carmencita does a dance with kicks and twirls, a smile always on "
    #                      "her face.")
    #
    #     # incomplete plot
    #     self.assertEqual(IMDbSoup(self.test_id_list[1]).extract_plot(),
    #                      "Host Cat Deeley promised at the outset that the final 14 dancers will face some changes and"
    #                      " the competition would get more difficult for the final seven couples...")
    #
    #     # none plot
    #     self.assertEqual(IMDbSoup(self.test_id_list[3]).extract_plot(), None)


