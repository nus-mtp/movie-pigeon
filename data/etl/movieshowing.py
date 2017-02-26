"""
    This class retrieves movie schedule from different sources,
    parse all data into required format, and match it with imdb id.


"""
from urllib import request, error
from bs4 import BeautifulSoup
from selenium import webdriver


import html


class MovieShowing:

    imdb_search_format = "http://www.imdb.com/find?&q={}"

    def __init__(self, cinema):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)  # set browser size.
        self.cinema_id, self.cinema_name, self.cinema_url = cinema

    def extract_cinema_schedule(self):
        """retrieve one cinema schedule based on the given url,
        return a list of dictionaries of movie titles

        Main logic flow as follow:
            1. extract_raw
            2. transform and packaging
            3. match and store imdb id
            4. return the data
        """
        self.extract_raw_golden_village()

    # extract_raw
    def extract_raw_golden_village(self):
        self.driver.get(self.cinema_url)
        # retrieve title, (type like 3D) and schedule time raw data
        tabs = self.driver.find_elements_by_class_name("ng-binding")
        for tab in tabs:
            if tab.get_attribute("ng-bind-html") == "day.day":
                print(tab.text)
                if tab.text == "Advance Sales":
                    break

                tab.click()
                rows = self.driver.find_elements_by_class_name("row")
                for row in rows:
                    # get movie title
                    anchors = row.find_elements_by_class_name("ng-binding")
                    for anchor in anchors:
                        if anchor.get_attribute("ng-bind-html") == "getFilmTitle(movie)":
                            print(anchor.text)

                    # get movie schedule
                    buttons = row.find_elements_by_css_selector("button")
                    for button in buttons:
                        if button.get_attribute("ng-bind-html") == "time.time":
                            print(button.text)

                            # find imdb id
                            # create tuple cinema_id, movie_id, type, schedule
        return

    def extract_raw_cathay(self):
        pass

    def extract_raw_shaw_brother(self):
        pass

    # match (to be moved into moviematcher class)
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

    # getter
    def get_movie_schedule(self):
        pass