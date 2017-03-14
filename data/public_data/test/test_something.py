from data.etl.extractor import Extractor

import unittest


class TestMovieRating(unittest.TestCase):

    test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                    'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869', 'tt0000019',
                    'tt0000025', 'tt0010781', 'tt0000481', 'tt0000012', 'tt0000399', 'tt0039624', 'tt0030298',
                    'tt0039445']

    def __init__(self, *args, **kwargs):
        super(TestMovieRating, self).__init__(*args, **kwargs)

    def test_extract_movie_rating(self):
        data_model = Extractor(None).extract_movie_rating(self.test_id_list[0])
        for item in data_model:
            self.assertEqual(item['movie_id'], 'tt0000001')
            if item['source_id'] == 1:
                self.assertEqual(item['votes'], '1232')
                self.assertEqual(item['score'], '5.8')
            if item['source_id'] == 2:
                self.assertEqual(item['votes'], '164')
                self.assertEqual(item['score'], '7.1')
            if item['source_id'] == 3:
                self.assertEqual(item['votes'], '9')
                self.assertEqual(item['score'], '4.66667')