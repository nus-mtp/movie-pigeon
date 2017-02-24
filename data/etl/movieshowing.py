from urllib import request, error
from bs4 import BeautifulSoup
import html


class MovieShowing:

    imdb_search_format = "http://www.imdb.com/find?&q={}"

    def __init__(self):
        pass

    def extract_cinema_schedule(self, cinema_url):
        """Retrieve one cinema schedule based on the given url"""
        pass

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
