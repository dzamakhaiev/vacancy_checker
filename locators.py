from selenium.webdriver.common.by import By


class BaseLocators:
    HTML = (By.TAG_NAME, 'html')


class DouLocators(BaseLocators):
    VACANCIES = (By.CLASS_NAME, 'l-vacancy')
    MORE_BUTTON = (By.CLASS_NAME, 'more-btn')
    DATE = (By.CLASS_NAME, 'date')
    TITLE = (By.CLASS_NAME, 'title')
    COMPANY = (By.TAG_NAME, 'strong')
    COMPANY_NAME = (By.CLASS_NAME, 'company')
    URL = (By.CLASS_NAME, 'vt')
    CITIES = (By.CLASS_NAME, 'cities')
    INFO = (By.CLASS_NAME, 'sh-info')

