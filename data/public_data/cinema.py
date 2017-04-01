from datetime import datetime
from selenium import webdriver, common
from string import capwords
from public_data.transformer import CinemaScheduleTransformer, GeneralTransformer, CinemaListTransformer

import public_data.utils as utils


class CinemaList:
    """
    This class provides one single operation:
    return the list of cinemas with name and their geocode
    """

    CATHAY_LIST = "http://www.cathaycineplexes.com.sg/cinemas/"
    SHAW_BROTHER_LIST = "http://www.shaw.sg/sw_cinema.aspx"
    GV_LIST = 'https://www.gv.com.sg/GVBuyTickets#/'

    GV_PROVIDER = 'GV'
    CATHAY_PROVIDER = 'Cathay'
    SHAW_PROVIDER = 'Shaw'

    def __init__(self, test=False):
        if test:
            self.cathay_soup = utils.build_soup_from_file('data_cinema_list/cathay_home.html')
            self.sb_soup = utils.build_soup_from_file('data_cinema_list/shaw_home.html')
            self.gv_soup = utils.build_soup_from_file('data_cinema_list/gv_home.html')
        else:
            self.cathay_soup = utils.build_soup_from_url(self.CATHAY_LIST)
            self.sb_soup = utils.build_soup_from_url(self.SHAW_BROTHER_LIST)
            self.gv_soup = utils.build_soup_from_selenium(self.GV_LIST)

    def get_cinema_list(self):
        """
        return the latest cinema list for all providers
        :return: list
        """
        cinema_list = []
        cinema_list.extend(self._extract_cathay_cinema_list())
        cinema_list.extend(self._extract_sb_cinema_list())
        cinema_list.extend(self._extract_gv_cinema_list())
        return cinema_list

    # ============ Golden Village ============

    def _extract_gv_cinema_list(self):
        """
        return a list of dictionaries contain all Golden Village
        cinema names, and their corresponding url
        :return: list
        """
        cinema_provider = self.GV_PROVIDER
        cinema_iterator = self._get_cinema_iterator(cinema_provider)

        cinema_list = []
        for cinema_web in cinema_iterator:
            try:
                if cinema_web['ng-bind-html'] == 'cinema.name':
                    cinema_name = cinema_web.text.strip()
                    displayed_name, location = self._parse_gv_cinema_name(cinema_name)
                    latitude, longitude = utils.get_geocode(location)
                    inserted_tuple = CinemaListTransformer.insert_cinema_data(cinema_name, cinema_provider, latitude,
                                                                              longitude, displayed_name)
                    cinema_list.append(inserted_tuple)
            except KeyError:
                continue

        return cinema_list

    def _parse_gv_cinema_name(self, original_cinema_name):
        """
        parse the messed up GV cinema name into standard
        format, return both the text and the location
        :param original_cinema_name: string
        :return: string
        """
        if "," in original_cinema_name:
            tokens = original_cinema_name.split(",")
            cinema_name = "(" + tokens[0].strip() + ")"
            location = tokens[1].strip()
            if location == "Grand":
                location = "Great World City"
            final_text = self.GV_PROVIDER + " @ " + (location + " " + cinema_name).replace("GV ", "")
        elif "@" in original_cinema_name:
            location = "Capitol"
            final_text = original_cinema_name
        else:
            if "Gold Class" in original_cinema_name:
                location = original_cinema_name.replace("Gold Class", "")
                cinema_name = "(Gold Class)"
            elif "GV " in original_cinema_name:
                location = original_cinema_name.replace("GV ", "")
                cinema_name = ""
            elif "Gemini" in original_cinema_name:
                location, cinema_name = original_cinema_name.split(" ", 0)
                cinema_name = "({})".format(cinema_name)
            else:
                raise utils.InvalidCinemaTypeException
            final_text = self.GV_PROVIDER + " @ " + (location.strip() + " " + cinema_name.strip())
        return final_text, location

    # ============ Cathay ============

    def _extract_cathay_cinema_list(self):
        """
        get a list of dictionaries contain all cathay cinema names.
        :return: list
        """
        cinema_provider = self.CATHAY_PROVIDER
        cinema_iterator = self._get_cinema_iterator(cinema_provider)

        cinema_list = []
        for cinema_web in cinema_iterator:
            cinema_name = capwords(cinema_web.find("h1").text).strip()

            displayed_name = self._parse_cathay_cinema_name(cinema_name)

            latitude, longitude = utils.get_geocode(cinema_name)
            inserted_tuple = CinemaListTransformer.insert_cinema_data(cinema_name, cinema_provider, latitude, longitude,
                                                                      displayed_name)
            cinema_list.append(inserted_tuple)

        return cinema_list

    def _parse_cathay_cinema_name(self, cinema_name):
        """
        parse the cathay cinema name into standard format
        :param cinema_name: string
        :return: string
        """
        if cinema_name == "The Cathay Cineplex":
            return self.CATHAY_PROVIDER + " @ " + "The Cathay"
        displayed_name = cinema_name.replace("Cathay Cineplex", "").strip()
        return self.CATHAY_PROVIDER + " @ " + displayed_name

    # ============ Shaw Brother ============

    def _extract_sb_cinema_list(self):
        """
        get a list of dictionaries contain all SB cinema names,
        and their corresponding urls
        :return: list
        """
        cinema_provider = self.SHAW_PROVIDER
        cinema_iterator = self._get_cinema_iterator(cinema_provider)

        cinema_list = []
        for cinema_web in cinema_iterator:
            cinema_name = cinema_web.text.strip()

            displayed_name = self._parse_shaw_cinema_name(cinema_name)

            latitude, longitude = utils.get_geocode(cinema_name)
            inserted_tuple = CinemaListTransformer.insert_cinema_data(capwords(cinema_name), cinema_provider, latitude,
                                                                      longitude, displayed_name)
            cinema_list.append(inserted_tuple)
        return cinema_list

    def _parse_shaw_cinema_name(self, cinema_name):
        """
        parse the shaw cinema name into standard format
        :param cinema_name: string
        :return: string
        """
        displayed_name = cinema_name.replace("Shaw Theatres", "")
        if 'nex' in displayed_name:
            displayed_name = displayed_name.replace('nex', 'Nex')
        displayed_name = self.SHAW_PROVIDER + " @" + displayed_name
        return displayed_name

    # ============ General Helper ============

    def _get_cinema_iterator(self, provider):
        """
        get the list of web elements from BeautifulSoup object
        :param provider: string
        :return: list
        """
        if provider == self.GV_PROVIDER:
            return self.gv_soup.find_all('p', {'class': 'ng-binding'})
        elif provider == self.SHAW_PROVIDER:
            return self.sb_soup.find_all("a", {"class": "txtHeaderBold"})
        elif provider == self.CATHAY_PROVIDER:
            return self.cathay_soup.find_all("div", {"class": "description"})
        else:
            raise utils.InvalidCinemaTypeException


