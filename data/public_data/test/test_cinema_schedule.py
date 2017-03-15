from cinema import CinemaSchedule, CinemaList

import unittest


class TestCinemaSchedule(unittest.TestCase):

    def setUp(self):
        self.gv_schedule = CinemaSchedule('GV Tiong Bahru', 'https://www.gv.com.sg/GVCinemaDetails#/cinema/03', "gv")
        self.cathay_schedule = CinemaSchedule('The Cathay Cineplex', 'http://www.cathaycineplexes.com.sg/showtimes/',
                                              "cathay")
        self.shaw_schedule = CinemaSchedule('Shaw Theatres Lido', 'http://www.shaw.sg/sw_buytickets.aspx?'
                                                                  'filmCode=&cplexCode=30 210 236 39 155 56 75 124 '
                                                                    '123 77 76 246 36 85 160 0&date=', "sb")
        self.cinema_list = CinemaList()

    def test_convert_12_to_24_hour(self):
        # to be added in more test cases
        self.assertEqual(self.gv_schedule._convert_12_to_24_hour_time("8:25pm"), "20:25:00")

    def test_movie_title_parser(self):
        # gv
        self.assertEqual(self.gv_schedule._movie_title_parser("Logan*"), ("Logan", ["No free pass"]))

        # cathay
        self.assertEqual(self.cathay_schedule._movie_title_parser("*Hidden Figures PG (Dolby Digital)"),
                         ("Hidden Figures", ["Dolby Digital"]))
        self.assertEqual(self.cathay_schedule._movie_title_parser("*T2 Trainspotting R21 (Dolby Digital)"),
                         ("T2 Trainspotting", ["Dolby Digital"]))
        self.assertEqual(self.cathay_schedule._movie_title_parser("Fifty Shades Darker R21 (Dolby Digital)"),
                         ("Fifty Shades Darker", ["Dolby Digital"]))
        self.assertEqual(self.cathay_schedule._movie_title_parser("John Wick : Chapter 2 M18 (Dolby Digital)"),
                         ("John Wick : Chapter 2", ["Dolby Digital"]))
        self.assertEqual(self.cathay_schedule._movie_title_parser("*Before I Fall PG13 (Dolby Digital)"),
                         ("Before I Fall", ["Dolby Digital"]))

        # shaw
        self.assertEqual(self.shaw_schedule._movie_title_parser("Logan [D]"),
                         ("Logan", ["Digital"]))
        self.assertEqual(self.shaw_schedule._movie_title_parser("Siew Lup [M] [D]"),
                         ("Siew Lup", ['Digital']))
        self.assertEqual(self.shaw_schedule._movie_title_parser("Jackie [D]"),
                         ("Jackie", ["Digital"]))
        self.assertEqual(self.shaw_schedule._movie_title_parser("Hidden Figures [D]"),
                         ("Hidden Figures", ["Digital"]))
        self.assertEqual(self.shaw_schedule._movie_title_parser("Logan [IMAX]"),
                         ("Logan", ["IMAX"]))
        self.assertEqual(self.shaw_schedule._movie_title_parser("John Wick: Chapter 2 [D]"),
                         ("John Wick: Chapter 2", ["Digital"]))
        self.assertEqual(self.shaw_schedule._movie_title_parser("The Lego Batman Movie [D]"),
                         ("The Lego Batman Movie", ["Digital"]))



