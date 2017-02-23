from data.etl.cinemalist import CinemaList

import unittest


class TestCinemaList(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCinemaList, self).__init__(*args, **kwargs)

    def test_get_golden_villiage(self):
        cinemalist = CinemaList()
        cinemalist.get_golden_village_cinema_list()
