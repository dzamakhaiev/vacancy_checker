from selenium import webdriver
from latest_user_agents import get_random_user_agent


class BaseDriver:

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, driver: (webdriver.Chrome, webdriver.Edge)):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()


class ChromeDriver(BaseDriver):

    def __init__(self):
        service = webdriver.ChromeService()
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={get_random_user_agent()}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(service=service, options=options)
        super().__init__(driver)

