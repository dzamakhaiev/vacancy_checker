from time import sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from drivers import ChromeDriver
import locators


def no_such_element_exception(find):
    def wrap(self, *args, **kwargs):
        try:
            return find(self, *args, **kwargs)
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(e)
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

    def click_on_element(self, locator, element=None):
        if not element:
            element = self.driver.find_element(*locator)

        if element.is_displayed():
            element.click()
            sleep(1)


class DouVacanciesPage(BasePage):

    def get_all_vacancies(self):
        self.click_on_element(locator=locators.DouLocators.MORE_BUTTON)
        items = self.find_elements(locator=locators.DouLocators.VACANCIES)

        if items:
            return items
        else:
            return []
