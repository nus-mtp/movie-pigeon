from public_data.cinema import CinemaList

import unittest
import public_data.utils as utils


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

    # @unittest.skip  # test skipped for CI, tested using IDE
    # def test_get_geocode(self):
    #     self.assertEqual(self.cinema_list._get_geocode("27 Prince George's Park"), (1.2913898, 103.7810233))
    #     self.assertEqual(self.cinema_list._get_geocode("The Cathay Cineplex"), (1.299414, 103.847644))
    #     self.assertEqual(self.cinema_list._get_geocode("Cathay Cineplex Cineleisure Orchard"), (1.3016415, 103.8362236))
    #     self.assertEqual(self.cinema_list._get_geocode("Shaw Theatres Lot One"), (1.3850213, 103.7451159))
    #     self.assertEqual(self.cinema_list._get_geocode("Shaw Theatres Jcube"), (1.3332858, 103.7401865))

if __name__ == '__main__':
    unittest.main()
