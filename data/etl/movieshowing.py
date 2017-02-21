from urllib import request, error
from bs4 import BeautifulSoup
import json


class MovieShowing:

    def __init__(self):
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

if __name__ == '__main__':
    app = MovieShowing()
    app.extract()
