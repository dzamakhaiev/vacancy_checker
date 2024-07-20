import os
from time import sleep
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from urls_to_check import URLS_TO_CHECK
from sqlite_handler import DatabaseHandler
from email_sender import send_email
from logger import Logger


logger = Logger('main')
db_handler = DatabaseHandler()
CHECK_INTERVAL = 60 * int(os.environ.get('CHECK_INTERVAL_MINUTES', default=30))
msg = 'Interval between checks: {} seconds. ENV variable: {}'.format(
    CHECK_INTERVAL, os.environ.get('CHECK_INTERVAL_MINUTES'))
logger.info(msg)


def filter_vacancies(vacancies: dict):
    logger.info('Filter found vacancies.')

    vacancies_db = db_handler.get_vacancies()
    for vacancy in vacancies_db:
        vacancy_id = vacancy[0]

        if vacancy_id in vacancies:
            logger.debug(f'Vacancy "{vacancy_id}" was removed as duplicated.')
            vacancies.pop(vacancy_id)

    logger.info(f'New vacancies found: {len(vacancies)}')
    logger.info('All vacancies were filtered.')


def send_vacancies_to_email(website_name):
    logger.info(f'Send email with new vacancies for website: {website_name}')
    vacancies_db = db_handler.get_not_notified_vacancies()

    for vacancy in vacancies_db:
        vacancy_id, title, company, info, locations, date, url, notified = vacancy

        if not bool(notified):
            logger.info(f'New vacancy found: {title}')

            body = (f'{title}: {company}\n'
                    f'{locations}, {date}\n'
                    f'{info}\n'
                    f'{url}')
            email_sent = send_email(website_name, body)
            sleep(1)

            if email_sent:
                db_handler.change_vacancy_notify_state(vacancy_id)


def sleep_dynamic():
    current_time = datetime.now(tz=ZoneInfo("Europe/Athens"))
    start_hour = 8
    end_hour = 22

    if start_hour <= current_time.hour <= end_hour:
        logger.info(f'Sleep on {CHECK_INTERVAL} seconds before next check.')
        sleep(CHECK_INTERVAL)

    else:
        hours = 24 - current_time.hour + start_hour
        minutes = 60 - current_time.minute + (hours - 1) * 60  # minus almose full hour "60 - minutes"
        seconds = minutes * 60
        logger.info(f'Sleep on {seconds} seconds till the morning.')
        sleep(seconds)


def main_loop():

    for website_name, data in URLS_TO_CHECK.items():
        logger.info(f'Start parsing website: {website_name}')
        url = data.get('url')
        page_class = data.get('page')
        driver_class = data.get('driver')

        page = page_class(driver=driver_class)
        page.go_to(url)
        vacancies = page.get_all_vacancies()

        logger.info('Process found vacancies: filter, insert new ones and remove old ones.')
        filter_vacancies(vacancies)
        page.vacancy_details(vacancies)
        db_handler.insert_vacancies(vacancies)
        db_handler.delete_outdated_vacancies()

        logger.info('Send found vacancies via email.')
        send_vacancies_to_email(website_name)


if __name__ == '__main__':
    while True:
        try:
            main_loop()
            sleep_dynamic()
        except KeyboardInterrupt:
            break
