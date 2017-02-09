from urllib import request, error
from bs4 import BeautifulSoup
import json
import html
import datetime
import data.utils as utils
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
    metacritic_url_format = "http://www.metacritic.com/search/movie/{}/results"

    def __init__(self, logger):
        self.logger = logger

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

    def extract_imdb_data(self, movie_id):
        """
        given imdb_id, return the current rating and total number of votes of this movie in imdb database
        :param movie_id:
        :return: rating and votes in STRING format or False if it is a bad request
        """
        url = self.imdb_url_format.format(movie_id)
        try:
            request_result = request.urlopen(url).read()
        except error.HTTPError:
            self.logger.warning("Movie id is not valid:" + movie_id)
            return False

        soup = BeautifulSoup(request_result, "lxml")

        # title, production year
        title_wrapper = soup.find("h1").text.split("\xa0")
        title = title_wrapper[0]
        production_year = title_wrapper[1][1: -2]

        # rated, runtime, genre, released, country
        rated, runtime, genre, release_country = None, None, None, None  # initialisation
        subtext = soup.find("div", {"class": "subtext"}).text.replace("\n", "").strip().split("|")  # unpack subtext

        if len(subtext) == 3:
            runtime, genre, release_country = subtext
        elif len(subtext) == 2:  # either runtime + genre or genre + release_country
            if 'min' in subtext[0]:  # runtime plus genre
                runtime, genre = subtext
            else:
                genre, release_country = subtext
        elif len(subtext) == 1:
            genre = subtext[0]
            release_country = None
        elif len(subtext) == 4:
            rated, runtime, genre, release_country = subtext
        else:
            print(subtext)
            raise Exception("Examine the output")

        if runtime is not None:
            runtime = runtime.replace("min", "").strip()

        if release_country is not None:
            released, country = release_country.replace(")", "").split("(")
            released = released.strip()  # remove last white space
            length_of_date = len(released.split(" "))
            if length_of_date == 3:
                released = datetime.datetime.strptime(released, '%d %B %Y').strftime('%Y-%m-%d')
            elif length_of_date == 2:
                released = datetime.datetime.strptime(released, '%B %Y').strftime('%Y-%m-%d')
            elif length_of_date == 1:
                released = datetime.datetime.strptime(released, '%Y').strftime('%Y-%m-%d')
        else:
            released = None
            country = None

        # plot
        plot = soup.find("div", {"class": "summary_text"}).text.replace("\n", "").strip().split("    ")[0]
        if "Add a Plot" in plot:
            plot = None

        # actors, poster_url, director
        credits = soup.find_all("div", {"class": "credit_summary_item"})
        director, actor = None, None
        for item in credits:
            current_text = item.text
            if "Directors:" in current_text:
                director = current_text.replace("Directors:", "").replace("\n", "").replace("  ", "")
            elif "Director:" in current_text:
                director = current_text.replace("Director:", "").strip()
            elif "Stars" in current_text:
                actor = current_text.replace("Stars:", "").replace("\n", "").replace("  ", "")
            elif "Star" in current_text:
                actor = current_text.replace("Star:", "").strip()

        # poster_url
        poster = soup.find("div", {"class": "poster"})
        try:
            poster_url = poster.find("img")['src']
        except AttributeError:
            self.logger.warning("No poster for movie id: " + movie_id)
            poster_url = None

        movie_data = utils.get_movie_data_dict(actor, country, director, genre, movie_id, None,
                                               plot, poster_url, production_year, rated, released, runtime, title, None)

        return movie_data

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
    def extract_trakt_rating(self, movie_id):
        """
        given imdb_id, return the current rating and total number of votes of this movie in trakt.tv database
        :param movie_id:
        :return: rating and votes in STRING format
        """
        request_result = request.Request('https://api.trakt.tv/movies/{}/ratings'.format(movie_id),
                                          headers=self.trakt_header)
        try:
            json_result = json.loads(request.urlopen(request_result).read().decode("utf-8"))
        except error.HTTPError:
            self.logger.error("Rating is not available in Trakt")
            return None, None

        return str(json_result['rating']), str(json_result['votes'])

    def extract_imdb_rating(self, movie_id):
        """
        given imdb_id, return the current rating and total number of votes of this movie in imdb database
        :param movie_id:
        :return: rating and votes in STRING format
        """
        url = self.imdb_url_format.format(movie_id)
        request_result = request.urlopen(url).read()
        soup = BeautifulSoup(request_result, "lxml")
        div = soup.find('div', {'class': 'ratingValue'})

        try:
            parse_list = div.find("strong")['title'].split(" based on ")
        except AttributeError:
            self.logger.error("Rating is not available in IMDb.")
            return None, None

        rating = parse_list[0]
        votes = parse_list[1].split(" ")[0].replace(",", "")
        return rating, votes

    def extract_douban_rating(self, movie_id):
        """
        given imdb_id, return the current rating and total number of votes of this movie in douban database
        :param movie_id:
        :return: rating and votes in STRING format
        """
        url = self.douban_url_format.format(movie_id)
        request_result = request.urlopen(url).read()
        soup = BeautifulSoup(request_result, "lxml")

        try:
            rating = soup.find("span", {'class': 'rating_nums'}).text
            votes = soup.find("span", {'class': 'pl'}).text.replace("人评价","")[1: -1].replace(",", "")  # remove parenthesis and words
        except AttributeError:
            self.logger.error("Rating is not available in Douban.")
            return None, None

        return rating, votes

    def extract_metacritic_rating(self, imdb_id, search_string, director, release_date):
        # bad request, on hold, need to use selenium
        url = self.metacritic_url_format.format(html.escape(search_string))
        call_result = request.urlopen(url).read()
        soup = BeautifulSoup(call_result, "lxml")
        results = soup.find('li', {'class': 'result'})
        print(results)
        pass

    def extract_rotten_tomatoes_rating(self, imdb_id):
        pass

    def extract_letterboxd_rating(self, movie_id):
        pass

# test
if __name__ == '__main__':
    extractor = Extractor()
    extractor.extract_imdb_data("tt0000001")
