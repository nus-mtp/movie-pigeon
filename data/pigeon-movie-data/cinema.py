"""
    This class retrieves movie schedule from different sources,
    parse all data into required format, and match it with imdb id.
"""
from pytz import timezone
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
from string import capwords

import time


class CinemaList:

    GOLDEN_VILLAGE_LIST_HOME = "https://www.gv.com.sg/GVCinemas"

    CATHAY_LIST_HOME = "http://www.cathaycineplexes.com.sg/cinemas/"

    SHAW_BROTHER_LIST_HOME = "http://www.shaw.sg/sw_cinema.aspx"

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def get_latest_cinema_list(self):
        """
        return the latest cinema list to the processor in the format
        of
        {
            "url": ...
            "cinema_name: ...
            "provider": ...
        }
        :return: list
        """
        cinema_list = []
        cinema_list.extend(self._extract_cathay_cinema_list())
        cinema_list.extend(self._extract_sb_cinema_list())
        cinema_list.extend(self._extract_gv_cinema_list())
        return cinema_list

    def _extract_gv_cinema_list(self):
        """
        return a list of dictionaries contain all Golden Village
        cinema names, and their corresponding url.
        """
        url = self.GOLDEN_VILLAGE_LIST_HOME

        cinema_list = []

        # get raw cinema list
        raw_cinema_url = []
        self.driver.get(url)
        anchors = self.driver.find_element_by_class_name("cinemas-list").find_elements_by_class_name("ng-binding")
        for anchor in anchors:
            raw_cinema_url.append(anchor.get_attribute("href"))

        # get actual list, in each url it may contain more than one cinema
        for cinema_url in raw_cinema_url:
            self.driver = webdriver.PhantomJS()  # reinstantiate to avoid detach from DOM
            self.driver.get(cinema_url)
            div = self.driver.find_elements_by_class_name("ng-binding")
            for item in div:
                if item.get_attribute("ng-bind-html") == "cinema.name":
                    cinema_name = item.text
                    self.insert_cinema_data(cinema_list, cinema_name, cinema_url, "gv")
        return cinema_list

    def _extract_cathay_cinema_list(self):
        """Get a list of dictionaries contain all cathay cinema names.
        It's corresponding url is None because cathay does not show movies
        schedule based on individual cinemas in their web page layouts.
        """
        cinema_list = []

        url = self.CATHAY_LIST_HOME
        web_content = request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(web_content, "lxml")
        divs = soup.find_all("div", {"class": "description"})
        for div in divs:
            cinema_name = capwords(div.find("h1").text)
            self.insert_cinema_data(cinema_list, cinema_name, "http://www.cathaycineplexes.com.sg/showtimes/", "cathay")
        return cinema_list

    def _extract_sb_cinema_list(self):
        """Get a list of dictionaries contain all SB cinema names,
        and their corresponding urls
        """
        name_list = []
        url_list = []
        cinema_list = []

        # get names
        url = self.SHAW_BROTHER_LIST_HOME
        web_content = request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(web_content, "lxml")
        divs = soup.find_all("a", {"class": "txtHeaderBold"})
        for div in divs:
            name_list.append(div.text)

        # get url
        buy_tickets = soup.find_all("a", {"class": "txtNormalDim"})
        for item in buy_tickets:
            current_link = item["href"]
            if "buytickets" in current_link:
                url_list.append("http://" + "www.shaw.sg/" + item["href"])

        assert len(name_list) == len(url_list)  # check whether there is mistake in matching cinema name and url

        for i in range(len(name_list)):
            self.insert_cinema_data(cinema_list, name_list[i], url_list[i], "sb")
        return cinema_list

    @staticmethod
    def insert_cinema_data(cinema_list, cinema_name, cinema_url, provider):
        inserted_tuple = {
            "url": cinema_url,
            "cinema_name": cinema_name,
            "provider": provider
        }
        cinema_list.append(inserted_tuple)


