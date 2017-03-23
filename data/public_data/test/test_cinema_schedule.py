from cinema import CinemaSchedule

import unittest
import utils


class TestCinemaList(unittest.TestCase):

    def setUp(self):
        self.cinema_schedule = CinemaSchedule('gv', test=True, test_directory='data_cinema_schedule/gv.html')

    def test_extract_gv_schedule(self):
        pass