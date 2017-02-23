from data.etl.cinemalist import CinemaList

import unittest


class TestCinemaList(unittest.TestCase):

    def setUp(self):
        self.cinema_list = CinemaList()

    # def test_get_golden_villiage(self):
    #     cinemalist = CinemaList()
    #     cinemalist.get_golden_village_cinema_list()

    def test_get_cathay(self):
        self.cinema_list.get_cathay()
