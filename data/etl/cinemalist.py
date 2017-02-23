from bs4 import BeautifulSoup
from urllib import request, error
from selenium import webdriver
from urllib.request import Request, urlopen


class CinemaList:

    gv_cinema_list_home = "https://www.gv.com.sg/GVCinemas"

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        pass

    def get_golden_village_cinema_list(self):
        """
        get all cinema name and corresponding url from gv official page
        :return: a list of dictionary
        """
        url = self.gv_cinema_list_home
        cinema_list = []

        # get raw cinema list
        raw_cinema_url = []
        self.driver.get(url)
        anchors = self.driver.find_element_by_class_name("cinemas-list").find_elements_by_class_name("ng-binding")
        for anchor in anchors:
            raw_cinema_url.append(anchor.get_attribute("href"))

        # get actual list
        for cinema_url in raw_cinema_url:
            self.driver = webdriver.PhantomJS()  # reinstantiate to avoid detach from DOM
            self.driver.get(cinema_url)
            div = self.driver.find_elements_by_class_name("ng-binding")
            for item in div:
                if item.get_attribute("ng-bind-html") == "cinema.name":
                    cinema_name = item.text
                    tuple = {
                        "url": cinema_url,
                        "cinema_name": cinema_name
                    }
                    cinema_list.append(tuple)

        return cinema_list

    def get_cathay(self):
        pass

    def get_shaw_brother(self):
        pass
