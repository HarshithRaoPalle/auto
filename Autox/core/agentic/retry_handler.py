"""Reusable retry support for flaky Selenium actions."""

from functools import wraps
from time import sleep
from typing import Any, Callable, Iterable, TypeVar

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)

from utils.logger import get_logger


F = TypeVar("F", bound=Callable[..., Any])
logger = get_logger()

DEFAULT_RETRY_EXCEPTIONS = (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


def retry_on_flaky_action(
    retries: int = 3,
    delay: float = 1,
    exceptions: Iterable[type[Exception]] = DEFAULT_RETRY_EXCEPTIONS,
) -> Callable[[F], F]:
    """Retry a Selenium action when a known flaky exception is raised."""

    retry_exceptions = tuple(exceptions)

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as exc:
                    last_exception = exc
                    logger.warning(
                        "Retry %s/%s after %s in %s",
                        attempt,
                        retries,
                        exc.__class__.__name__,
                        func.__name__,
                    )
                    if attempt < retries:
                        sleep(delay)

            if last_exception:
                logger.error(
                    "Action %s failed after %s retries: %s",
                    func.__name__,
                    retries,
                    last_exception,
                )
                raise last_exception

            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
