from urls_to_check import URLS_TO_CHECK
from sqlite_handler import DatabaseHandler


db_handler = DatabaseHandler()


def filter_vacancies(vacancies: dict):
    vacancies_db = db_handler.get_vacancies()
    for vacancy in vacancies_db:
        vacancy_id = vacancy[0]

        if vacancy_id in vacancies:
            vacancies.pop(vacancy_id)


def main_loop():

    for website_name, data in URLS_TO_CHECK.items():
        url = data.get('url')
        page_class = data.get('page')
        driver_class = data.get('driver')

        page = page_class(driver=driver_class)
        page.go_to(url)
        vacancies = page.get_all_vacancies()
        print(vacancies)

        filter_vacancies(vacancies)
        print(vacancies)

        db_handler.insert_vacancies(vacancies)
        vacancies_db = db_handler.get_vacancies()
        print(vacancies_db)


if __name__ == '__main__':
    main_loop()
