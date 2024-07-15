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
    LOCATIONS = (By.CLASS_NAME, 'cities')
    INFO = (By.CLASS_NAME, 'sh-info')
    DETAILS_SECTION = (By.CLASS_NAME, 'vacancy-section')
    DETAILS = (By.TAG_NAME, 'li')


class LuxoftLocators(BaseLocators):
    VACANCIES_CONTAINER = (By.CLASS_NAME, 'jobs__list')
    VACANCIES = (By.TAG_NAME, 'a')
    TITLE = (By.CLASS_NAME, 'subtitle-l')
    URL = (By.CLASS_NAME, 'vt')
    LOCATIONS = (By.CLASS_NAME, 'jobs__list__job__details__tags__location')
    DATE = (By.XPATH, '/html/body/div[10]/div[1]/div[4]/p')
    RESPONSIBILITIES = (By.CLASS_NAME, 'job__grid__about-job__responsabilities__list__item')
    SKILLS = (By.CLASS_NAME, 'job__grid__about-job__skills__list__item')


class GlobalLogicLocators(BaseLocators):
    VACANCIES_CONTAINER = (By.CLASS_NAME, 'spinner-controls')
    VACANCIES = (By.CLASS_NAME, 'career-pagelink')
    TITLE = (By.TAG_NAME, 'a')
    LOCATIONS = (By.CLASS_NAME, 'job-locations')
    SKILLS = (By.XPATH, '//*[@id="carersearchpage"]/div/div/div[1]/div[1]/div/table/tbody/tr[6]/td[2]')
    REQUIREMENTS = (By.XPATH, '//*[@id="carersearchpage"]/div/div/div[1]/div[4]/p')
    RESPONSIBILITIES = (By.XPATH, '//*[@id="carersearchpage"]/div/div/div[1]/div[5]/p')
