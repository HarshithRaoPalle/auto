"""Simple retry decisions for Selenium failures."""

from enum import Enum

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

from utils.logger import get_logger


logger = get_logger()


class RetryDecision(str, Enum):
    """Actions the framework can take after a Selenium failure."""

    RETRY = "RETRY"
    FAIL_FAST = "FAIL_FAST"
    HEAL_AND_RETRY = "HEAL_AND_RETRY"


RETRY_EXCEPTIONS = (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

HEALABLE_EXCEPTIONS = (
    TimeoutException,
    NoSuchElementException,
)


def decide_action(exception: Exception, locator: tuple | None = None) -> RetryDecision:
    """Return a safe action for the given failure."""

    if isinstance(exception, AssertionError):
        logger.info("Decision: FAIL_FAST for assertion failure")
        return RetryDecision.FAIL_FAST

    if locator and isinstance(exception, HEALABLE_EXCEPTIONS):
        logger.info("Decision: HEAL_AND_RETRY for %s", locator)
        return RetryDecision.HEAL_AND_RETRY

    if isinstance(exception, RETRY_EXCEPTIONS):
        logger.info("Decision: RETRY for recoverable Selenium failure")
        return RetryDecision.RETRY

    logger.info("Decision: FAIL_FAST for non-recoverable failure")
    return RetryDecision.FAIL_FAST
