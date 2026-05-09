"""Basic Longcat API client."""

import os

import requests
from dotenv import load_dotenv

from utils.logger import get_logger


load_dotenv()
logger = get_logger()


class LongcatClient:
    """Simple client for asking Longcat a question."""

    def __init__(self) -> None:
        self.api_key = os.getenv("LONGCAT_API_KEY")
        self.base_url = os.getenv("LONGCAT_BASE_URL", "").rstrip("/")
        self.model = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")

    def ask_longcat(self, prompt: str) -> str:
        """Send a prompt to Longcat and return the answer text."""

        if not self.api_key:
            raise ValueError("LONGCAT_API_KEY is missing in .env")

        if not self.base_url:
            raise ValueError("LONGCAT_BASE_URL is missing in .env")

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        logger.info("Sending request to Longcat")

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        logger.info("Longcat response received")
        return answer
