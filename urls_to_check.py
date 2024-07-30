import pages
import drivers


URLS_TO_CHECK = {
    'dou': {'url': 'https://jobs.dou.ua/vacancies/?category=QA&search=automation+python&descr=1',
            'page': pages.DouVacanciesPage, 'driver': drivers.FirefoxDriver},
    'luxoft': {'url': 'https://career.luxoft.com/jobs?keyword=qa%20automation&country[]=Ukraine&perPage=60',
               'page': pages.LuxoftVacanciesPage, 'driver': drivers.FirefoxDriver},
    'globallogic': {'url': 'https://www.globallogic.com/ua/career-search-page/'
                           '?keywords=qa+automation&experience=&locations=ukraine&c=&workmodel=Remote',
                    'page': pages.GlobalLogicVacanciesPage, 'driver': drivers.FirefoxDriver}
}
