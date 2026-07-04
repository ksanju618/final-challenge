"""Small, dependency-free input validation helpers used by the Streamlit pages."""

import re

DESTINATION_PATTERN = re.compile(r"^[a-zA-Z0-9\s,.'\-]{2,60}$")


def clean_destination_input(raw: str) -> str:
    """Trims and validates a free-text destination field.

    Raises ValueError with a user-facing message if the input looks invalid,
    empty, or suspicious (e.g. contains characters not expected in a place name).
    """
    value = (raw or "").strip()
    if not value:
        raise ValueError("Please enter a destination.")
    if not DESTINATION_PATTERN.match(value):
        raise ValueError("Destination should only contain letters, numbers, spaces, and basic punctuation.")
    return value


def clean_interests(selected: list) -> list:
    if not selected:
        raise ValueError("Please select at least one interest.")
    return [str(i).strip() for i in selected if str(i).strip()]
