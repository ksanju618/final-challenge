import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from services import db


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    return db


def test_create_user_and_fetch(temp_db):
    user_id = temp_db.create_user("alice", "hashed_pw_value")
    fetched = temp_db.get_user_by_username("alice")
    assert fetched is not None
    assert fetched["id"] == user_id
    assert fetched["password_hash"] == "hashed_pw_value"


def test_username_exists(temp_db):
    temp_db.create_user("bob", "hash")
    assert temp_db.username_exists("bob") is True
    assert temp_db.username_exists("nonexistent") is False


def test_profile_defaults_on_signup(temp_db):
    user_id = temp_db.create_user("carol", "hash")
    profile = temp_db.get_profile(user_id)
    assert profile["onboarded"] == 0
    assert profile["interests"] == []


def test_save_and_fetch_profile(temp_db):
    user_id = temp_db.create_user("dave", "hash")
    temp_db.save_profile(user_id, ["Trekking & mountaineering", "Food & culinary culture"], "Expert", "Solo")
    profile = temp_db.get_profile(user_id)
    assert profile["onboarded"] == 1
    assert "Trekking & mountaineering" in profile["interests"]
    assert profile["experience_level"] == "Expert"


def test_search_history_logging_and_order(temp_db):
    user_id = temp_db.create_user("erin", "hash")
    temp_db.log_search(user_id, "Jaipur", "attractions", '{"foo": "bar"}')
    temp_db.log_search(user_id, "Kyoto", "story", "some story text")

    history = temp_db.get_history(user_id)
    assert len(history) == 2
    # most recent first
    assert history[0]["destination"] == "Kyoto"

    past = temp_db.get_past_destinations(user_id)
    assert "Kyoto" in past and "Jaipur" in past
