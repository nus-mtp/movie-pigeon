from matcher import MovieIDMatcher

import unittest


class TestMovieIDMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = MovieIDMatcher("Collide")

    # def test_extract_imdb_possible(self):
    #
    #     def helper(title, expect_result):
    #         matcher = MovieIDMatcher(title)
    #         test_result = matcher.extract_imdb_possible()
    #         self.assertEqual(test_result, expect_result)
    #
    #     helper("Collide", [
    #         ("tt2126235", "Collide (I) (2016)"),
    #         ("tt2834052", "Collide"),
    #         ("tt6260070", "Collide (2017) (Short)")
    #     ])
    #
    #     # helper("Cook up a storm", [
    #     #     ("tt6315750", "Cook Up a Storm (2017)"),
    #     #     ("tt4546976", "Cooking Up a Storm (2015) (TV Episode)"),
    #     #     ("tt0723671", "Storming Up a Cook (2002) (TV Episode)")
    #     # ])
    #
    #     helper("Kung Fu Yoga", [
    #         ('tt4217392', 'Kung-Fu Yoga (2017)'),
    #         ('tt0165581', 'The King of Queens (1998) (TV Series) aka "Kung av Queens"'),
    #         ('tt2267968', 'Kung Fu Panda 3 (2016)')
    #     ])
    #
    #     helper("The Lego Batman Movie", [])

    # def test_get_similarity(self):
    #     score = self.matcher._get_similarity("Collide", "Collide (I) (2016)")
    #     print(score)
    #     print("haha")
    #     self.assertTrue(score > 0.9)

    def test_parse_imdb_search_text(self):
        self.matcher._parse_imdb_search_text("Collide (I) (2016)")