from cinema import CinemaList

import unittest
import utils


class TestCinemaList(unittest.TestCase):

    def setUp(self):
        self.cinema_list = CinemaList()

    def test_extract_sb_cinema_list(self):
        soup = utils.build_soup_from_file('data_cinema_data/shaw_home.html')
        cinema_list = self.cinema_list._extract_sb_cinema_list(soup)
        self.assertEqual(len(cinema_list), 8)  # 8 cinemas for shaw

    def test_extract_cathay_cinema_list(self):
        soup = utils.build_soup_from_file('data_cinema_data/cathay_home.html')
        cinema_list = self.cinema_list._extract_cathay_cinema_list(soup)
        self.assertEqual(len(cinema_list), 7)  # 7 cinemas for cathay

    # comment out because it takes too long to be run on CI tools
    # def test_extract_gv_cinema_list(self):
    #     cinema_list = self.cinema_list._extract_gv_cinema_list()
    #     self.assertEqual(len(cinema_list), 31)  # 31 cinemas, 25 valid
