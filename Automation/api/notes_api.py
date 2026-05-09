import requests

from utils.logger import get_logger

from config.environment import config


logger = get_logger()


class NotesAPI:

    def __init__(self, token):

        self.base_url = config.api_url

        self.headers = {
            "x-auth-token": token
        }

    def get_notes(self):

        logger.info("Fetching notes via API")

        endpoint = f"{self.base_url}/notes"

        response = requests.get(
            endpoint,
            headers=self.headers
        )

        return response

    def create_note(
        self,
        title,
        description,
        category="Home"
    ):

        logger.info(
            f"Creating note via API: {title}"
        )

        endpoint = f"{self.base_url}/notes"

        payload = {
            "title": title,
            "description": description,
            "category": category
        }

        response = requests.post(
            endpoint,
            json=payload,
            headers=self.headers
        )

        return response

    def delete_note(self, note_id):

        logger.info(
            f"Deleting note via API: {note_id}"
        )

        endpoint = (
            f"{self.base_url}/notes/{note_id}"
        )

        response = requests.delete(
            endpoint,
            headers=self.headers
        )

        return response