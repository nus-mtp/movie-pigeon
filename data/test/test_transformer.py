import unittest
from data.etl.transformer import Transformer


class TestTransformer(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTransformer, self).__init__(*args, **kwargs)
        self.transformer = Transformer(None)

    def test_split_release_and_country_imdb(self):
        self.assertEqual(self.transformer.split_release_and_country_imdb("19 January 2016 (Germany)"),
                         ("19 January 2016", "Germany"))
        self.assertEqual(self.transformer.split_release_and_country_imdb("January 2016 (Germany)"),
                         ("January 2016", "Germany"))
        self.assertEqual(self.transformer.split_release_and_country_imdb("2016 (Germany)"),
                         ("2016", "Germany"))
        self.assertEqual(self.transformer.split_release_and_country_imdb("    2016 (Germany)"),
                         ("2016", "Germany"))
        self.assertEqual(self.transformer.split_release_and_country_imdb("    2016     "),
                         ("2016", None))

    def test_transform_date_imdb(self):
        self.assertEqual(self.transformer.transform_date_imdb("19 January 2016"), "2016-01-19")
        self.assertEqual(self.transformer.transform_date_imdb("1 January 2016"), "2016-01-01")
        self.assertEqual(self.transformer.transform_date_imdb("01 January 2016"), "2016-01-01")
        self.assertEqual(self.transformer.transform_date_imdb("February 2016"), "2016-01-01")
        self.assertEqual(self.transformer.transform_date_imdb("2016"), "2016-01-01")

    def test_transform_time_imdb(self):
        self.assertEqual(self.transformer.transform_time_imdb("40min"), "40")
        self.assertEqual(self.transformer.transform_time_imdb("1h40min"), "100")
        self.assertEqual(self.transformer.transform_time_imdb("1h"), "60")
        self.assertEqual(self.transformer.transform_time_imdb("2h40min"), "160")
        self.assertEqual(self.transformer.transform_time_imdb("1h   40min   "), "100")
        self.assertEqual(self.transformer.transform_time_imdb("1h   40min"), "100")

if __name__ == '__main__':
    unittest.main()
