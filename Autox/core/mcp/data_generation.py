"""Basic Longcat test data generation."""

import json
import re

from core.mcp.client import LongcatClient


class TestDataGenerator:
    """Generate test data using Longcat."""

    __test__ = False

    def __init__(self) -> None:
        self.llm = LongcatClient()

    def generate_note_data(self) -> list[dict[str, str]]:
        """Generate note data and return it as a Python list."""

        prompt = """
Generate 5 unique test notes for an API system.

Each note must contain:
- category (Home, Work, Personal)
- title (unique random string)
- description (1-2 sentences)

Return ONLY valid JSON array like:
[
  {
    "category": "...",
    "title": "...",
    "description": "..."
  }
]
""".strip()

        response = self.llm.ask_longcat(prompt)

        try:
            return json.loads(response)
        except Exception:
            match = re.search(r"\[.*\]", response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise Exception(f"Invalid JSON from LLM: {response}")
