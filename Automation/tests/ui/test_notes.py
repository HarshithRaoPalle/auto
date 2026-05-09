import pytest
import uuid

import os

from dotenv import load_dotenv

from config.environment import config

from pages.login_page import LoginPage

from pages.notes_page import NotesPage


load_dotenv()


def login(driver):

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)

    login_page.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

@pytest.mark.ui
def test_create_note(driver):

    login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Automation Note {unique_id}"

    description = "Created by Selenium automation"

    notes_page.create_note(
        title,
        description,
        category="Home",
        completed=True
    )

    assert notes_page.is_note_created(title)

@pytest.mark.ui
def test_delete_note(driver):

    login(driver)

    notes_page = NotesPage(driver)

    before_delete = (
        notes_page.get_notes_count()
    )

    notes_page.delete_first_note()

    after_delete = (
        notes_page.get_notes_count()
    )

    assert after_delete < before_delete

@pytest.mark.ui
def test_create_multiple_notes(driver):

    login(driver)

    notes_page = NotesPage(driver)

    titles = []

    for i in range(3):

        unique_id = str(uuid.uuid4())[:8]

        title = f"Multi Note {unique_id}"

        titles.append(title)

        notes_page.create_note(
            title,
            f"Description {i}",
            category="Home"
        )

    for title in titles:

        assert notes_page.is_note_created(title)

@pytest.mark.ui
def test_note_appears_instantly_ui(driver):

    login(driver)

    notes_page = NotesPage(driver)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Instant Note {unique_id}"

    notes_page.create_note(
        title,
        "Realtime UI validation",
        category="Home"
    )

    assert notes_page.is_note_created(title)
