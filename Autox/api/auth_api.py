import requests

from utils.logger import get_logger

from config.environment import config


logger = get_logger()


class AuthAPI:

    def __init__(self):

        self.base_url = config.api_url

    def login(self, email, password):

        logger.info("Calling login API")

        endpoint = f"{self.base_url}/users/login"

        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(
            endpoint,
            json=payload
        )

        logger.info(
            f"Response Status: {response.status_code}"
        )

        return response