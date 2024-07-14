import pages
import drivers
import locators


URLS_TO_CHECK = {
    'dou': {'url': 'https://jobs.dou.ua/vacancies/?category=QA&search=automation+python&descr=1',
            'locators': locators.DouLocators, 'page': pages.DouVacanciesPage, 'driver': drivers.ChromeDriver},
    'luxoft': {'url': 'https://career.luxoft.com/jobs?keyword=qa%20automation&country[]=Ukraine&perPage=60',
               'locators': locators.LuxoftLocators, 'page': pages.LuxoftVacanciesPage, 'driver': drivers.ChromeDriver}
}
