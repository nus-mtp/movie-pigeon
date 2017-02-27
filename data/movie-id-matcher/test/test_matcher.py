from matcher import MovieIDMatcher

import unittest


class TestMovieIDMatcher(unittest.TestCase):

    def setUp(self):
        pass

    def test_extract_imdb_possible(self):

        def helper(title, expect_result):
            matcher = MovieIDMatcher(title)
            test_result = matcher.extract_imdb_possible()
            self.assertEqual(test_result, expect_result)

        helper("Collide", [
            ("tt2126235", "Collide (I) (2016)"),
            ("tt2834052", "Collide"),
            ("tt6260070", "Collide (2017) (Short)")
        ])

        helper("Cook up a storm", [
            ("tt6315750", "Cook Up a Storm (2017)"),
            ("tt4546976", "Cooking Up a Storm (2015) (TV Episode)"),
            ("tt0723671", "Storming Up a Cook (2002) (TV Episode)")
        ])

