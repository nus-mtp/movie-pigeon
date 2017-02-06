from urllib import request
from bs4 import BeautifulSoup
import json


class Extractor:

    trakt_header = {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }

    wemakesites_api_key = "5a7e0693-af96-4d43-89a3-dc8ca00cf355"

    imdb_url_format = "http://www.imdb.com/title/{}/"

    # omdb setup
    omdb_plot_option = "full"  # attribute for omdb

    omdb_content_type = "json"  # return type for omdb requests

    # douban
    douban_url_format = "https://movie.douban.com/subject_search?search_text={}"

    def __init__(self):
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
            "http://www.omdbapi.com/?i={}&plot={}&r={}".format(imdb_id, self.omdb_plot_option, self.omdb_content_type))
        text_result = api_call_result.read().decode("utf-8")
        json_result = json.loads(text_result)
        return json_result

    def extract_imdb_data(self, imdb_id):
        """
        service on hold incase omdb is not going to back up
        :param imdb_id:
        :return:
        """
        json_result = 0
        return json_result

    def extract_wemakesites_data(self, imdb_id):
        """
        alternatives to omdb
        :param imdb_id:
        :return:
        """
        api_call_result = request.urlopen(
            "http://imdb.wemakesites.net/api/{}?api_key={}".format(imdb_id, self.wemakesites_api_key))
        text_result = api_call_result.read().decode("utf-8")
        json_result = json.loads(text_result)
        return json_result

    # ==========
    #   rating
    # ==========
    def extract_trakt_rating(self, imdb_id):
        """
        given imdb_id, return the current rating and total number of votes of this movie in trakt
        :param imdb_id:
        :return: rating and votes in string format
        """
        api_call_result = request.Request('https://api.trakt.tv/movies/{}/ratings'.format(imdb_id),
                                          headers=self.trakt_header)
        json_result = json.loads(request.urlopen(api_call_result).read().decode("utf-8"))
        return json_result['rating'], json_result['votes']

    def extract_imdb_rating(self, imdb_id):
        """
        given imdb_id, return the current rating and total number of votes of this movie in imdb
        :param imdb_id:
        :return: rating and votes in string format
        """
        url = self.imdb_url_format.format(imdb_id)
        content = request.urlopen(url).read()
        soup = BeautifulSoup(content, "lxml")
        div = soup.find('div', {'class': 'ratingValue'})
        parse_list = div.find("strong")['title'].split(" based on ")
        rating = parse_list[0]
        votes = parse_list[1].split(" ")[0]
        return rating, votes

    def extract_metacritic_rating(self, imdb_id, search_string, director, release_date):
        """
        given imdb_id and various validation info, return the correct current rating and total votes count of a movie
        :param imdb_id:
        :param search_string: movie title formatted according to source
        :param director:
        :param release_date:
        :return:
        """

        pass

    def extract_rotten_tomatoes_rating(self, imdb_id):
        pass

    def extract_douban_rating(self, movie_id):
        url = self.douban_url_format.format(movie_id)
        call_result = request.urlopen(url).read()
        soup = BeautifulSoup(call_result, "lxml")
        rating = soup.find("span", {'class': 'rating_nums'}).text
        votes = soup.find("span", {'class': 'pl'}).text.replace("人评价","")[1: -1]  # remove parenthesis and words
        return rating, votes


if __name__ == '__main__':
    extractor = Extractor()
    extractor.extract_douban_rating("tt0000001")
