from urllib import request

import requests
import logging
import json

class Extractor:

    trakt_header = {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }

    def __init__(self):
        pass

    def extract_trakt(self):
        api_call_result = request.Request('https://api.trakt.tv/movies/tt4972582', headers=self.trakt_header)
        print(request.urlopen(api_call_result).read())
        logging.warning("haha")
        pass

    def extract_omdb(self):
        api_call_result = request.urlopen("http://www.omdbapi.com/?i=tt4972582&plot=full&r=json")
        print(api_call_result.read().decode("utf-8"))

    def extract_imdb(self):
        pass

    def extract_letterboxd(self):
        pass


if __name__ == '__main__':
    extractor = Extractor()
    extractor.extract_omdb()
