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
        vacancies = {}
        elements = self.find_elements(locator=locators.DouLocators.VACANCIES)

        if elements:
            for element in elements:

                date = self.find_element(element=element, locator=locators.DouLocators.DATE)
                date = date.text if date else date

                title = self.find_element(element=element, locator=locators.DouLocators.TITLE)
                url = self.find_element(element=title, locator=locators.DouLocators.URL)
                vacancy_title = url.text
                url = url.get_attribute('href')
                vacancy_id = url.split('/')[-2]

                company = self.find_element(element=title, locator=locators.DouLocators.COMPANY)
                company = self.find_element(element=company, locator=locators.DouLocators.COMPANY_NAME)
                company = company.text

                cities = self.find_element(element=title, locator=locators.DouLocators.CITIES)
                cities = cities.text
                info = self.find_element(element=element, locator=locators.DouLocators.INFO)
                info = info.text if info else info

                vacancies.update({vacancy_id: {'url': url, 'date': date, 'title': vacancy_title, 'cities': cities,
                                               'info': info, 'company': company}})

        return vacancies
