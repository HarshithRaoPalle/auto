
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from config.environment import config
from utils.logger import get_logger


logger = get_logger()


def get_chrome_options():

    chrome_options = Options()

    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    return chrome_options


def get_driver():

    chrome_options = get_chrome_options()

    if config.execution.lower() == "remote":

        driver = webdriver.Remote(
            command_executor=config.grid_url,
            options=chrome_options
        )

        logger.info(
            "Remote Chrome browser launched"
        )

    else:

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

        logger.info(
            "Local Chrome browser launched"
        )

    driver.set_page_load_timeout(60)
    driver.implicitly_wait(5)

    return driver
