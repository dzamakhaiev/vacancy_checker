from time import sleep
from datetime import date
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException,
                                        TimeoutException, WebDriverException)
from drivers import ChromeDriver
import locators
from logger import Logger


logger = Logger('pages')


def no_such_element_exception(find):
    def wrap(self, *args, **kwargs):
        try:
            return find(self, *args, **kwargs)
        except (NoSuchElementException, StaleElementReferenceException) as e:
            logger.error(e)
            return None

    return wrap


class BasePage:

    def __init__(self, driver: (ChromeDriver,)):
        self.driver = None
        self.driver_class = driver
        self.set_driver()

    def set_driver(self):
        driver = self.driver_class()
        self.driver = driver.get_driver()

    def go_to(self, url):
        logger.info(f'Go to url: {url}')
        try:
            self.driver.get(url)
            sleep(1)
        except TimeoutException:
            quit(f'Cannot load page: {url}')

    @no_such_element_exception
    def find_element(self, locator, element=None):
        logger.debug(f'Find element with locator "{locator}". Element provided: {element}')

        if not element:
            return self.driver.find_element(*locator)
        else:
            return element.find_element(*locator)

    @no_such_element_exception
    def find_elements(self, locator, element=None):
        logger.debug(f'Find elements with locator "{locator}". Element provided: {element}')

        if not element:
            return self.driver.find_elements(*locator)
        else:
            return element.find_elements(*locator)

    def click_on_element(self, locator, element=None):
        logger.debug(f'Click on element with locator "{locator}". Element provided: {element}')

        if not element:
            element = self.driver.find_element(*locator)

        if element.is_displayed():
            element.click()
            sleep(1)


class DouVacanciesPage(BasePage):

    def vacancy_details(self, vacancies: dict):
        logger.info('Parse vacancy details.')

        for vacancy_id, vacancy_dict in vacancies.items():
            url = vacancy_dict.get('url')
            try:
                self.go_to(url)

                info = vacancy_dict.get('info')
                details_section = self.find_element(locator=locators.DouLocators.DETAILS_SECTION)

                info += '\nDETAILS:\n'
                elements = self.find_elements(element=details_section, locator=locators.DouLocators.DETAILS)
                info += '\n'.join([element.text for element in elements])
                vacancies[vacancy_id]['info'] = info

            except WebDriverException as e:
                logger.error(e)
                self.set_driver()

        logger.info('Details parsed.')

    def get_all_vacancies(self):
        logger.info('Collect all vacancies from current page.')
        vacancies = {}
        elements = self.find_elements(locator=locators.DouLocators.VACANCIES)

        if elements:
            logger.info('Parse all found elements on current page.')

            for element in elements:

                vacancy_date = self.find_element(element=element, locator=locators.DouLocators.DATE)
                vacancy_date = vacancy_date.text
                vacancy_day = int(vacancy_date.split(' ')[0])
                current_date = date.today()

                if vacancy_day > current_date.day:
                    vacancy_date = date(year=current_date.year, month=current_date.month-1, day=vacancy_day)
                else:
                    vacancy_date = date(year=current_date.year, month=current_date.month, day=vacancy_day)

                title = self.find_element(element=element, locator=locators.DouLocators.TITLE)
                url = self.find_element(element=title, locator=locators.DouLocators.URL)
                vacancy_title = url.text
                url = url.get_attribute('href')
                vacancy_id = url.split('/')[-2]

                company = self.find_element(element=title, locator=locators.DouLocators.COMPANY)
                company = self.find_element(element=company, locator=locators.DouLocators.COMPANY_NAME)
                company = company.text
                company = company.strip()

                locations = self.find_element(element=title, locator=locators.DouLocators.LOCATIONS)
                locations = locations.text
                info = self.find_element(element=element, locator=locators.DouLocators.INFO)
                info = info.text if info else info

                vacancies.update({vacancy_id: {'url': url, 'date': vacancy_date, 'title': vacancy_title,
                                               'locations': locations, 'info': info, 'company': company}})

        logger.info('Elements parsed.')
        self.vacancy_details(vacancies)
        return vacancies


class LuxoftVacanciesPage(BasePage):

    def vacancy_details(self, vacancies: dict):
        logger.info('Parse vacancy details.')

        for vacancy_id, vacancy_dict in vacancies.items():
            url = vacancy_dict.get('url')

            try:
                self.go_to(url)

                info = vacancy_dict.get('info')
                info += '\nResponsibilities:\n'
                elements = self.find_elements(locator=locators.LuxoftLocators.RESPONSIBILITIES)
                info += '\n'.join([element.text for element in elements])

                info += '\nSkills:\n'
                elements = self.find_elements(locator=locators.LuxoftLocators.SKILLS)
                info += '\n'.join([element.text for element in elements])
                vacancies[vacancy_id]['info'] = info

                vacancy_date = self.find_element(locator=locators.LuxoftLocators.DATE).text
                vacancy_date = vacancy_date.split('/')[::-1]
                vacancy_date = date(year=int(vacancy_date[0]), month=int(vacancy_date[1]), day=int(vacancy_date[2]))
                vacancies[vacancy_id]['date'] = vacancy_date

            except WebDriverException as e:
                logger.error(e)
                self.set_driver()

    logger.info('Details parsed.')

    def get_all_vacancies(self):
        logger.info('Collect all vacancies from current page.')
        vacancies = {}
        element = self.find_element(locator=locators.LuxoftLocators.VACANCIES_CONTAINER)
        elements = self.find_elements(element=element, locator=locators.LuxoftLocators.VACANCIES)

        if elements:
            logger.info('Parse all found elements on current page.')

            for element in elements:

                title = self.find_element(element=element, locator=locators.LuxoftLocators.TITLE)
                vacancy_title = title.text
                url = element.get_attribute('href')
                vacancy_id = url.split('-')[-1]

                locations = self.find_element(element=element, locator=locators.LuxoftLocators.LOCATIONS)
                locations = locations.text
                vacancies.update({vacancy_id: {'url': url, 'date': date.today(), 'title': vacancy_title,
                                               'locations': locations, 'info': '', 'company': 'luxoft'}})

        logger.info('Elements parsed.')

        self.vacancy_details(vacancies)
        return vacancies
