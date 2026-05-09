import pytest
import os

from dotenv import load_dotenv

from config.environment import config

from pages.login_page import LoginPage

from pages.notes_page import NotesPage


load_dotenv()


@pytest.mark.ui
def test_create_note_without_title(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    login_page.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    notes_page = NotesPage(driver)

    notes_page.click_add_note()

    notes_page.send_keys(
        notes_page.DESCRIPTION_INPUT,
        "Validation test"
    )

    notes_page.safe_click(
        notes_page.SAVE_BUTTON
    )

    page_text = driver.page_source.lower()

    assert (
        "title" in page_text
        or
        "required" in page_text
    )

@pytest.mark.ui
def test_create_note_without_category(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    login_page.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    notes_page = NotesPage(driver)

    notes_page.click_add_note()

    notes_page.send_keys(
        notes_page.TITLE_INPUT,
        "Category Validation"
    )

    notes_page.send_keys(
        notes_page.DESCRIPTION_INPUT,
        "Missing category validation"
    )

    notes_page.safe_click(
        notes_page.SAVE_BUTTON
    )

    page_text = driver.page_source.lower()

    assert (
        "category" in page_text
        or
        "required" in page_text
    )
