from public_data.cinema import CinemaList

import unittest


class TestCinemaList(unittest.TestCase):

    def setUp(self):
        self.cinema_list = CinemaList(test=True)

    def test_extract_sb_cinema_list(self):
        cinema_list = self.cinema_list._extract_sb_cinema_list()
        self.assertEqual(len(cinema_list), 8)  # 8 cinemas for shaw

    def test_extract_cathay_cinema_list(self):
        cinema_list = self.cinema_list._extract_cathay_cinema_list()
        self.assertEqual(len(cinema_list), 7)  # 7 cinemas for cathay

    def test_extract_gv_cinema_list(self):
        cinema_list = self.cinema_list._extract_gv_cinema_list()
        self.assertEqual(len(cinema_list), 25)  # 31 cinemas, 25 valid

if __name__ == '__main__':
    unittest.main()
