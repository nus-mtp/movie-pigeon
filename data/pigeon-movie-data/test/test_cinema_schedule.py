from cinema import CinemaSchedule

import unittest


class TestCinemaSchedule(unittest.TestCase):

    def setUp(self):
        self.gv_schedule = CinemaSchedule(('1', 'GV Tiong Bahru', 'https://www.gv.com.sg/GVCinemaDetails#/cinema/03'))
        self.cathay_schedule = CinemaSchedule(('32', 'The Cathay Cineplex', 'http://www.cathaycineplexes.com.sg/showtimes/'))
        self.shaw_schedule = CinemaSchedule(('39', 'Shaw Theatres Lido', 'http://www.shaw.sg/sw_buytickets.aspx?'
                                                                    'filmCode=&cplexCode=30 210 236 39 155 56 75 124 '
                                                                    '123 77 76 246 36 85 160 0&date='))

    def test_extract_raw_golden_village(self):
        self.gv_schedule._extract_raw_golden_village()

    def test_convert_12_to_24_hour(self):
        self.assertEqual(self.gv_schedule._convert_12_to_24_hour_time("8:25pm"), "20:25:00")
