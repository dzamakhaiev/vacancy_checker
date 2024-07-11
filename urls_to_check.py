import pages
import drivers
import locators


URLS_TO_CHECK = {
    'dou': {'url': 'https://jobs.dou.ua/vacancies/?category=QA&search=automation+python&descr=1',
            'locators': locators.DouLocators, 'page': pages.DouVacanciesPage, 'driver': drivers.ChromeDriver}
}
