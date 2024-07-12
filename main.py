from time import sleep
from urls_to_check import URLS_TO_CHECK
from sqlite_handler import DatabaseHandler
from email_sender import send_email


db_handler = DatabaseHandler()


def filter_vacancies(vacancies: dict):
    vacancies_db = db_handler.get_vacancies()
    for vacancy in vacancies_db:
        vacancy_id = vacancy[0]

        if vacancy_id in vacancies:
            vacancies.pop(vacancy_id)


def send_vacancies_to_email(website_name):
    vacancies_db = db_handler.get_not_notified_vacancies()
    for vacancy in vacancies_db:
        vacancy_id, title, company, info, cities, date, url, notified = vacancy

        if not bool(notified):

            body = (f'{title}: {company}\n'
                    f'{cities}, {date}\n'
                    f'{info}\n'
                    f'{url}')
            email_sent = send_email(website_name, body)
            sleep(1)

            if email_sent:
                db_handler.change_vacancy_notify_state(vacancy_id)


def main_loop():

    for website_name, data in URLS_TO_CHECK.items():
        url = data.get('url')
        page_class = data.get('page')
        driver_class = data.get('driver')

        page = page_class(driver=driver_class)
        page.go_to(url)
        vacancies = page.get_all_vacancies()

        filter_vacancies(vacancies)
        db_handler.insert_vacancies(vacancies)
        send_vacancies_to_email(website_name)


if __name__ == '__main__':
    main_loop()
