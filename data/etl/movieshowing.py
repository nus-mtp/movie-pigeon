"""
    This class retrieves movie schedule from different sources,
    parse all data into required format, and match it with imdb id.
"""
from urllib import request, error
from bs4 import BeautifulSoup
from selenium import webdriver, common
from pytz import timezone
from datetime import datetime, timedelta

import time
import html


class MovieShowing:

    imdb_search_format = "http://www.imdb.com/find?&q={}"

    def __init__(self, cinema):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)  # set browser size
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
        # self.extract_raw_golden_village()
        # self.extract_raw_cathay()
        self.extract_raw_shaw_brother()

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
        # data set up
        self.cinema_url = "http://www.cathaycineplexes.com.sg/showtimes/"
        self.cinema_name = "Cathay Cineplex Amk Hub"
        
        # engine set up
        self.driver.get(self.cinema_url)
        cathay_id = self._get_id_from_cathay_cinema_name(self.cinema_name)
        outer_div = self.driver.find_element_by_id("ContentPlaceHolder1_wucST{}_tabs".format(cathay_id))
        tabbers = outer_div.find_elements_by_class_name("tabbers")

        n = 0
        for tabber in tabbers: # for each day
            print(self._get_singapore_date(n))
            rows = tabber.find_elements_by_class_name("movie-container")
            for row in rows:
                try:
                    row_content = row.get_attribute("innerHTML")
                    soup = BeautifulSoup(row_content, "lxml")
                    title = soup.find("strong").text

                    time_list = []
                    times = soup.find_all("a", {"class": "cine_time"})
                    for show_time in times:
                        time_list.append(show_time.text)

                    print(title, time_list)
                except AttributeError:
                    break

            n += 1

    def extract_raw_shaw_brother(self):
        self.cinema_url = "http://www.shaw.sg/sw_buytickets.aspx?filmCode=&cplexCode=30 210 236 39 155 56 75 124 123 77 76 246 36 85 160 0&date="
        self.cinema_name = "Shaw Theatres Lido"
        self.driver.get(self.cinema_url)

        show_dates = []
        options = self.driver.find_element_by_id("ctl00_Content_ddlShowDate").find_elements_by_css_selector("option")
        for show_date in options:
            show_dates.append(show_date.get_attribute("value"))

        for show_date in show_dates:  # each day
            print(show_date)
            self.driver.find_element_by_xpath("//select[@id='ctl00_Content_ddlShowDate']/option[@value='{}']".format(show_date)).click()
            rows = self.driver.find_elements_by_class_name("panelSchedule")
            for row in rows[2:]: # remove table header
                name, schedule = row.text.strip().split("\n")
                if "PM" in schedule or "AM" in schedule:
                    name = name.split("   ")[1]
                    schedule = schedule.replace("+", "").replace("*", "")
                    schedule = schedule.replace(" PM", "PM").replace(" AM", "AM")
                    schedule = schedule.split(" ")
                    print(name, schedule)

    # getter
    def get_movie_schedule(self):
        pass

    @staticmethod
    def _get_id_from_cathay_cinema_name(cinema_name):
        """get cathay internal id from their cinema name for web elements"""
        mapper = {
            "Cathay Cineplex Amk Hub": ""
        }
        return mapper[cinema_name]

    @staticmethod
    def _get_singapore_date(n):
        """get the date of n days from now in SGT"""
        today = (datetime.fromtimestamp(time.time(), timezone("Singapore")) + timedelta(days=n)).strftime("%Y-%m-%d")
        return today