import json
import os
import platform
from pathlib import Path

import allure
import pytest
from selenium.common.exceptions import TimeoutException
from time import sleep

from config.environment import config as app_config
from core.agentic.decision_engine import RetryDecision, decide_action
from fixtures.browser_fixture import get_driver

from utils.helpers import take_screenshot
from utils.logger import get_logger


ALLURE_RESULTS_DIR = Path("reports/allure-results")
logger = get_logger()


def _add_agentic_navigation_retry(driver):

    original_get = driver.get
    original_refresh = driver.refresh

    def retry_browser_action(action, label):

        last_exception = None

        for attempt in range(1, 4):

            try:

                return action()

            except TimeoutException as exc:

                last_exception = exc
                decision = decide_action(exc)

                if decision == RetryDecision.FAIL_FAST:
                    raise

                logger.warning(
                    "Agentic browser retry %s/3 for %s after timeout",
                    attempt,
                    label
                )

                try:
                    driver.execute_script("window.stop();")
                except Exception:
                    pass

                if attempt < 3:
                    sleep(2)

        raise last_exception

    def get_with_retry(url):

        return retry_browser_action(
            lambda: original_get(url),
            f"driver.get({url})"
        )

    def refresh_with_retry():

        return retry_browser_action(
            original_refresh,
            "driver.refresh()"
        )

    driver.get = get_with_retry
    driver.refresh = refresh_with_retry

    return driver


def _write_allure_environment(allure_dir):

    allure_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    environment = {
        "Base URL": app_config.base_url,
        "API URL": app_config.api_url,
        "Browser": app_config.browser,
        "Execution": app_config.execution,
        "Grid URL": app_config.grid_url if app_config.execution.lower() == "remote" else "N/A",
        "Python": platform.python_version(),
        "OS": platform.platform(),
    }

    env_lines = [
        f"{key}={value}"
        for key, value in environment.items()
    ]

    (allure_dir / "environment.properties").write_text(
        "\n".join(env_lines),
        encoding="utf-8"
    )

    executor = {
        "name": "pytest",
        "type": "local",
        "buildName": os.getenv("BUILD_NAME", "local-run"),
        "reportName": "Notes Automation Allure Report",
    }

    (allure_dir / "executor.json").write_text(
        json.dumps(executor, indent=2),
        encoding="utf-8"
    )


def pytest_configure(config):

    allure_dir = config.getoption(
        "--alluredir",
        default=None
    )

    _write_allure_environment(
        Path(allure_dir) if allure_dir else ALLURE_RESULTS_DIR
    )


@pytest.fixture(scope="function")
def driver():

    driver = get_driver()
    driver = _add_agentic_navigation_retry(driver)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)

def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            screenshot_path = take_screenshot(
                driver,
                item.name
            )

            allure.attach.file(
                screenshot_path,
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )
