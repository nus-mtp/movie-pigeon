from matcher import MovieIDMatcher

import unittest


class TestMovieIDMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = MovieIDMatcher()

    @unittest.skip  # test skipped for CI, tested using IDE
    def test_extract_imdb_possible(self):

        def helper_extract_imdb_possible(title, expect_result):
            matcher = MovieIDMatcher()
            test_result = matcher._extract_imdb_possible(title)
            self.assertEqual(test_result, expect_result)

        helper_extract_imdb_possible("Collide", [
            ("tt2126235", "Collide (I) (2016)"),
            ("tt2834052", "Collide"),
            ("tt1230120", "Collide (II) (2010)")
        ])

        helper_extract_imdb_possible("Cook up a storm", [
            ("tt6315750", "Cook Up a Storm (2017)")
        ])

        helper_extract_imdb_possible("Kung Fu Yoga", [
            ('tt4217392', 'Gong fu yu jia (2017)\naka "Kung Fu Yoga"')
        ])

        helper_extract_imdb_possible("The Lego Batman Movie", [
            ('tt4116284', 'The LEGO Batman Movie (2017)')
        ])

        helper_extract_imdb_possible("Rings", [
            ('tt0498381', 'Rings (2017)'),
            ('tt0152191', 'Rings (1993)')
        ])

        helper_extract_imdb_possible("Hidden Figures", [
            ('tt4846340', 'Hidden Figures (2016)')
        ])

        helper_extract_imdb_possible("Sleepless", [
            ('tt2072233', 'Sleepless (III) (2017)'),
            ('tt0220827', 'Sleepless (2001)'),
            ('tt5039992', 'Sleepless (II) (2017)')
        ])

        helper_extract_imdb_possible("Fist Fight", [
            ('tt3401882', 'Fist Fight (2017)')
        ])

        helper_extract_imdb_possible("Siew Lup", [
            ('tt6550794', 'Siew Lup (2017)')
        ])

        helper_extract_imdb_possible("Jackie", [
            ('tt1619029', 'Jackie (V) (2016)'),
            ('tt2108546', 'Jackie (II) (2012)'),
            ('tt5249954', 'Jackie')
        ])

        helper_extract_imdb_possible("John Wick: Chapter 2", [
            ('tt4425200', 'John Wick: Chapter 2 (2017)')
        ])

        helper_extract_imdb_possible("John Wick : Chapter 2", [
            ('tt4425200', 'John Wick: Chapter 2 (2017)')
        ])

        helper_extract_imdb_possible("Resident Evil: The Final Chapter", [
            ('tt2592614', 'Resident Evil: The Final Chapter (2016)')
        ])

        helper_extract_imdb_possible("Let's Go Jets", [
            ('tt5693562', 'Chiadan: Joshi kousei ga chiadansu de zenbei seihashichatta honto no hanashi (2017)')
        ])

        helper_extract_imdb_possible("Motta Siva Ketta Siva", [
            ('tt6495714', 'Motta Shiva Ketta Shiva (2017)')
        ])

    def test_parse_imdb_search_text(self):
        self.assertEqual(
            self.matcher._parse_search_results("Collide (I) (2016)"), (["Collide"], ["I", "2016"]))
        self.assertEqual(
            self.matcher._parse_search_results("Collide (2017) (Short)"), (["Collide"], ["2017", "Short"]))
        self.assertEqual(
            self.matcher._parse_search_results("Cook Up a Storm (2017)"), (["Cook Up a Storm"], ["2017"]))
        self.assertEqual(
            self.matcher._parse_search_results("Cooking Up a Storm (2015) (TV Episode)"),
            (["Cooking Up a Storm"], ["2015", "TV Episode"]))
        self.assertEqual(
            self.matcher._parse_search_results('The King of Queens (1998) (TV Series) aka "Kung av Queens"'),
            (["The King of Queens", "Kung av Queens"], ["1998", "TV Series"]))
        self.assertEqual(
            self.matcher._parse_search_results('Kung-Fu Yoga (2017)\naka "Kung Fu Yoga"'),
            (["Kung-Fu Yoga", "Kung Fu Yoga"], ["2017"]))

    def test_match_imdb_id(self):

        def helper(title, expect_result):
            matcher = MovieIDMatcher()
            test_result = matcher.match_imdb_id_from_title_recent(title)
            self.assertEqual(test_result, expect_result)

        helper("Collide", "tt2126235")
        helper("Cook up a storm", "tt6315750")
        helper("Kung Fu Yoga", 'tt4217392')
        helper("The Lego Batman Movie", 'tt4116284')
        helper("Rings", 'tt0498381')


