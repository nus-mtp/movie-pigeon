from matcher import MovieIDMatcher

import unittest


class TestMovieIDMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = MovieIDMatcher()

    @unittest.skip  # test skipped for CI, tested using IDE
    def test_get_search_results(self):

        def helper_get_search_results(title, expect_result):
            matcher = MovieIDMatcher()
            test_result = matcher._get_search_results(title)
            self.assertEqual(test_result, expect_result)

        helper_get_search_results("Collide", [
            ("tt2126235", "Collide (I) (2016)"),
            ("tt2834052", "Collide"),
            ("tt1230120", "Collide (II) (2010)")
        ])

        helper_get_search_results("Cook up a storm", [
            ("tt6315750", "Cook Up a Storm (2017)")
        ])

        helper_get_search_results("Kung Fu Yoga", [
            ('tt4217392', 'Gong fu yu jia (2017)\naka "Kung Fu Yoga"')
        ])

        helper_get_search_results("The Lego Batman Movie", [
            ('tt4116284', 'The LEGO Batman Movie (2017)')
        ])

        helper_get_search_results("Rings", [
            ('tt0498381', 'Rings (2017)'),
            ('tt0152191', 'Rings (1993)')
        ])

        helper_get_search_results("Hidden Figures", [
            ('tt4846340', 'Hidden Figures (2016)')
        ])

        helper_get_search_results("Sleepless", [
            ('tt2072233', 'Sleepless (III) (2017)'),
            ('tt0220827', 'Sleepless (2001)'),
            ('tt5039992', 'Sleepless (II) (2017)')
        ])

        helper_get_search_results("Fist Fight", [
            ('tt3401882', 'Fist Fight (2017)')
        ])

        helper_get_search_results("Siew Lup", [
            ('tt6550794', 'Siew Lup (2017)')
        ])

        helper_get_search_results("Jackie", [
            ('tt1619029', 'Jackie (V) (2016)'),
            ('tt2108546', 'Jackie (II) (2012)'),
            ('tt5249954', 'Jackie')
        ])

        helper_get_search_results("John Wick: Chapter 2", [
            ('tt4425200', 'John Wick: Chapter 2 (2017)')
        ])

        helper_get_search_results("John Wick : Chapter 2", [
            ('tt4425200', 'John Wick: Chapter 2 (2017)')
        ])

        helper_get_search_results("Resident Evil: The Final Chapter", [
            ('tt2592614', 'Resident Evil: The Final Chapter (2016)')
        ])

        helper_get_search_results("Let's Go Jets", [
            ('tt5693562', 'Chiadan: Joshi kousei ga chiadansu de zenbei seihashichatta honto no hanashi (2017)')
        ])

        helper_get_search_results("Motta Siva Ketta Siva", [
            ('tt6495714', 'Motta Shiva Ketta Shiva (2017)')
        ])

    @unittest.skip  # test skipped for CI, tested using IDE
    def test_match_imdb_id_from_title_recent(self):

        def helper_match_imdb_id_from_title_recent(title, expect_result):
            test_result = self.matcher.match_imdb_id_from_title_recent(title)
            self.assertEqual(test_result, expect_result)

        helper_match_imdb_id_from_title_recent("Collide", "tt2126235")
        helper_match_imdb_id_from_title_recent("Cook up a storm", "tt6315750")
        helper_match_imdb_id_from_title_recent("Kung Fu Yoga", 'tt4217392')
        helper_match_imdb_id_from_title_recent("The Lego Batman Movie", 'tt4116284')
        helper_match_imdb_id_from_title_recent("Rings", 'tt0498381')
        helper_match_imdb_id_from_title_recent("Let's go, Jets", "tt5693562")
        helper_match_imdb_id_from_title_recent("Power Rangers", "tt3717490")
        helper_match_imdb_id_from_title_recent("Life", "tt5442430")

    def test_parse_search_text(self):
        self.assertEqual(self.matcher._parse_search_text("Power Rangers"), "power rangers")
        self.assertEqual(self.matcher._parse_search_text("Life"), "life")
        self.assertEqual(self.matcher._parse_search_text("Don't Knock Twice"), "don't knock twice")
        self.assertEqual(self.matcher._parse_search_text("Let's Go Jets"), "let's go jets")
        self.assertEqual(self.matcher._parse_search_text("    Power Rangers   "), "power rangers")
        self.assertEqual(self.matcher._parse_search_text("Power : Rangers"), "power: rangers")
        self.assertEqual(self.matcher._parse_search_text("John Wick: Chapter 2"), "john wick: chapter 2")
        self.assertEqual(self.matcher._parse_search_text("John Wick : Chapter 2"), "john wick: chapter 2")

    def test_parse_search_results(self):
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

    def test_build_exact_search_url(self):
        self.assertEqual(
            self.matcher._build_exact_search_url("power rangers"),
            "http://www.imdb.com/find?&q=power rangers&s=tt&ttype=ft&exact=true"
        )
        self.assertEqual(
            self.matcher._build_exact_search_url(1),
            "http://www.imdb.com/find?&q=1&s=tt&ttype=ft&exact=true"
        )
        self.assertEqual(
            self.matcher._build_exact_search_url("let's go, jet"),
            "http://www.imdb.com/find?&q=let's go, jet&s=tt&ttype=ft&exact=true"
        )
        self.assertEqual(
            self.matcher._build_exact_search_url(" 3 12 y 12"),
            "http://www.imdb.com/find?&q= 3 12 y 12&s=tt&ttype=ft&exact=true"
        )

    def test_build_fuzzy_search_url(self):
        self.assertEqual(
            self.matcher._build_fuzzy_search_url("power rangers"),
            "http://www.imdb.com/find?q=power rangers&s=tt&ref_=fn_tt"
        )
        self.assertEqual(
            self.matcher._build_fuzzy_search_url("adfs%dqd"),
            "http://www.imdb.com/find?q=adfs%dqd&s=tt&ref_=fn_tt"
        )
        self.assertEqual(
            self.matcher._build_fuzzy_search_url("let's go, jet"),
            "http://www.imdb.com/find?q=let's go, jet&s=tt&ref_=fn_tt"
        )
        self.assertEqual(
            self.matcher._build_fuzzy_search_url(" 3 12 y 12"),
            "http://www.imdb.com/find?q= 3 12 y 12&s=tt&ref_=fn_tt"
        )

    def test_is_recent(self):
        self.assertEqual(self.matcher._is_recent(["I", "2016"]), True)
        self.assertEqual(self.matcher._is_recent(["2012", "Short"]), False)
        self.assertEqual(self.matcher._is_recent(["2015", "TV Episode"]), False)
        self.assertEqual(self.matcher._is_recent(["2017", "TV Episode"]), True)
        self.assertEqual(self.matcher._is_recent(["2018", "TV Episode"]), True)

    def test_is_correct_type(self):
        self.assertEqual(self.matcher._is_correct_type(["I", "2016"]), True)
        self.assertEqual(self.matcher._is_correct_type(["2012", "Short"]), False)
        self.assertEqual(self.matcher._is_correct_type(["2015", "TV Episode"]), False)

if __name__ == '__main__':
    unittest.main()

