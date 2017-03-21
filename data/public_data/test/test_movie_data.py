from movie import MovieData
from utils import InvalidMovieTypeException

import unittest


class TestMovieData(unittest.TestCase):

    test_id_list = ['tt2771200', 'tt3227946', 'tt3271078', 'tt6023350', 'tt0068918', 'tt0125590',
                    'tt0378422', 'tt2016315', 'tt0141399', 'tt0142231', 'tt3107288', 'tt0034517']

    def test_extract_title_and_year(self):

        def helper_extract_title_and_year(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_title_and_year(), expected)

        helper_extract_title_and_year(self.test_id_list[0], ('Beauty and the Beast', 2017))
        helper_extract_title_and_year(self.test_id_list[1], ('Death Test', None))

    def test_extract_poster(self):

        def helper_extract_poster(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_poster(), expected)

        helper_extract_poster(self.test_id_list[0], "https://images-na.ssl-images-amazon.com/"
                                                    "images/M/MV5BMTUwNjUxMTM4NV5BMl5BanBnXkFtZTgwODExMDQzMTI@._"
                                                    "V1_UX182_CR0,0,182,268_AL_.jpg")
        helper_extract_poster(self.test_id_list[2], None)

    def test_extract_credits(self):

        def helper_extract_credits(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_credits(), expected)

        # test single actor, single director tt6023350
        helper_extract_credits(self.test_id_list[3], ('Ben Leonberg', 'Ben Leonberg'))

        # test multiple directors tt0068918
        helper_extract_credits(self.test_id_list[4], ('Mary Brunner, Vincent Bugliosi, Bruce Davis',
                                                      'Robert Hendrickson, Laurence Merrick'))

        # test null actors tt3227946
        helper_extract_credits(self.test_id_list[5], (None, 'Hsiao-Ming Hsu'))

        # test null directors tt0378422
        helper_extract_credits(self.test_id_list[6], ('Tonton Gutierrez, Sheila Ysrael', None))

        # test both null tt2016315
        helper_extract_credits(self.test_id_list[7], (None, None))

    def test_extract_plot(self):

        def helper_extract_plot(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_plot(), expected)

        helper_extract_plot(self.test_id_list[0], 'An adaptation of the Disney fairy tale about '
                                                  'a monstrous-looking prince and a young woman who fall in love.')
        helper_extract_plot(self.test_id_list[5], None)

    def test_extract_rated(self):

        def helper_extract_rated(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_rated(), expected)

        helper_extract_rated(self.test_id_list[0], 'PG')
        helper_extract_rated(self.test_id_list[1], None)
        helper_extract_rated(self.test_id_list[8], 'R')
        helper_extract_rated(self.test_id_list[9], 'PG-13')

    def test_extract_release(self):

        def helper_extract_release(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_release(), expected)

        # date, country, type
        helper_extract_release(self.test_id_list[0], ('2017-03-16', 'Singapore', 'movie'))
        helper_extract_release(self.test_id_list[1], (None, None, 'movie'))
        helper_extract_release(self.test_id_list[2], ('2016-04-08', 'USA', 'movie'))
        helper_extract_release(self.test_id_list[3], (None, None, 'movie'))

        def helper_extract_release_error(imdb_id):
            data_model = MovieData(imdb_id, test=True)
            with self.assertRaises(InvalidMovieTypeException):
                data_model._extract_release()

        # exceptions tt3107288
        helper_extract_release_error(self.test_id_list[10])

    def test_extract_genre(self):

        def helper_extract_genre(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_genre(), expected)

        helper_extract_genre(self.test_id_list[0], 'Family, Fantasy, Musical')
        helper_extract_genre(self.test_id_list[1], 'Sci-Fi, Thriller')
        helper_extract_genre(self.test_id_list[11], None)

    def test_extract_runtime(self):

        def helper_extract_runtime(imdb_id, expected):
            data_model = MovieData(imdb_id, test=True)
            self.assertEqual(data_model._extract_runtime(), expected)

        helper_extract_runtime(self.test_id_list[0], 129)
        helper_extract_runtime(self.test_id_list[1], 110)
        helper_extract_runtime(self.test_id_list[4], 83)
        helper_extract_runtime(self.test_id_list[6], None)

if __name__ == '__main__':
    unittest.main()
