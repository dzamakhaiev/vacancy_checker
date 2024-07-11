from selenium.webdriver.common.by import By


class BaseLocators:
    HTML = (By.TAG_NAME, 'html')


class DouLocators(BaseLocators):
    VACANCIES = (By.CLASS_NAME, 'l-vacancy')
    MORE_BUTTON = (By.CLASS_NAME, 'more-btn')
