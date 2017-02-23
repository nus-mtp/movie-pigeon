from bs4 import BeautifulSoup
from urllib import request, error
from selenium import webdriver
from string import capwords


class CinemaList:

    gv_cinema_list_home = "https://www.gv.com.sg/GVCinemas"

    cathay_cinema_list_home = "http://www.cathaycineplexes.com.sg/cinemas/"

    sb_cinema_list_home = "http://www.shaw.sg/sw_cinema.aspx"

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def get_golden_village_cinema_list(self):
        """Get a list of dictionaries contain all Golden Village
        cinema names, and their corresponding url.
        """
        url = self.gv_cinema_list_home

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
                    self.insert_cinema_data(cinema_list, cinema_name, cinema_url)
        return cinema_list

    def get_cathay_cinema_list(self):
        """Get a list of dictionaries contain all cathay cinema names.
        It's corresponding url is None because cathay does not show movies
        schedule based on individual cinemas in their web page layouts.
        """
        cinema_list = []

        url = self.cathay_cinema_list_home
        web_content = request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(web_content, "lxml")
        divs = soup.find_all("div", {"class": "description"})
        for div in divs:
            cinema_name = capwords(div.find("h1").text)
            self.insert_cinema_data(cinema_list, cinema_name, None)
        return cinema_list

    def get_shaw_brother_cinema_list(self):
        """Get a list of dictionaries contain all SB cinema names,
        and their corresponding urls
        """
        name_list = []
        url_list = []
        cinema_list = []

        url = self.sb_cinema_list_home
        web_content = request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(web_content, "lxml")
        divs = soup.find_all("a", {"class": "txtHeaderBold"})
        for div in divs:
            name_list.append(div.text)

        buy_tickets = soup.find_all("a", {"class": "txtNormalDim"})
        for item in buy_tickets:
            current_link = item["href"]
            if "buytickets" in current_link:
                url_list.append("www.shaw.sg/" + item["href"])

        assert len(name_list) == len(url_list) # check whether there is misake in matching cinema name and url

        for i in range(len(name_list)):
            self.insert_cinema_data(cinema_list, name_list[i], url_list[i])

        return cinema_list

    @staticmethod
    def insert_cinema_data(cinema_list, cinema_name, cinema_url):
        inserted_tuple = {
            "url": cinema_url,
            "cinema_name": cinema_name
        }
        cinema_list.append(inserted_tuple)


