import locators
from drivers import ChromeDriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException


def no_such_element_exception(find):
    def wrap(self, *args, **kwargs):
        try:
            return find(self, *args, **kwargs)
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    return wrap


class BasePage:

    def __init__(self, driver: (ChromeDriver,)):
        chrome_driver = driver()
        self.driver = chrome_driver.get_driver()

    def go_to(self, url):
        try:
            self.driver.get(url)
        except TimeoutException:
            quit(f'Cannot load page: {url}')

    @no_such_element_exception
    def find_element(self, locator, element=None):
        if not element:
            return self.driver.find_element(*locator)
        else:
            return element.find_element(*locator)

    @no_such_element_exception
    def find_elements(self, locator, element=None):

        if not element:
            return self.driver.find_elements(*locator)
        else:
            return element.find_elements(*locator)
