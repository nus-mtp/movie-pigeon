import unittest
import os

from movie import MovieData


class TestMovieData(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                    'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869', 'tt0000019',
                    'tt0000025', 'tt0010781', 'tt0000481', 'tt0000012', 'tt0000399', 'tt0039624', 'tt0030298',
                    'tt0039445']

    def test_extract_title_and_year(self):
        """
        test the extractor of movie title and production year
        1. title is not nullable
        2. production year is nullable
        :return:
        """

        def helper(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_title_and_year(), expected)
            io_wrapper.close()

        helper(self.test_id_list[0], ('Carmencita', 1894))
        helper(self.test_id_list[7], ('La La Land', 2016))

    def test_extract_poster(self):
        """
        test the extractor of movie poster url
        1. url is nullable
        :return:
        """

        def helper(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")

            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_poster(), expected)
            io_wrapper.close()

        helper(self.test_id_list[0],
                    "https://images-na.ssl-images-amazon.com/images/"
                    "M/MV5BMjAzNDEwMzk3OV5BMl5BanBnXkFtZTcwOTk4OTM5Ng@@._V1_UY268_CR6,0,182,268_AL_.jpg")
        helper(self.test_id_list[13], None)
        helper(self.test_id_list[14], None)

    def test_extract_credits(self):
        """
        test the extractor of credits
        1. actors can be nullable, one token or multiple tokens
        2. directors can be nullable, one token or multiple tokens
        :return:
        """

        def helper_test(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_credits(), expected)
            io_wrapper.close()

        helper_test(self.test_id_list[16], (None, None))
        helper_test(self.test_id_list[14], (None, "Birt Acres"))
        helper_test(self.test_id_list[17], (None, "Auguste Lumière, Louis Lumière"))
        helper_test(self.test_id_list[0], ("Carmencita", "William K.L. Dickson"))
        helper_test(self.test_id_list[18], ("Thomas White", "George S. Fleming, Edwin S. Porter"))
        helper_test(self.test_id_list[15], ("Ruth Roland, George Larkin, Mark Strong", "Robert Ellis, Louis J. Gasnier"))

    def test_extract_plot(self):
        """
        test plot
        :return:
        """

        def helper_test(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_plot(), expected)
            io_wrapper.close()

        helper_test(self.test_id_list[0], "Performing on what looks like a small wooden stage, wearing a dress with a "
                                          "hoop skirt and white high-heeled pumps, Carmencita does a dance with kicks "
                                          "and twirls, a smile always on her face.")

    def test_extract_rated(self):
        """
        test the rated token
        :return:
        """

        def helper_test(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_rated(), expected)
            io_wrapper.close()

        helper_test(self.test_id_list[0], "NOT RATED")

    def test_extract_release(self):
        """
        test the release token of subtext
        :return:
        """

        def helper_test(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_release(), expected)
            io_wrapper.close()

        helper_test(self.test_id_list[0], ('1894-03-10', 'USA', 'movie'))
        helper_test(self.test_id_list[7], ('2016-12-25', 'USA', 'movie'))
        helper_test(self.test_id_list[8], ('1892-10-28', 'France', 'movie'))
        helper_test(self.test_id_list[9], (None, None, 'movie'))
        helper_test(self.test_id_list[10], (None, None, 'movie'))
        helper_test(self.test_id_list[11], ('1913-01-10', 'Germany', 'movie'))
        helper_test(self.test_id_list[12], (None, None, 'movie'))

    def test_extract_genre(self):
        """
        test the genre token of subtext
        :return:
        """

        def helper_test(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_genre(), expected)
            io_wrapper.close()

        helper_test(self.test_id_list[0], 'Documentary, Short')
        helper_test(self.test_id_list[12], None)

    def test_extract_runtime(self):
        """
        test runtime
        :return:
        """

        def helper_test(imdb_id, expected):
            """
            takes in imdb id and the tuple of expected result
            :param imdb_id:
            :param expected:
            :return:
            """
            data_model = MovieData("mock-id")
            test_data_directory = os.path.realpath(
                os.path.join(os.getcwd(), "data_movie_data/{}.html".format(imdb_id)))
            io_wrapper = open(test_data_directory, encoding="utf8")
            data_model._build_soup_for_test(io_wrapper)
            data_model._extract_process()
            self.assertEqual(data_model._extract_runtime(), expected)
            io_wrapper.close()

        helper_test(self.test_id_list[0], 1)
        helper_test(self.test_id_list[12], None)

if __name__ == '__main__':
    unittest.main()
