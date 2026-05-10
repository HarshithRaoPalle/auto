from selenium.webdriver.common.by import By

from pages.base_page import BasePage

from utils.logger import get_logger


logger = get_logger()


class LoginPage(BasePage):

    # =========================
    # LOCATORS
    # =========================

    OPEN_LOGIN = (
        By.XPATH,
        "//a[text()='Login']"
    )

    EMAIL = (
        By.CSS_SELECTOR,
        "input[data-testid='login-email']"
    )

    PASSWORD = (
        By.CSS_SELECTOR,
        "input[data-testid='login-password']"
    )

    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='login-submit']"
    )

    ADD_NOTE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='add-new-note']"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-testid='alert-message']"
    )

    # =========================
    # METHODS
    # =========================

    def login(self, email, password):

        logger.info("Performing login")

        self.wait_for_visibility(self.EMAIL)

        self.safe_send_keys(self.EMAIL, email)

        self.safe_send_keys(self.PASSWORD, password)

        self.safe_click(self.LOGIN_BUTTON)

    def is_login_successful(self):

        logger.info("Checking login success")

        return self.is_visible(
            self.ADD_NOTE_BUTTON
        )

    def get_error_message(self):

        logger.info("Waiting for error message")

        element = self.wait_for_visibility(
            self.ERROR_MESSAGE
        )

        return element.text
