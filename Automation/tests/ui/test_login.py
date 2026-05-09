import pytest
import os

from dotenv import load_dotenv

from pages.login_page import LoginPage

from config.environment import config


load_dotenv()

@pytest.mark.ui
def test_valid_login(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    email = os.getenv("EMAIL")

    password = os.getenv("PASSWORD")

    login_page.login(
        email,
        password
    )

    assert login_page.is_login_successful()

@pytest.mark.ui
def test_invalid_login(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    login_page.login(
        "wrong@gmail.com",
        "wrongpassword"
    )

    alerts = driver.find_elements(
        "xpath",
        "//*[contains(text(),'incorrect')]"
    )

    print("ALERT COUNT:", len(alerts))

    for alert in alerts:
        print(alert.text)

    error = login_page.get_error_message()

    assert "incorrect" in error.lower()

