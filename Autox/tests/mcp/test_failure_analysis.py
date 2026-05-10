import os

import pytest
from dotenv import load_dotenv

from config.environment import config
from core.mcp.failure_analysis import analyze_failure


load_dotenv()


@pytest.mark.ui
@pytest.mark.flaky(reruns=0)
def test_launch_application(driver) -> None:
    expected_title = "Notex"

    driver.get(config.base_url)
    actual_title = driver.title

    if expected_title not in actual_title:
        if os.getenv("LONGCAT_API_KEY") and os.getenv("LONGCAT_BASE_URL"):
            reason = analyze_failure(expected_title, actual_title)
            print(f"\nMCP failure reason: {reason}")

    assert expected_title in actual_title
