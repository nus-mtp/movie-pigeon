from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from string import capwords
from transformer import CinemaScheduleTransformer, GeneralTransformer, CinemaListTransformer
from urllib import request

import utils
import json
import logging
import time


class CinemaList:
    """
    This class provides one single operation.
    Return the list of cinemas, with their url and name
    """
    GOLDEN_VILLAGE_LIST_HOME = "https://www.gv.com.sg/GVCinemas"

    CATHAY_LIST_HOME = "http://www.cathaycineplexes.com.sg/cinemas/"

    SHAW_BROTHER_LIST_HOME = "http://www.shaw.sg/sw_cinema.aspx"

    GOOGLE_GEOCODE_API = 'http://maps.google.com/maps/api/geocode/json?address={}'

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
        cinema_urls = self._get_gv_cinema_url()

        # get actual list, in each url it may contain more than one cinema
        cinema_list = []
        for cinema_url in cinema_urls:
            self._get_single_gv_cinema_data(cinema_list, cinema_url)

        return cinema_list

    def _get_single_gv_cinema_data(self, cinema_list, cinema_url):
        """
        get a single cinema data
        :param cinema_list: list
        :param cinema_url: string
        :return:
        """
        driver = webdriver.PhantomJS()  # re-instantiate to avoid detach from DOM
        driver.get(cinema_url)
        div = driver.find_elements_by_class_name("ng-binding")
        for item in div:
            if item.get_attribute("ng-bind-html") == "cinema.name":
                cinema_name = item.text
                latitude, longitude = self._get_geocode(cinema_name)
                cinema_data = CinemaListTransformer.insert_cinema_data(cinema_name, cinema_url, "gv", latitude, longitude)
                cinema_list.append(cinema_data)

    def _get_gv_cinema_url(self):
        """
        get cinema urls from website
        :return: list
        """
        driver = webdriver.PhantomJS()
        driver.get(self.GOLDEN_VILLAGE_LIST_HOME)
        cinema_urls = []
        anchors = driver.find_element_by_class_name("cinemas-list").find_elements_by_class_name("ng-binding")

        for anchor in anchors:
            cinema_urls.append(anchor.get_attribute("href"))

        return cinema_urls

    def _extract_cathay_cinema_list(self, soup):
        """
        get a list of dictionaries contain all cathay cinema names.
        :param soup: BeautifulSoup()
        :return: list
        """
        cinema_list = []

        divs = soup.find_all("div", {"class": "description"})
        for div in divs:
            cinema_name = capwords(div.find("h1").text)
            latitude, longitude = self._get_geocode(cinema_name)
            inserted_tuple = CinemaListTransformer.insert_cinema_data(
                cinema_name, "http://www.cathaycineplexes.com.sg/showtimes/", "cathay", latitude, longitude)
            cinema_list.append(inserted_tuple)
        return cinema_list

    def _extract_sb_cinema_list(self, soup):
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
            latitude, longitude = self._get_geocode(name_list[i])
            inserted_tuple = CinemaListTransformer.insert_cinema_data(name_list[i], url_list[i], "sb", latitude, longitude)
            cinema_list.append(inserted_tuple)

        return cinema_list

    def _get_geocode(self, address):
        """
        return the latitude and longtitude of an address,
        given by google geocode api
        :param address: string
        :return: float, float
        """
        address = self._parse_special_cinema(address)

        time.sleep(1)  # important to avoid violating google api limit

        web_result = self._get_json_result_from_google_geocode(address)
        location = web_result['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude

    @staticmethod
    def _parse_special_cinema(address):
        """
        parse the name of special cinemas, so it
        can be used for google API
        :param address: string
        :return: string
        """
        if ',' in address:
            address = address.split(",")[-1].strip()  # special cinema will be determined by their location
        if '(' in address:
            address = address.split('(')[0].strip()  # remove stalls
        address = address.replace(" ", '%20')  # replace space for html encoding
        return address

    def _get_json_result_from_google_geocode(self, address):
        url = self.GOOGLE_GEOCODE_API.format(address)
        json_content = request.urlopen(url).read().decode('utf-8')
        web_result = json.loads(json_content)
        return web_result


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

    def get_cinema_schedule(self):
        """
        it will auto select the extract method based on the url
        or cinema name given, return the formatted data object
        that can be used by Loader
        :return: list
        """
        if self.provider == "gv":
            cinema_object = self._extract_gv_schedule()
        elif self.provider == "sb":
            cinema_object = self._extract_sb_schedule()
        elif self.provider == "cathay":
            cinema_object = self._extract_cathay_schedule()
        else:
            raise utils.InvalidCinemaTypeException("Invalid Cinema provider!")

        return self.transformer.parse_cinema_object_to_data(cinema_object, self.provider)

    # ==================
    #   Golden Village
    # ==================
    def _extract_gv_schedule(self):
        """
        extract current gv cinema schedule
        return a dict contains only raw movie title and a
        list of timing
        :return: dictionary
        """
        cinema_schedule = {}

        date_iterator = self._get_gv_date_iterator()

        date_counter = 0  # date counter into the future
        for each_day in date_iterator:
            if each_day.get_attribute("ng-bind-html") == "day.day":  # iterate through date tabs
                current_date = GeneralTransformer.get_singapore_date(date_counter)

                if each_day.text == "Advance Sales":  # reach the end of tabs
                    break

                each_day.click()  # select tab
                self.driver.implicitly_wait(2)  # wait for page to load
                web_element_titles = self.driver.find_elements_by_class_name("row")

                self._update_gv_single_movie_schedule(cinema_schedule, current_date, web_element_titles)

                date_counter += 1

        return cinema_schedule

    def _get_gv_date_iterator(self):
        """
        get the outmost layer of web element, representing
        each day, which will be iterated for every movie
        :return: selenium web element
        """
        self.driver.get(self.cinema_url)
        tabs = self.driver.find_elements_by_class_name("ng-binding")
        return tabs

    def _update_gv_single_movie_schedule(self, cinema_schedule, current_date, movie_iterator):
        """
        update the dictionary with data of each movie
        :param cinema_schedule: dictionary
        :param current_date: datetime
        :param movie_iterator: selenium web element
        :return:
        """
        for movie_row in movie_iterator:
            current_title = self._get_gv_single_movie_title(movie_row)
            current_time = self._get_gv_single_movie_time(current_date, movie_row)
            self._merge_gv_single_movie_schedule(cinema_schedule, current_time, current_title)

    @staticmethod
    def _merge_gv_single_movie_schedule(cinema_schedule, current_time, current_title):
        """
        merge the time list and title list into dictionary
        :param cinema_schedule: dictionary
        :param current_time: list
        :param current_title: string
        :return:
        """
        if current_title is not None:
            if current_title in cinema_schedule:
                cinema_schedule[current_title].extend(current_time)
            else:
                cinema_schedule[current_title] = current_time

    @staticmethod
    def _get_gv_single_movie_time(current_date, web_element_title):
        """
        get time list from one web element
        :param current_date:
        :param web_element_title:
        :return:
        """
        current_time = []
        buttons = web_element_title.find_elements_by_css_selector("button")

        for button in buttons:
            if button.get_attribute("ng-bind-html") == "time.time":
                current_time.append(current_date + " " +
                                    GeneralTransformer.convert_12_to_24_hour_time(button.text))

        return current_time

    @staticmethod
    def _get_gv_single_movie_title(web_element_title):
        """
        get title from one web element
        :param web_element_title:
        :return:
        """
        current_title = None
        anchors = web_element_title.find_elements_by_class_name("ng-binding")

        for anchor in anchors:
            if anchor.get_attribute("ng-bind-html") == "getFilmTitle(movie)":
                current_title = anchor.text

        return current_title

    # ==========
    #   Cathay
    # ==========
    def _extract_cathay_schedule(self):
        """
        extract current cathay cinema schedule
        return a dict contains only raw movie title and a
        list of timing
        :return: dictionary
        """
        cinema_schedule = {}

        date_iterator = self._get_cathay_date_iterator()

        date_counter = 0
        for each_day in date_iterator:  # for each day
            current_date = GeneralTransformer.get_singapore_date(date_counter)

            rows = each_day.find_elements_by_class_name("movie-container")
            self._update_cathay_single_movie_schedule(cinema_schedule, current_date, rows)

            date_counter += 1

        return cinema_schedule

    def _get_cathay_date_iterator(self):
        """
        get the outmost layer of web element, representing
        each day, which will be iterated for every movie
        :return: selenium web element
        """
        self.driver.get(self.cinema_url)
        self.driver.implicitly_wait(2)  # wait for page to load
        cathay_id = CinemaScheduleTransformer.get_cathay_id_from_cathay_cinema_name(self.cinema_name)
        outer_div = self.driver.find_element_by_id(cathay_id)
        tabs = outer_div.find_elements_by_class_name("tabbers")
        return tabs

    def _update_cathay_single_movie_schedule(self, cinema_schedule, current_date, movie_iterator):
        """
        update the dictionary with data of each movie
        :param cinema_schedule: dictionary
        :param current_date: datetime
        :param movie_iterator: selenium web element
        :return: None
        """
        for movie_row in movie_iterator:
            soup = self._parse_cathay_inner_html(movie_row)

            try:
                current_title = self._get_cathay_single_movie_title(soup)
            except AttributeError:  # break when there is no more content in tabs
                break

            current_time = self._get_cathay_single_movie_time(current_date, soup)
            self._merge_cathay_single_movie_schedule(cinema_schedule, current_time, current_title)

    @staticmethod
    def _merge_cathay_single_movie_schedule(cinema_schedule, current_time, current_title):
        """
        merge the time list and title list into dictionary
        :param cinema_schedule: dictionary
        :param current_time: list
        :param current_title: string
        :return: None
        """
        if current_title is not None:
            if current_title in cinema_schedule:
                cinema_schedule[current_title].extend(current_time)
            else:
                cinema_schedule[current_title] = current_time

    @staticmethod
    def _get_cathay_single_movie_time(current_date, soup):
        """
        get time list from one web element
        :param current_date: datetime
        :param soup: BeautifulSoup object
        :return: list
        """
        current_time = []
        times = soup.find_all("a", {"class": "cine_time"})
        for show_time in times:
            current_time.append(current_date + " " + show_time.text + ":00")
        return current_time

    @staticmethod
    def _get_cathay_single_movie_title(soup):
        """
        get title from one web element
        :param soup: BeautifulSoup object
        :return: string
        """
        current_title = soup.find("strong").text
        return current_title

    @staticmethod
    def _parse_cathay_inner_html(row):
        """
        parse the inner html of the movie web element
        for the extraction of title and schedules
        :param row: selenium web element
        :return: BeautifulSoup object
        """
        row_content = row.get_attribute("innerHTML")
        soup = BeautifulSoup(row_content, "lxml")
        return soup

    # ================
    #   Shaw Brother
    # ================
    def _extract_sb_schedule(self):
        """
        extract current shaw cinema schedule
        return a dict contains only raw movie title and a
        list of timing
        :return: dictionary
        """
        cinema_schedule = {}

        date_iterator = self._get_sb_date_iterator()

        for each_day in date_iterator:  # each day
            current_date = self.parse_sb_date(each_day)

            self._load_page_by_date(each_day)  # click on the date to load page
            rows = self.driver.find_elements_by_class_name("panelSchedule")
            self._update_sb_single_movie_schedule(cinema_schedule, current_date, rows)

        return cinema_schedule

    def _get_sb_date_iterator(self):
        """
        get the outmost layer of web element, representing
        each day, which will be iterated for every movie
        :return: selenium web element
        """
        self.driver.get(self.cinema_url)
        show_dates = []
        options = self.driver.find_element_by_id("ctl00_Content_ddlShowDate")\
            .find_elements_by_css_selector("option")

        for show_date in options:
            show_dates.append(show_date.get_attribute("value"))

        return show_dates

    def _update_sb_single_movie_schedule(self, cinema_schedule, current_date, movie_iterator):
        """
        update the dictionary with data of each movie
        :param cinema_schedule: dictionary
        :param current_date: datetime
        :param movie_iterator: selenium element
        :return: None
        """
        for movie_row in movie_iterator[2:]:  # remove table header
            current_title, schedule = movie_row.text.strip().split("\n", 1)

            if "PM" in schedule or "AM" in schedule:
                current_title = self._get_sb_single_movie_title(current_title)
                current_time = self._get_sb_single_movie_time(current_date, schedule)
                self._merge_sb_single_movie_schedule(cinema_schedule, current_time, current_title)

    @staticmethod
    def _merge_sb_single_movie_schedule(cinema_schedule, current_time, current_title):
        """
        merge the time list and title list into dictionary
        :param cinema_schedule: dictionary
        :param current_time: list
        :param current_title: string
        :return: None
        """
        if current_title is not None:
            if current_title in cinema_schedule:
                cinema_schedule[current_title].extend(current_time)
            else:
                cinema_schedule[current_title] = current_time

    @staticmethod
    def _get_sb_single_movie_title(current_title):
        """
        parse title from raw title text
        :param current_title:
        :return:
        """
        current_title = current_title.split("   ")[1]
        return current_title

    @staticmethod
    def _get_sb_single_movie_time(current_date, schedule):
        """

        :param current_date:
        :param schedule:
        :return:
        """
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

        return current_time

    def _load_page_by_date(self, each_day):
        """
        navigate the webdriver and click the corresponding
        date selector, loading a web component
        :param each_day: string
        :return: None
        """
        self.driver.find_element_by_xpath(
            "//select[@id='ctl00_Content_ddlShowDate']/option[@value='{}']".format(each_day)).click()
        self.driver.implicitly_wait(2)

    @staticmethod
    def parse_sb_date(each_day):
        current_date = datetime.strptime(each_day, "%m/%d/%Y").strftime("%Y-%m-%d")
        return current_date


