"""
    This class retrieves movie schedule from different sources and
    parse all data into required format
"""
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from string import capwords
from transformer import CinemaScheduleTransformer, GeneralTransformer, CinemaListTransformer

import utils


class CinemaList:

    GOLDEN_VILLAGE_LIST_HOME = "https://www.gv.com.sg/GVCinemas"

    CATHAY_LIST_HOME = "http://www.cathaycineplexes.com.sg/cinemas/"

    SHAW_BROTHER_LIST_HOME = "http://www.shaw.sg/sw_cinema.aspx"

    def __init__(self):
        self.cathay_soup = utils.build_soup_from_url(self.CATHAY_LIST_HOME)
        self.sb_soup = utils.build_soup_from_url(self.SHAW_BROTHER_LIST_HOME)

    def get_latest_cinema_list(self):
        """
        return the latest cinema list for all providers
        :return: list
        """
        cinema_list = []
        cinema_list.extend(self._extract_cathay_cinema_list(self.cathay_soup))
        cinema_list.extend(self._extract_sb_cinema_list(self.sb_soup))
        cinema_list.extend(self._extract_gv_cinema_list())
        return cinema_list

    def _extract_gv_cinema_list(self):
        """
        return a list of dictionaries contain all Golden Village
        cinema names, and their corresponding url
        :return: list
        """
        cinema_list = []
        driver = webdriver.PhantomJS()
        driver.get(self.GOLDEN_VILLAGE_LIST_HOME)

        # get raw cinema list
        raw_cinema_url = []
        anchors = driver.find_element_by_class_name("cinemas-list").find_elements_by_class_name("ng-binding")
        for anchor in anchors:
            raw_cinema_url.append(anchor.get_attribute("href"))

        # get actual list, in each url it may contain more than one cinema
        for cinema_url in raw_cinema_url:
            driver = webdriver.PhantomJS()  # reinstantiate to avoid detach from DOM
            driver.get(cinema_url)
            div = driver.find_elements_by_class_name("ng-binding")
            for item in div:
                if item.get_attribute("ng-bind-html") == "cinema.name":
                    cinema_name = item.text
                    inserted_tuple = CinemaListTransformer.insert_cinema_data(cinema_name, cinema_url, "gv")
                    cinema_list.append(inserted_tuple)

        return cinema_list

    @staticmethod
    def _extract_cathay_cinema_list(soup):
        """
        get a list of dictionaries contain all cathay cinema names.
        :param soup: BeautifulSoup()
        :return: list
        """
        cinema_list = []

        divs = soup.find_all("div", {"class": "description"})
        for div in divs:
            cinema_name = capwords(div.find("h1").text)
            inserted_tuple = CinemaListTransformer.insert_cinema_data(
                cinema_name, "http://www.cathaycineplexes.com.sg/showtimes/", "cathay")
            cinema_list.append(inserted_tuple)
        return cinema_list

    @staticmethod
    def _extract_sb_cinema_list(soup):
        """
        get a list of dictionaries contain all SB cinema names,
        and their corresponding urls
        :param soup: BeautifulSoup()
        :return: list
        """
        cinema_list = []

        name_list = []
        url_list = []

        # get names list
        divs = soup.find_all("a", {"class": "txtHeaderBold"})
        for div in divs:
            name_list.append(div.text)

        # get url list
        buy_tickets = soup.find_all("a", {"class": "txtNormalDim"})
        for item in buy_tickets:
            current_link = item["href"]
            if "buytickets" in current_link:
                url_list.append("http://" + "www.shaw.sg/" + item["href"])

        # check list length
        name_list_length = len(name_list)
        url_list_length = len(url_list)
        assert name_list_length == url_list_length  # check whether there is mistake in matching cinema name and url

        # merge lists
        for i in range(name_list_length):
            inserted_tuple = CinemaListTransformer.insert_cinema_data(name_list[i], url_list[i], "sb")
            cinema_list.append(inserted_tuple)

        return cinema_list


class CinemaSchedule:
    """
    This class handles all operations related to the extraction
    of movie schedules in cinemas
    """
    def __init__(self, cinema_name, cinema_url, cinema_provider):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)  # set browser size

        self.cinema_name = cinema_name
        self.cinema_url = cinema_url
        self.provider = cinema_provider

        self.transformer = CinemaScheduleTransformer()

    def extract_cinema_schedule(self):
        """
        it will auto select the extract method based on the url
        or cinema name given, return the formatted data object
        that can be used by Loader
        :return: list
        """
        if self.provider == "gv":
            cinema_object = self._extract_golden_village()
        elif self.provider == "sb":
            cinema_object = self._extract_shaw_brother()
        elif self.provider == "cathay":
            cinema_object = self._extract_cathay()
        else:
            raise utils.InvalidCinemaTypeException("Invalid Cinema provider!")

        return self.transformer.parse_cinema_object_to_data(cinema_object)

    def _extract_golden_village(self):
        """
        extract current gv cinema schedule
        return a dict contains only raw movie title and a
        list of timing
        :return: dictionary
        """
        self.driver.get(self.cinema_url)
        # retrieve title, (type like 3D) and schedule time raw data
        tabs = self.driver.find_elements_by_class_name("ng-binding")

        cinema_schedule = {}
        date_counter = 0
        for tab in tabs:
            if tab.get_attribute("ng-bind-html") == "day.day":  # iterate through date tabs
                current_date = GeneralTransformer.get_singapore_date(date_counter)

                if tab.text == "Advance Sales":  # reach the end of tabs
                    break

                tab.click()
                rows = self.driver.find_elements_by_class_name("row")

                for row in rows:
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
                            current_time.append(current_date + " " +
                                                GeneralTransformer.convert_12_to_24_hour_time(button.text))

                    # store
                    if current_title is not None:
                        if current_title in cinema_schedule:
                            cinema_schedule[current_title].extend(current_time)
                        else:
                            cinema_schedule[current_title] = current_time

                date_counter += 1
        return cinema_schedule

    def _extract_cathay(self):
        """
        extract current cathay cinema schedule
        return a dict contains only raw movie title and a
        list of timing
        :return: dictionary
        """
        self.driver.get(self.cinema_url)
        cathay_id = CinemaScheduleTransformer.get_cathay_id_from_cathay_cinema_name(self.cinema_name)
        outer_div = self.driver.find_element_by_id("ContentPlaceHolder1_wucST{}_tabs".format(cathay_id))
        tabbers = outer_div.find_elements_by_class_name("tabbers")

        date_counter = 0
        cinema_schedule = {}
        for tabber in tabbers:  # for each day
            current_date = GeneralTransformer.get_singapore_date(date_counter)
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
        """
        extract current shaw cinema schedule
        return a dict contains only raw movie title and a
        list of timing
        :return: dictionary
        """
        self.driver.get(self.cinema_url)

        show_dates = []
        options = self.driver.find_element_by_id("ctl00_Content_ddlShowDate").find_elements_by_css_selector(
            "option")

        for show_date in options:
            show_dates.append(show_date.get_attribute("value"))

        cinema_schedule = {}  # data store

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
                            current_time.append(current_date + " " +
                                                GeneralTransformer.convert_12_to_24_hour_time(item))

                    if current_title is not None:
                        if current_title in cinema_schedule:
                            cinema_schedule[current_title].extend(current_time)
                        else:
                            cinema_schedule[current_title] = current_time

        return cinema_schedule

