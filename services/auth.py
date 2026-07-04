"""
Authentication layer.

Passwords are hashed with bcrypt (salted, adaptive cost) before ever
touching the database - the DB never stores or logs a plaintext password.
"""

import re
import bcrypt

from services import db

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


class AuthError(Exception):
    """Raised for any signup/login validation or credential failure."""
    pass


def _validate_username(username: str):
    if not USERNAME_PATTERN.match(username or ""):
        raise AuthError(
            "Username must be 3-20 characters and contain only letters, numbers, or underscores."
        )


def _validate_password(password: str):
    if not password or len(password) < 8:
        raise AuthError("Password must be at least 8 characters long.")


def signup(username: str, password: str) -> int:
    """Creates a new user account. Returns the new user_id. Raises AuthError on invalid input."""
    _validate_username(username)
    _validate_password(password)

    if db.username_exists(username):
        raise AuthError("That username is already taken.")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return db.create_user(username, password_hash)


def login(username: str, password: str) -> dict:
    """Verifies credentials and returns the user record (without password hash) on success."""
    user = db.get_user_by_username(username)
    if not user:
        raise AuthError("Invalid username or password.")

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        raise AuthError("Invalid username or password.")

    return {"id": user["id"], "username": user["username"]}
