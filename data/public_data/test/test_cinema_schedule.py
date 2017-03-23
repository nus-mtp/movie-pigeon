"""These test cases will only be run in local environment"""
from cinema import CinemaSchedule

import unittest
import utils


class TestCinemaList(unittest.TestCase):

    def setUp(self):
        self.cinema_schedule = CinemaSchedule('gv')

    def test_extract_gv_schedule(self):
        self.cinema_schedule._new_extract_gv_schedule()
