from urllib import request
import logging
import json


class Extractor:

    trakt_header = {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }

    def __init__(self):
        self.content_type = "json"  # return type for omdb requests
        self.plot = "full"  # attribute for omdb
        pass

    # ==========
    #   data
    # ==========
    def extract_omdb_data(self, imdb_id):
        """
        :param imdb_id: a given imdb id
        :return: json result of its movie data
        """
        api_call_result = request.urlopen(
            "http://www.omdbapi.com/?i={}&plot={}&r={}".format(imdb_id, self.plot, self.content_type))
        text_result = api_call_result.read().decode("utf-8")
        json_result = json.loads(text_result)
        return json_result

    # ==========
    #   rating
    # ==========
    def extract_trakt_rating(self, imdb_id):
        api_call_result = request.Request('https://api.trakt.tv/movies/{}/rating'.format(imdb_id),
                                          headers=self.trakt_header)
        print(request.urlopen(api_call_result).read())
        pass

    def extract_imdb_rating(self):
        pass

    def extract_letterboxd_rating(self):
        pass

    def extract_metacritic_rating(self):
        pass

    def extract_rotten_tomatoes_rating(self):
        pass

    def extract_douban_rating(self):
        pass


if __name__ == '__main__':
    extractor = Extractor()
    extractor.extract_trakt_rating()
