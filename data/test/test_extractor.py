import unittest
import random
import data.utils as utils


class TestExtractor(unittest.TestCase):

    test_id_list = []

    def __init__(self, *args, **kwargs):
        super(TestExtractor, self).__init__(*args, **kwargs)
        for i in range(0, 10):
            testing_movie_id_numeric = random.randint(1, 9999999)
            testing_movie_id = utils.imdb_id_builder(testing_movie_id_numeric)
            self.test_id_list.append(testing_movie_id)


    def test_test(self):
        self.assertEqual("1", "1")


