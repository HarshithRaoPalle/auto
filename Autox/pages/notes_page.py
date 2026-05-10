from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

from utils.logger import get_logger


logger = get_logger()


class NotesPage(BasePage):

    # =========================
    # LOCATORS
    # =========================

    ADD_NOTE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='add-new-note']"
    )

    TITLE_INPUT = (
        By.ID,
        "title"
    )

    DESCRIPTION_INPUT = (
        By.ID,
        "description"
    )
    CATEGORY_DROPDOWN = (
        By.CSS_SELECTOR,
        "[data-testid='note-category']"
    )

    COMPLETED_CHECKBOX = (
        By.CSS_SELECTOR,
        "input[type='checkbox']"
    )

    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='note-submit']"
    )

    NOTES_CONTAINER = (
        By.CSS_SELECTOR,
        "[data-testid='note-card']"
    )

    LOADING_SPINNER = (
        By.CSS_SELECTOR,
        ".spinner-border"
    )

    DELETE_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='note-delete']"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-testid='alert-message']"
    )
    CONFIRM_DELETE = (
        By.CSS_SELECTOR,
        "[data-testid='note-delete-confirm']"
    )
    

    # =========================
    # METHODS
    # =========================

    def click_add_note(self):

        logger.info("Clicking add note")

        self.click(self.ADD_NOTE_BUTTON)

    def create_note(
        self,
        title,
        description,
        category="Home",
        completed=False
    ):

        logger.info(f"Creating note: {title}")

        self.click_add_note()

        # select category
        dropdown = Select(
            self.wait_for_visibility(
                self.CATEGORY_DROPDOWN
            )
        )

        dropdown.select_by_visible_text(category)

        # completed checkbox
        if completed:

            checkbox = self.wait_for_clickable(
                self.COMPLETED_CHECKBOX
            )

            if not checkbox.is_selected():

                checkbox.click()

        self.send_keys(self.TITLE_INPUT, title)

        self.send_keys(
            self.DESCRIPTION_INPUT,
            description
        )

        self.click(self.SAVE_BUTTON)
        self.retry_action(
            lambda: self.wait_for_visibility(
                self.ADD_NOTE_BUTTON
            ),
            locator=self.ADD_NOTE_BUTTON
        )

    def is_note_created(self, title):

        logger.info(
            f"Checking note existence: {title}"
        )

        try:

            self.retry_action(
                lambda: self.wait.until(
                    lambda driver:
                    EC.invisibility_of_element_located(
                        self.LOADING_SPINNER
                    )(driver)
                    and
                    title.lower()
                    in driver.page_source.lower()
                ),
                locator=self.NOTES_CONTAINER
            )

            return True

        except TimeoutException:

            return False

    def is_note_deleted(self, title):

        logger.info(
            f"Checking note deletion: {title}"
        )

        try:

            self.retry_action(
                lambda: self.wait.until(
                    lambda driver:
                    EC.invisibility_of_element_located(
                        self.LOADING_SPINNER
                    )(driver)
                    and
                    title.lower()
                    not in driver.page_source.lower()
                ),
                locator=self.NOTES_CONTAINER
            )

            return True

        except TimeoutException:

            return False

    def delete_first_note(self):

        logger.info("Deleting first note")

        before_count = self.get_notes_count()

        self.safe_click(self.DELETE_BUTTON)

        self.safe_click(self.CONFIRM_DELETE)

        self.retry_action(
            lambda: self.wait.until(
                lambda driver:
                self.get_notes_count() < before_count
            ),
            locator=self.NOTES_CONTAINER
        )

    def get_success_message(self):

        logger.info("Fetching success message")

        element = self.wait_for_visibility(
            self.SUCCESS_MESSAGE
        )

        return element.text
    def get_notes_count(self):

        self.retry_action(
            lambda: self.wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='note-card']"
                    )
                )
            ),
            locator=self.NOTES_CONTAINER
        )

        notes = self.driver.find_elements(
            By.CSS_SELECTOR,
            "[data-testid='note-card']"
        )

        return len(notes)
