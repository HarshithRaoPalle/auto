
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from selenium.webdriver.support.ui import WebDriverWait

from config.environment import config
from core.agentic.decision_engine import RetryDecision, decide_action
from core.agentic.intelligent_waits import IntelligentWaits
from core.agentic.self_healing import SelfHealingLocator
from utils.logger import get_logger
from time import sleep

logger = get_logger()


class BasePage:

    def __init__(self, driver):

        self.driver = driver
        self.smart_waits = IntelligentWaits(driver)
        self.self_healer = SelfHealingLocator(driver)

        self.wait = WebDriverWait(
            driver,
            config.timeout,
            poll_frequency=1,
            ignored_exceptions=[
                StaleElementReferenceException
            ]
        )

    def open_url(self, url):

        logger.info(f"Opening URL: {url}")

        self.driver.get(url)

        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=40):

        return self.smart_waits.wait_for_page_load(timeout)

    def retry_action(
        self,
        action,
        retries=3,
        delay=2,
        locator=None
    ):

        last_exception = None

        for attempt in range(retries):

            try:

                return action()

            except Exception as e:

                last_exception = e
                decision = decide_action(e, locator)

                if decision == RetryDecision.FAIL_FAST:
                    logger.error(
                        "Fail-fast decision for %s: %s",
                        e.__class__.__name__,
                        e
                    )
                    raise

                logger.warning(
                    f"Retry attempt "
                    f"{attempt + 1}/{retries} "
                    f"after {e.__class__.__name__}"
                )

                if attempt < retries - 1:
                    sleep(delay)

        raise last_exception

    def _heal_locator(self, locator):

        healed_locator = self.self_healer.heal(locator)

        if healed_locator:
            logger.info(
                "Using healed locator %s instead of %s",
                healed_locator,
                locator
            )
            return healed_locator

        return locator

    def _wait_with_healing(self, locator, wait_method):

        try:

            return wait_method(locator)

        except Exception as e:

            decision = decide_action(e, locator)

            if decision != RetryDecision.HEAL_AND_RETRY:
                raise

            healed_locator = self._heal_locator(locator)

            if healed_locator == locator:
                raise

            return wait_method(healed_locator)

    def click(self, locator):

        def action():

            logger.info(
                f"Clicking element: {locator}"
            )

            element = self._wait_with_healing(
                locator,
                self.smart_waits.wait_for_clickable
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView("
                "{block: 'center'});",
                element
            )

            try:
                element.click()

            except (
                ElementClickInterceptedException,
                ElementNotInteractableException
            ):

                logger.warning(
                    "Normal click failed. "
                    "Trying JS click."
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

        return self.retry_action(action, locator=locator)

    def send_keys(self, locator, text):

        def action():

            logger.info(
                f"Entering text into {locator}"
            )

            element = self._wait_with_healing(
                locator,
                self.smart_waits.wait_for_visible
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView("
                "{block: 'center'});",
                element
            )

            element.clear()

            element.send_keys(text)

        return self.retry_action(action, locator=locator)

    def enter_text(self, locator, text):

        return self.send_keys(locator, text)

    def find_element(self, locator):

        return self._wait_with_healing(
            locator,
            self.smart_waits.wait_for_presence
        )

    def get_text(self, locator):

        element = self._wait_with_healing(
            locator,
            self.smart_waits.wait_for_visible
        )

        return element.text.strip()

    def is_visible(self, locator):

        try:

            self._wait_with_healing(
                locator,
                self.smart_waits.wait_for_visible
            )

            return True

        except TimeoutException:

            return False

    def wait_for_visibility(self, locator):

        return self._wait_with_healing(
            locator,
            self.smart_waits.wait_for_visible
        )

    def wait_for_clickable(self, locator):

        return self._wait_with_healing(
            locator,
            self.smart_waits.wait_for_clickable
        )

    def wait_for_presence(self, locator):

        return self._wait_with_healing(
            locator,
            self.smart_waits.wait_for_presence
        )

    def safe_click(self, locator):

        return self.click(locator)

    def safe_send_keys(
        self,
        locator,
        text
    ):

        return self.send_keys(
            locator,
            text
        )
