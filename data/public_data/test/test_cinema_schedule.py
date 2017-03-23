"""These test cases will only be run in local environment"""
from cinema import CinemaSchedule

import unittest


class TestCinemaList(unittest.TestCase):

    # def test_extract_gv_schedule(self):
    #     self.cinema_schedule = CinemaSchedule('gv')
    #     self.cinema_schedule.get_gv_schedule()

    def test_extract_cathay_schedule(self):
        self.cinema_schedule = CinemaSchedule('cathay')
        self.cinema_schedule.get_cathay_schedule()

    # def test_extract_sb_schedule(self):
    #     self.cinema_schedule = CinemaSchedule('sb')
    #     self.cinema_schedule.get_sb_schedule()
