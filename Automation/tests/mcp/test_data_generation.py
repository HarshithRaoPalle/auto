import os

import pytest
from dotenv import load_dotenv

from config.environment import config
from core.mcp.data_generation import TestDataGenerator
from pages.login_page import LoginPage
from pages.notes_page import NotesPage


load_dotenv()


@pytest.mark.ui
def test_generate_note_data(driver) -> None:
    if not os.getenv("LONGCAT_API_KEY") or not os.getenv("LONGCAT_BASE_URL"):
        pytest.skip("Longcat environment variables are required")

    notes = TestDataGenerator().generate_note_data()
    note = notes[0]

    assert len(notes) == 5
    assert note["category"]
    assert note["title"]
    assert note["description"]

    driver.get(f"{config.base_url}/login")

    login_page = LoginPage(driver)
    login_page.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    notes_page = NotesPage(driver)
    notes_page.create_note(
        title=note["title"],
        description=note["description"],
        category=note["category"],
        completed=True
    )

    assert notes_page.is_note_created(note["title"])

