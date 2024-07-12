import sqlite3
from logger import Logger


logger = Logger('database')


class DatabaseHandler:

    def __init__(self):
        try:
            self.conn = sqlite3.connect('database/vacancies.db')
            self.cursor = self.conn.cursor()
            self.create_vacancies_table()
            logger.info('SQLite database connection opened.')

        except sqlite3.Error as e:
            logger.error(e)
            quit(e)

    def cursor_execute(self, query, args=None):
        logger.debug(f'Query for execute: {query}\nWith args: {args}')
        if args is None:
            args = tuple()

        try:
            result = self.cursor.execute(query, args)
            return result

        except sqlite3.DatabaseError as e:
            logger.error(e)
            self.conn.rollback()

    def cursor_with_commit(self, query, args=None, many=False):
        logger.debug(f'Query for commit: {query}\nWith args: {args}')
        if args is None:
            args = []

        try:
            if many:
                self.cursor.executemany(query, args)
            elif query.startswith('DELETE'):
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, args)
            self.conn.commit()

        except sqlite3.DatabaseError as e:
            logger.error(e)
            self.conn.rollback()

    def create_vacancies_table(self):
        logger.info('Table for vacancies created.')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS vacancies
                    (vacancy_id TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    info TEXT NOT NULL,
                    cities TEXT,
                    date TEXT,
                    url TEXT,
                    notified BOOLEAN DEFAULT 0)
                    ''')

    def get_vacancies(self):
        result = self.cursor_execute('SELECT * FROM vacancies ORDER BY date DESC')
        if result:
            return result.fetchall()
        else:
            return []

    def get_not_notified_vacancies(self):
        result = self.cursor_execute('SELECT * FROM vacancies WHERE notified = 0')
        if result:
            return result.fetchall()
        else:
            return []

    def check_vacancy(self, vacancy_id):
        result = self.cursor_execute('SELECT * FROM vacancies WHERE vacancy_id = ?', (vacancy_id,))
        if result:
            return True
        else:
            return False

    def insert_vacancy(self, vacancy_id: str, vacancy_dict: dict):
        self.cursor_with_commit('INSERT OR IGNORE INTO vacancies '
                                '(vacancy_id, title, company, info, cities, date, url)'
                                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (vacancy_id, vacancy_dict.get('title'), vacancy_dict.get('company'),
                                 vacancy_dict.get('info'), vacancy_dict.get('cities'), vacancy_dict.get('date'),
                                 vacancy_dict.get('url')))

    def insert_vacancies(self, vacancies: dict):
        args = []
        for vacancy_id, vacancy_dict in vacancies.items():
            args.append((vacancy_id, vacancy_dict.get('title'), vacancy_dict.get('company'),
                         vacancy_dict.get('info'), vacancy_dict.get('cities'), vacancy_dict.get('date'),
                         vacancy_dict.get('url')))

        self.cursor_with_commit('INSERT OR IGNORE INTO vacancies '
                                '(vacancy_id, title, company, info, cities, date, url)'
                                ' VALUES (?, ?, ?, ?, ?, ?, ?)', args=args, many=True)

    def change_vacancy_notify_state(self, vacancy_id):
        self.cursor_with_commit('UPDATE vacancies SET notified = 1 WHERE vacancy_id = ?', (vacancy_id,))

    def delete_outdated_vacancies(self, days=30):
        self.cursor_with_commit(
            f"DELETE FROM vacancies WHERE DATE(date) < DATE('now', '-{days} days')")

    def __del__(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
            logger.info('SQLite database connection closed.')
