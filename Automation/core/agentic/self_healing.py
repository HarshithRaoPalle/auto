"""Simple self-healing locator support."""

from typing import Iterable, Optional, Tuple

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from utils.logger import get_logger


Locator = Tuple[str, str]
logger = get_logger()


class SelfHealingLocator:
    """Try simple fallback locators when the original locator fails."""

    FALLBACK_STRATEGIES = (
        By.ID,
        By.NAME,
        By.CSS_SELECTOR,
        By.XPATH,
        By.PARTIAL_LINK_TEXT,
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def heal(self, failed_locator: Locator) -> Optional[Locator]:
        """Return the first fallback locator that finds an element."""

        logger.info("Starting locator healing for: %s", failed_locator)
        original_implicit_wait = self._get_implicit_wait()

        try:
            self.driver.implicitly_wait(0)

            for locator in self._candidate_locators(failed_locator):
                if locator == failed_locator:
                    continue

                try:
                    logger.info("Trying healed locator candidate: %s", locator)
                    elements = self.driver.find_elements(*locator)
                    if elements:
                        logger.info("Healed locator found: %s", locator)
                        return locator
                except WebDriverException as exc:
                    logger.warning("Locator candidate failed %s: %s", locator, exc)

        finally:
            self.driver.implicitly_wait(original_implicit_wait)

        logger.warning("Unable to heal locator: %s", failed_locator)
        return None

    def _candidate_locators(self, failed_locator: Locator) -> Iterable[Locator]:
        by, value = failed_locator
        cleaned = value.strip()

        simple_value = self._simple_value(cleaned)
        if simple_value:
            yield (By.ID, simple_value)
            yield (By.NAME, simple_value)
            yield (By.CSS_SELECTOR, f"[data-testid='{simple_value}']")
            yield (By.CSS_SELECTOR, f"#{simple_value}")
            yield (By.CSS_SELECTOR, f"[name='{simple_value}']")
            yield (By.XPATH, f"//*[@id='{simple_value}' or @name='{simple_value}']")
            yield (By.PARTIAL_LINK_TEXT, simple_value)

        if by == By.CSS_SELECTOR and cleaned.startswith(("#", ".", "[")):
            yield (By.CSS_SELECTOR, cleaned)
        elif by in (By.XPATH, By.PARTIAL_LINK_TEXT) and cleaned:
            yield (by, cleaned)

    @staticmethod
    def _simple_value(value: str) -> str:
        """Extract a reusable token from common Selenium locator values."""

        if value.startswith("#"):
            return value[1:]

        if "data-testid" in value:
            return (
                value.replace("[data-testid=", "")
                .replace("]", "")
                .replace("'", "")
                .replace('"', "")
            )

        if value.startswith("//") or value.startswith("("):
            return ""

        return value

    def _get_implicit_wait(self) -> float:
        """Read Selenium implicit wait timeout with a safe fallback."""

        try:
            return float(self.driver.timeouts.implicit_wait)
        except Exception:
            return 0
