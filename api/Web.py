# coding=utf-8
import abc
from contextlib import contextmanager
from os.path import dirname, realpath

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait


class WebDriverAPI(object):
    __exe_path = dirname(dirname(realpath(__file__))) + "/phantomjs"
    __debug_path = "/phantomjs"

    def __init__(self):
        self.driver = PhantomJS(self.__exe_path)
        self.driver.maximize_window()

    def get(self, url):
        with self.__wait_for_element():
            self.driver.get(url)

    @contextmanager
    def __wait_for_element(self, timeout=30):
        element = self.driver.find_element_by_tag_name("html")
        yield
        WebDriverWait(self.driver, timeout).until(staleness_of(element))

    def get_class_e(self, class_name):
        try:
            return WebDriverWait(self.driver, 1, 0.2).until(lambda d: d.find_element_by_class_name(class_name))
        except TimeoutException:
            return None

    def get_xpath_e(self, xpath):
        try:
            return WebDriverWait(self.driver, 1, 0.2).until(lambda d: d.find_element_by_xpath(xpath))
        except TimeoutException:
            return None

    def get_css_e(self, css):
        try:
            return WebDriverWait(self.driver, 1, 0.2).until(lambda d: d.find_element_by_css_selector(css))
        except TimeoutException:
            return None

    @abc.abstractmethod
    def click_condition(self): return True

    def click(self, element, iterations=1):
        # TODO: check vars
        for i in range(iterations):
            element.click()
            if self.click_condition():
                return True
        return False

    def get_tabs_count(self):
        return len(self.driver.window_handles)

    def get_tabs(self):
        return self.driver.window_handles

    def close_tabs(self, *args):
        pass

    def close_all_except_one(self, select=0):
        if len(self.get_tabs()) >= select:
            if self.get_tabs_count() > 1:
                for i in range(self.get_tabs_count()):
                    if self.switch_to_tab(i):
                        self.driver.close()
                self.switch_to_tab(select)
            else:
                return

    def switch_to_tab(self, i):
        try:
            tab = self.driver.window_handles[i]
            self.driver.switch_to.window(tab)
            return True
        except IndexError:
            return False

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def get_page(self):
        return self.driver.page_source
