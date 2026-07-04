"""
Scripted end-to-end test: signup -> login -> onboarding -> discover -> story ->
events -> history, all through the real service layer (DB is real/temp,
external network calls to Gemini/OpenTripMap are mocked so this test is
fast, free, and runs in CI without API keys).

Before every submission, ALSO run the full flow manually against the real
APIs from the Streamlit UI (see README "Manual E2E Checklist").
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from services import db, auth, recommender, places_service, genai_service

FAKE_GROUNDED = {
    "resolved_name": "Kyoto",
    "places": [
        {"name": "Fushimi Inari Shrine", "kinds": "religion", "rating": 3, "lat": 34.9, "lon": 135.7,
         "description": "Famous shrine known for its thousands of vermilion torii gates."},
        {"name": "Nishiki Market", "kinds": "market", "rating": 2, "lat": 35.0, "lon": 135.7,
         "description": "Narrow shopping street known as Kyoto's kitchen."},
    ],
}


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "e2e_test.db"))
    db.init_db()
    return db


def test_full_user_journey(temp_db, monkeypatch):
    # 1. Signup
    user_id = auth.signup("journey_user", "JourneyPass123")

    # 2. Login
    user = auth.login("journey_user", "JourneyPass123")
    assert user["id"] == user_id

    # 3. Onboarding
    temp_db.save_profile(user_id, ["Art & museums", "Food & culinary culture"], "Beginner", "Solo")
    profile = temp_db.get_profile(user_id)
    assert profile["onboarded"] == 1

    # Mock external calls (real network disabled in this environment / CI)
    monkeypatch.setattr(places_service, "get_destination_places", lambda destination, **kw: FAKE_GROUNDED)
    monkeypatch.setattr(
        genai_service,
        "rank_and_personalize",
        lambda destination, places, profile, past_destinations: {
            "top_attractions": [{"name": "Fushimi Inari Shrine", "reason": "Iconic cultural site"}],
            "hidden_gems": [{"name": "Nishiki Market", "reason": "Local food culture"}],
            "why": "Matched to art/food interests.",
        },
    )
    monkeypatch.setattr(genai_service, "generate_story", lambda destination, places, profile: "A grounded Kyoto story.")
    monkeypatch.setattr(
        genai_service,
        "suggest_events_and_culture",
        lambda destination, places, profile: "- Visit during a local food festival season.",
    )

    # 4. Discover
    attractions = recommender.get_personalized_attractions(user_id, "Kyoto", profile)
    assert attractions["resolved_name"] == "Kyoto"

    # 5. Storytelling
    story = recommender.get_story(user_id, "Kyoto", profile)
    assert "Kyoto" in story["resolved_name"]

    # 6. Events & culture
    events = recommender.get_culture_and_events(user_id, "Kyoto", profile)
    assert "festival" in events["suggestions"].lower()

    # 7. History reflects all three interactions
    history = temp_db.get_history(user_id)
    query_types = {h["query_type"] for h in history}
    assert query_types == {"attractions", "story", "events"}
    assert len(history) == 3