class CinemaSchedule:
    """
    This class handles all operations related to the extraction
    of movie schedules in cinemas
    """

    SHAW_SCHEDULES = 'http://www.shaw.sg/sw_buytickets.aspx?CplexCode=&FilmCode=&date={}'
    GV_SCHEDULES = 'https://www.gv.com.sg/GVBuyTickets#/'
    CATHAY_SCHEDULES = 'http://www.cathaycineplexes.com.sg/showtimes/'

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1124, 850)  # set browser size

        self.transformer = CinemaScheduleTransformer()

        from public_data.loader import Loader
        self.loader = Loader()  # for matching cinema id

    # ============ Golden Village ============

    def get_gv_schedule(self):
        # get web content
        self.driver.get(self.GV_SCHEDULES)

        # declare data object
        provider_schedule = {}

        for i in range(6):  # for each day
            current_date = GeneralTransformer.get_singapore_date(i)
            self._get_gv_date_iterator(i).click()
            self.driver.implicitly_wait(2)

            cinema_iterators = self._get_gv_cinema_iterator()

            for current_cinema in cinema_iterators:  # for each cinema
                cinema_name = current_cinema.find_element_by_css_selector('p').text
                cinema_id = self.loader.get_cinema_id_from_name(cinema_name)
                movie_iterators = self._get_gv_movie_iterator(current_cinema)

                for current_movie in movie_iterators:  # for each movie
                    movie_title = self._get_gv_movie_title(current_movie)

                    if 'Zen Zone' in movie_title:  # gv special time slot
                        continue

                    movie_timing = self._get_gv_movie_timing(current_date, current_movie)
                    title, additional_info = self.transformer.parse_gv_movie_title(movie_title)
                    self._package_schedule_data(additional_info, cinema_id, movie_timing, provider_schedule, title)

        return provider_schedule

    @staticmethod
    def _get_gv_movie_iterator(current_cinema):
        movie_iterators = current_cinema.find_elements_by_class_name('row')[1:]  # skip date row
        return movie_iterators

    def _get_gv_cinema_iterator(self):
        return self.driver.find_elements_by_class_name("buy-tickets-section")

    def _get_gv_date_iterator(self, index):
        date_iterators = []
        tabs = self.driver.find_elements_by_class_name("ng-binding")
        for tab in tabs:
            if tab.get_attribute("ng-bind-html") == "date.name":

                if tab.text == "Advance Sales":  # reach the end of tabs
                    break

                date_iterators.append(tab)

        return date_iterators[index]

    @staticmethod
    def _get_gv_movie_title(current_movie):
        movie_title = current_movie.find_element_by_css_selector('span').text
        return movie_title

    @staticmethod
    def _get_gv_movie_timing(current_date, current_movie):
        movie_timing = []
        buttons = current_movie.find_elements_by_css_selector("button")
        for button in buttons:
            movie_timing.append(current_date + " " +
                                GeneralTransformer.convert_12_to_24_hour_time(button.text))
        return movie_timing

    # ============ Cathay ============

    def get_cathay_schedule(self):
        # get web content
        self.driver.get(self.CATHAY_SCHEDULES)

        provider_schedule = {}

        cathay_index = 0
        while True:
            if cathay_index == 0:
                cathay_id = self.transformer.get_cathay_id_from_cathay_cinema_name('')
                cathay_index_for_title = ''
            else:
                cathay_id = self.transformer.get_cathay_id_from_cathay_cinema_name(cathay_index)
                cathay_index_for_title = cathay_index
            try:
                current_cinema_all = self.driver.find_element_by_id(cathay_id)
            except common.exceptions.NoSuchElementException:  # end of list
                break

            cinema_name = capwords(self.driver.find_element_by_id('ContentPlaceHolder1_wucST{}_tab_title'
                                                                  .format(cathay_index_for_title)).text)

            if cinema_name == 'The Cathay':
                cinema_name = 'The Cathay Cineplex'
            else:
                cinema_name = "Cathay Cineplex " + cinema_name

            cinema_id = self.loader.get_cinema_id_from_name(cinema_name)

            cinema_iterators = self._get_cathay_cinema_iterator(current_cinema_all)
            date_iterator = self._get_cathay_date_iterator(current_cinema_all)

            for i in range(6):  # for each day
                current_date = GeneralTransformer.get_singapore_date(i)
                current_cinema = cinema_iterators[i]
                date_iterator[i].click()
                movie_iterator = self._get_cathay_movie_iterator(current_cinema)

                for current_movie in movie_iterator[:-1]:  # remove last no session container
                    movie_info = current_movie.find_elements_by_css_selector('a')
                    movie_title = self._get_cathay_movie_title(movie_info)
                    movie_timing = self._get_cathay_movie_timing(current_date, movie_info)
                    title, additional_info = self.transformer.parse_cathay_movie_title(movie_title)
                    self._package_schedule_data(additional_info, cinema_id, movie_timing, provider_schedule, title)

            cathay_index += 1

        return provider_schedule

    @staticmethod
    def _get_cathay_movie_iterator(current_cinema):
        return current_cinema.find_elements_by_class_name('movie-container')

    @staticmethod
    def _get_cathay_date_iterator(current_cinema_all):
        date_iterators = current_cinema_all.find_elements_by_class_name('caps')
        return date_iterators

    @staticmethod
    def _get_cathay_cinema_iterator(current_cinema_all):
        cinema_iterators = current_cinema_all.find_elements_by_class_name('tabbers')
        return cinema_iterators

    @staticmethod
    def _get_cathay_movie_title(movie_info):
        movie_title = movie_info[0].text
        return movie_title

    @staticmethod
    def _get_cathay_movie_timing(current_date, movie_info):
        movie_timing = []
        for current_timing in movie_info[1:]:
            movie_timing.append(current_date + " " + current_timing.text + ":00")
        return movie_timing

    # ============ Shaw Brother ============

    def get_sb_schedule(self):
        provider_schedule = {}

        for i in range(6):
            current_date = GeneralTransformer.get_singapore_date(i)
            sb_date = datetime.strptime(current_date, '%Y-%m-%d').strftime('%-m/%d/%Y')
            self.driver.get(self.SHAW_SCHEDULES.format(sb_date))

            cinema_iterators = self._get_sb_cinema_iterator()

            for current_cinema in cinema_iterators:
                cinema_name = current_cinema.find_element_by_class_name('txtScheduleHeaderCineplex').text
                cinema_name = capwords(cinema_name.split("(")[0].strip().replace('\n', ''))
                cinema_id = self.loader.get_cinema_id_from_name(cinema_name)
                movie_iterators = self._get_sb_movie_iterator(current_cinema)

                for movie_row in movie_iterators[2:]:  # remove table header

                    try:
                        movie_title, schedule = movie_row.text.strip().split("\n", 1)
                    except ValueError:
                        continue

                    if "PM" in schedule or "AM" in schedule:
                        movie_title = self._get_sb_single_movie_title(movie_title)
                        movie_timing = self._get_sb_single_movie_time(current_date, schedule)
                        title, additional_info = self.transformer.parse_sb_movie_title(movie_title)
                        self._package_schedule_data(additional_info, cinema_id, movie_timing, provider_schedule, title)

        return provider_schedule

    def _get_sb_cinema_iterator(self):
        return self.driver.find_elements_by_class_name('persist-area')

    @staticmethod
    def _get_sb_movie_iterator(current_cinema):
        return current_cinema.find_elements_by_class_name('panelSchedule')

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

    @staticmethod
    def _package_schedule_data(additional_info, cinema_id, movie_timing, provider_schedule, title):
        data_object = {
            "cinema_id": cinema_id,
            "schedule": movie_timing,
            "additional_info": additional_info
        }
        if title in provider_schedule:
            provider_schedule[title].append(data_object)
        else:
            provider_schedule[title] = [data_object]

