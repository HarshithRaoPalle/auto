"""Centralized explicit wait helpers for Selenium page objects."""

from typing import Any, Tuple

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.environment import config
from utils.logger import get_logger


Locator = Tuple[str, str]
logger = get_logger()


class IntelligentWaits:
    """Reusable explicit waits with consistent logging."""

    def __init__(
        self,
        driver: WebDriver,
        timeout: int | None = None,
        poll_frequency: float = 1,
    ) -> None:
        self.driver = driver
        self.timeout = timeout or config.timeout
        self.poll_frequency = poll_frequency

    def _wait(self, timeout: int | None = None) -> WebDriverWait:
        return WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency,
            ignored_exceptions=[StaleElementReferenceException],
        )

    def wait_for_visible(self, locator: Locator, timeout: int | None = None) -> Any:
        """Wait until an element is visible."""

        logger.info("Waiting for visible element: %s", locator)
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Locator, timeout: int | None = None) -> Any:
        """Wait until an element is visible and enabled for clicking."""

        logger.info("Waiting for clickable element: %s", locator)
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, locator: Locator, timeout: int | None = None) -> Any:
        """Wait until an element exists in the DOM."""

        logger.info("Waiting for element presence: %s", locator)
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_page_load(self, timeout: int = 40) -> bool:
        """Wait until the browser reports a fully loaded document."""

        logger.info("Waiting for page load")
        return self._wait(timeout).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
