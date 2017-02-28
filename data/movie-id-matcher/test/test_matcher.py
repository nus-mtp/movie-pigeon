from matcher import MovieIDMatcher

import unittest


class TestMovieIDMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = MovieIDMatcher("Collide")  # any name

    def test_extract_imdb_possible(self):

        def helper(title, expect_result):
            matcher = MovieIDMatcher(title)
            test_result = matcher.extract_imdb_possible()
            self.assertEqual(test_result, expect_result)

        helper("Collide", [
            ("tt2126235", "Collide (I) (2016)"),
            ("tt2834052", "Collide"),
            ("tt1230120", "Collide (II) (2010)")
        ])

        helper("Cook up a storm", [
            ("tt6315750", "Cook Up a Storm (2017)")
        ])

        helper("Kung Fu Yoga", [
            ('tt4217392', 'Kung-Fu Yoga (2017)\naka "Kung Fu Yoga"')
        ])

        helper("The Lego Batman Movie", [
            ('tt4116284', 'The LEGO Batman Movie (2017)')
        ])

        helper("Rings", [
            ('tt0498381', 'Rings (2017)'),
            ('tt0152191', 'Rings (1993)')
        ])

        helper("Hidden Figures", [
            ('tt4846340', 'Hidden Figures (2016)')
        ])

        helper("Sleepless", [
            ('tt2072233', 'Sleepless (III) (2017)'),
            ('tt0220827', 'Sleepless (2001)'),
            ('tt5039992', 'Sleepless (II) (2017)')
        ])

        helper("Fist Fight", [
            ('tt3401882', 'Fist Fight (2017)')
        ])

        helper("Siew Lup", [
            ('tt6550794', 'Siew Lup (2017)')
        ])

        helper("Jackie", [
            ('tt1619029', 'Jackie (V) (2016)'),
            ('tt2108546', 'Jackie (II) (2012)'),
            ('tt5249954', 'Jackie')
        ])

        helper("John Wick", [
            ('tt2911666', 'John Wick (2014)')
        ])

        helper("Resident Evil: The Final Chapter", [
            ('tt2592614', 'Resident Evil: The Final Chapter (2016)')
        ])

    def test_parse_imdb_search_text(self):
        self.assertEqual(
            self.matcher._parse_imdb_search_text("Collide (I) (2016)"), (["Collide"], ["I", "2016"]))
        self.assertEqual(
            self.matcher._parse_imdb_search_text("Collide (2017) (Short)"), (["Collide"], ["2017", "Short"]))
        self.assertEqual(
            self.matcher._parse_imdb_search_text("Cook Up a Storm (2017)"), (["Cook Up a Storm"], ["2017"]))
        self.assertEqual(
            self.matcher._parse_imdb_search_text("Cooking Up a Storm (2015) (TV Episode)"),
            (["Cooking Up a Storm"], ["2015", "TV Episode"]))
        self.assertEqual(
            self.matcher._parse_imdb_search_text('The King of Queens (1998) (TV Series) aka "Kung av Queens"'),
            (["The King of Queens", "Kung av Queens"], ["1998", "TV Series"]))
        self.assertEqual(
            self.matcher._parse_imdb_search_text('Kung-Fu Yoga (2017)\naka "Kung Fu Yoga"'),
            (["Kung-Fu Yoga", "Kung Fu Yoga"], ["2017"]))