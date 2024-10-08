import platform
from selenium import webdriver
from latest_user_agents import get_random_user_agent
from logger import Logger


logger = Logger('driver')


class BaseDriver:

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, driver: (webdriver.Chrome,)):
        logger.info(f'Platform: {platform.system()}: {platform.release()}')
        logger.info('Initiate driver.')
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def get_driver(self) -> webdriver.Chrome:
        return self.driver

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
            logger.info('Driver closed.')


class ChromeDriver(BaseDriver):

    def __init__(self):
        service = webdriver.ChromeService()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent={get_random_user_agent()}')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(service=service, options=options)

        super().__init__(driver)
        logger.info('Chrome driver started.')


class FirefoxDriver(BaseDriver):

    def __init__(self):
        service = webdriver.FirefoxService()
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument(f'user-agent={get_random_user_agent()}')
        driver = webdriver.Firefox(service=service, options=options)

        super().__init__(driver)
        logger.info('Firefox driver started.')
