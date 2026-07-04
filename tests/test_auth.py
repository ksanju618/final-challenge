import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from services import db, auth


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    return db


def test_signup_success(temp_db):
    user_id = auth.signup("newuser1", "StrongPass123")
    assert isinstance(user_id, int)


def test_signup_duplicate_username_rejected(temp_db):
    auth.signup("dupuser", "StrongPass123")
    with pytest.raises(auth.AuthError):
        auth.signup("dupuser", "AnotherPass456")


def test_signup_rejects_short_password(temp_db):
    with pytest.raises(auth.AuthError):
        auth.signup("shortpassuser", "short")


def test_signup_rejects_invalid_username(temp_db):
    with pytest.raises(auth.AuthError):
        auth.signup("a b!", "StrongPass123")


def test_login_success_with_correct_password(temp_db):
    auth.signup("loginuser", "CorrectPass123")
    user = auth.login("loginuser", "CorrectPass123")
    assert user["username"] == "loginuser"


def test_login_fails_with_wrong_password(temp_db):
    auth.signup("loginuser2", "CorrectPass123")
    with pytest.raises(auth.AuthError):
        auth.login("loginuser2", "WrongPassword")


def test_login_fails_for_nonexistent_user(temp_db):
    with pytest.raises(auth.AuthError):
        auth.login("ghostuser", "whatever123")


def test_password_is_hashed_not_stored_plaintext(temp_db):
    auth.signup("hashcheckuser", "PlainTextPass1")
    stored = db.get_user_by_username("hashcheckuser")
    assert stored["password_hash"] != "PlainTextPass1"
    assert stored["password_hash"].startswith("$2b$")
