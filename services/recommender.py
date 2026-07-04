"""
Orchestration layer: ties together real-data retrieval (places_service),
GenAI synthesis (genai_service), and persistence (db) for each feature.

Kept separate from the Streamlit pages so it can be unit-tested without
spinning up any UI, and so the retrieval-then-generate pattern is defined
in exactly one place.
"""

import json

from typing import Any
from services import places_service, genai_service, db


def get_personalized_attractions(user_id: int, destination: str, profile: dict[str, Any]) -> dict[str, Any]:
    grounded = places_service.get_destination_places(destination)
    past_destinations = db.get_past_destinations(user_id)

    result = genai_service.rank_and_personalize(
        destination=grounded["resolved_name"],
        places=grounded["places"],
        profile=profile,
        past_destinations=past_destinations,
    )
    result["resolved_name"] = grounded["resolved_name"]
    result["source_place_count"] = len(grounded["places"])

    db.log_search(
        user_id=user_id,
        destination=grounded["resolved_name"],
        query_type="attractions",
        raw_response=json.dumps(result),
    )
    return result


def get_story(user_id: int, destination: str, profile: dict[str, Any]) -> dict[str, Any]:
    grounded = places_service.get_destination_places(destination)
    story = genai_service.generate_story(
        destination=grounded["resolved_name"], places=grounded["places"], profile=profile
    )

    db.log_search(
        user_id=user_id, destination=grounded["resolved_name"], query_type="story", raw_response=story
    )
    return {"resolved_name": grounded["resolved_name"], "story": story}


def get_culture_and_events(user_id: int, destination: str, profile: dict[str, Any]) -> dict[str, Any]:
    grounded = places_service.get_destination_places(destination)
    suggestions = genai_service.suggest_events_and_culture(
        destination=grounded["resolved_name"], places=grounded["places"], profile=profile
    )

    db.log_search(
        user_id=user_id,
        destination=grounded["resolved_name"],
        query_type="events",
        raw_response=suggestions,
    )
    return {"resolved_name": grounded["resolved_name"], "suggestions": suggestions}
