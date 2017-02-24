from urllib import request, error
from bs4 import BeautifulSoup
from selenium import webdriver


import html


class MovieShowing:

    imdb_search_format = "http://www.imdb.com/find?&q={}"

    def __init__(self, cinema):
        self.driver = webdriver.PhantomJS()
        self.cinema_id, self.cinema_name, self.cinema_url = cinema

    def extract_cinema_schedule(self):
        """retrieve one cinema schedule based on the given url,
        return a list of dictionaries contains """
        # retrieve title, (type like 3D) and schedule time
        print(self.cinema_url)
        self.driver.get(self.cinema_url)

        # find imdb id
        # create tuple cinema_id, movie_id, type, schedule

    def extract(self):
        url = "http://www.imdb.com/find?&q=harry+potter+and+deathly+hallows"
        soup = BeautifulSoup(request.urlopen(url).read().decode("utf-8"), "lxml")
        anchors = soup.find_all("a")
        for item in anchors:
            try:
                current_href = item['href']
            except KeyError:
                continue
            if "/title" in current_href:
                print(current_href)

    def match(self):
        print(self.build_search_url("Tu ying dang an"))

    def build_search_url(self, search_title):
        search_query = html.escape(search_title.lower())
        return self.imdb_search_format.format(search_query)


if __name__ == '__main__':
    app = MovieShowing()
    app.match()
