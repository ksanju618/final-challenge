import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from services import db, recommender, places_service, genai_service

FAKE_GROUNDED = {
    "resolved_name": "Jaipur",
    "places": [
        {"name": "Amber Fort", "kinds": "historic", "rating": 3, "lat": 26.98, "lon": 75.85,
         "description": "A hilltop fort blending Rajput and Mughal architecture."},
        {"name": "Nahargarh Stepwell", "kinds": "architecture", "rating": 1, "lat": 26.9, "lon": 75.8,
         "description": "A lesser-visited stepwell with intricate carvings."},
    ],
}


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    return db


@pytest.fixture
def profile():
    return {"interests": ["Heritage & history"], "experience_level": "Intermediate", "travel_style": "Solo"}


def test_get_personalized_attractions_grounds_and_logs(temp_db, profile, monkeypatch):
    user_id = temp_db.create_user("testuser", "hash")

    monkeypatch.setattr(places_service, "get_destination_places", lambda destination, **kw: FAKE_GROUNDED)
    monkeypatch.setattr(
        genai_service,
        "rank_and_personalize",
        lambda destination, places, profile, past_destinations: {
            "top_attractions": [{"name": "Amber Fort", "reason": "Matches heritage interest"}],
            "hidden_gems": [{"name": "Nahargarh Stepwell", "reason": "Low-traffic but rich history"}],
            "why": "Chosen for heritage focus.",
        },
    )

    result = recommender.get_personalized_attractions(user_id, "Jaipur", profile)

    assert result["resolved_name"] == "Jaipur"
    assert result["top_attractions"][0]["name"] == "Amber Fort"

    history = temp_db.get_history(user_id)
    assert len(history) == 1
    assert history[0]["query_type"] == "attractions"


def test_recommender_only_uses_names_from_grounded_places(temp_db, profile, monkeypatch):
    """Regression guard: the GenAI mock output must reference only grounded place names -
    this test documents the contract, real prompt-level enforcement lives in genai_service."""
    user_id = temp_db.create_user("testuser2", "hash")
    monkeypatch.setattr(places_service, "get_destination_places", lambda destination, **kw: FAKE_GROUNDED)
    monkeypatch.setattr(
        genai_service,
        "rank_and_personalize",
        lambda destination, places, profile, past_destinations: {
            "top_attractions": [{"name": p["name"], "reason": "test"} for p in places],
            "hidden_gems": [],
            "why": "test",
        },
    )

    result = recommender.get_personalized_attractions(user_id, "Jaipur", profile)
    grounded_names = {p["name"] for p in FAKE_GROUNDED["places"]}
    returned_names = {a["name"] for a in result["top_attractions"]}
    assert returned_names.issubset(grounded_names)


def test_get_story_logs_history(temp_db, profile, monkeypatch):
    user_id = temp_db.create_user("testuser3", "hash")
    monkeypatch.setattr(places_service, "get_destination_places", lambda destination, **kw: FAKE_GROUNDED)
    monkeypatch.setattr(genai_service, "generate_story", lambda destination, places, profile: "A short grounded story.")

    result = recommender.get_story(user_id, "Jaipur", profile)
    assert result["story"] == "A short grounded story."

    history = temp_db.get_history(user_id)
    assert history[0]["query_type"] == "story"