class CinemaSchedule:

    def __init__(self, cinema):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)  # set browser size
        self.cinema_id, self.cinema_name, self.cinema_url, self.provider = cinema

    def generic_cinema_extractor(self):
        """
        it will auto select the extract method based on the url
        or cinema name given, return the formatted data object
        that can be used by Loader
        :return: dictionary
        """
        self._extract_golden_village()
        self._extract_cathay()
        self._extract_shaw_brother()

    # extract_raw
    def _extract_golden_village(self):
        self.driver.get(self.cinema_url)
        # retrieve title, (type like 3D) and schedule time raw data
        tabs = self.driver.find_elements_by_class_name("ng-binding")

        cinema_schedule = {}
        date_counter = 0
        for tab in tabs:
            if tab.get_attribute("ng-bind-html") == "day.day":
                current_date = self._get_singapore_date(date_counter)
                if tab.text == "Advance Sales":  # reach the end of tabs
                    break

                tab.click()
                rows = self.driver.find_elements_by_class_name("row")

                for row in rows:
                    # get movie title
                    current_title = None
                    current_time = []

                    # get movie title
                    anchors = row.find_elements_by_class_name("ng-binding")
                    for anchor in anchors:
                        if anchor.get_attribute("ng-bind-html") == "getFilmTitle(movie)":
                            current_title = anchor.text

                    # get movie schedule
                    buttons = row.find_elements_by_css_selector("button")
                    for button in buttons:
                        if button.get_attribute("ng-bind-html") == "time.time":
                            current_time.append(current_date + " " + self._convert_12_to_24_hour_time(button.text))

                    # store
                    if current_title is not None:
                        if current_title in cinema_schedule:
                            cinema_schedule[current_title].extend(current_time)
                        else:
                            cinema_schedule[current_title] = current_time

            date_counter += 1
        return cinema_schedule

    def _extract_cathay(self):
        self.driver.get(self.cinema_url)
        cathay_id = self._get_id_from_cathay_cinema_name(self.cinema_name)
        outer_div = self.driver.find_element_by_id("ContentPlaceHolder1_wucST{}_tabs".format(cathay_id))
        tabbers = outer_div.find_elements_by_class_name("tabbers")

        date_counter = 0
        cinema_schedule = {}
        for tabber in tabbers:  # for each day
            current_date = self._get_singapore_date(date_counter)
            rows = tabber.find_elements_by_class_name("movie-container")
            for row in rows:
                try:
                    row_content = row.get_attribute("innerHTML")
                    soup = BeautifulSoup(row_content, "lxml")
                    current_title = soup.find("strong").text

                    current_time = []
                    times = soup.find_all("a", {"class": "cine_time"})
                    for show_time in times:
                        current_time.append(current_date + " " + show_time.text + ":00")

                    if current_title is not None:
                        if current_title in cinema_schedule:
                            cinema_schedule[current_title].extend(current_time)
                        else:
                            cinema_schedule[current_title] = current_time
                except AttributeError:
                    break

            date_counter += 1
        return cinema_schedule

    def _extract_shaw_brother(self):
        self.driver.get(self.cinema_url)
        show_dates = []
        options = self.driver.find_element_by_id("ctl00_Content_ddlShowDate").find_elements_by_css_selector(
            "option")
        for show_date in options:
            show_dates.append(show_date.get_attribute("value"))

        cinema_schedule = {}
        for show_date in show_dates:  # each day
            current_date = datetime.strptime(show_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            self.driver.find_element_by_xpath(
                "//select[@id='ctl00_Content_ddlShowDate']/option[@value='{}']".format(show_date)).click()
            rows = self.driver.find_elements_by_class_name("panelSchedule")
            for row in rows[2:]:  # remove table header
                current_title, schedule = row.text.strip().split("\n", 1)
                if "PM" in schedule or "AM" in schedule:
                    # title
                    current_title = current_title.split("   ")[1]

                    # time
                    current_time = []
                    schedule = schedule.replace("+", "").replace("*", "")
                    schedule = schedule.replace(" PM", "PM").replace(" AM", "AM").replace("\n", " ")
                    if "(" in schedule:
                        bracket_index = schedule.find("(")
                        schedule = schedule[:bracket_index]  # remove anything behind bracket
                    schedule = schedule.split(" ")

                    for item in schedule:
                        if item != "":
                            current_time.append(current_date + " " + self._convert_12_to_24_hour_time(item))

                    if current_title is not None:
                        if current_title in cinema_schedule:
                            cinema_schedule[current_title].extend(current_time)
                        else:
                            cinema_schedule[current_title] = current_time
        return cinema_schedule

    def _parse_cinema_object_to_data(self):
        """
        parse the cinema object in the format:
        (based on self.provider, parsing strategy may vary)
        {
            movie_title: a list of movie schedule
        }
        to the format that can be consumed by loader class and
        subsequently being stored into the database
        {
            "imdb_id": ...,
            "schedule": [...],
            "type": ...

        In the process, it will complete 2 additional tasks
        besides rearranging the dictionary -- parse the movie
        title into title and additional information such as
        "3D" "Dolby Digital", and match the title to imdb id
        :return: dictionary
        """
        pass

    @staticmethod
    def _get_id_from_cathay_cinema_name(cinema_name):
        """get cathay internal id from their cinema name for web elements"""
        mapper = {
            "Cathay Cineplex Amk Hub": "",
            "Cathay Cineplex Causeway Point": "1",
            "Cathay Cineplex Cineleisure Orchard": "2",
            "Cathay Cineplex Downtown East": "3",
            "Cathay Cineplex Jem": "4",
            "The Cathay Cineplex": "5",
            "Cathay Cineplex West Mall": "6"
        }
        return mapper[cinema_name]

    @staticmethod
    def _get_singapore_date(n):
        """get the date of n days from now in SGT"""
        today = (datetime.fromtimestamp(time.time(), timezone("Singapore")) + timedelta(days=n)).strftime(
            "%Y-%m-%d")
        return today

    @staticmethod
    def _convert_12_to_24_hour_time(time_string):
        """
        convert time in 12 hour string format to 24 hour string format
        :param time_string: string
        :return: string
        """
        return datetime.strptime(time_string, "%I:%M%p").strftime("%H:%M:%S")


