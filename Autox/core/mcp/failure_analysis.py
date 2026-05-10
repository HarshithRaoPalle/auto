"""Basic Longcat failure analysis."""

from core.mcp.client import LongcatClient


def analyze_failure(expected: str, actual: str) -> str:
    """Ask Longcat for a short reason why a test failed."""

    prompt = f"""
Explain this Selenium test failure in 1 short sentence.

Expected title to contain: {expected}
Actual title: {actual}

Return only the reason. No markdown. No bullet points.
""".strip()

    return LongcatClient().ask_longcat(prompt).strip()
