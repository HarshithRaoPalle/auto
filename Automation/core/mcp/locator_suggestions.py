"""Longcat helper for improving Selenium locators."""

from core.mcp.client import LongcatClient
from utils.logger import get_logger


logger = get_logger()


def suggest_locator(
    html: str,
    failed_locator: tuple[str, str],
    client: LongcatClient | None = None,
) -> str:
    """Ask Longcat to suggest better Selenium locators for a failed element."""

    prompt = f"""
Suggest stable Selenium locators for this failed locator.

Failed locator:
{failed_locator}

HTML snippet:
{html}

Return concise locator suggestions using ID, NAME, CSS_SELECTOR, or XPATH.
Prefer data-testid, id, name, and accessible labels when present.
""".strip()

    logger.info("Requesting Longcat locator suggestions for: %s", failed_locator)
    return (client or LongcatClient()).ask_longcat(prompt)
