"""
GenAI synthesis layer (Google Gemini).

Design rule enforced throughout this file: Gemini is ALWAYS given the real,
retrieved place data from `places_service.py` as context, and is explicitly
instructed to only reference venues that appear in that data. Its job is
personalization, ranking, and narrative - not invention of facts.
"""

import os
import json
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.0-flash"

_client = None


class GenAIError(Exception):
    """Raised when the Gemini API call fails or returns an unusable response."""
    pass


def _get_client():
    global _client
    if not GEMINI_API_KEY:
        raise GenAIError("GEMINI_API_KEY is not configured.")
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def _places_context(places: list) -> str:
    """Serializes retrieved real places into compact text for the prompt."""
    lines = []
    for p in places:
        desc = (p.get("description") or "")[:280]
        lines.append(f"- {p['name']} | categories: {p.get('kinds', 'n/a')} | rating: {p.get('rating', 0)} | {desc}")
    return "\n".join(lines)


GROUNDING_RULE = (
    "You must ONLY reference attraction or venue names that appear in the VERIFIED PLACES list below. "
    "Do not invent names of places, events, restaurants, or facts that are not supported by this list. "
    "If you want to suggest a general type of activity not tied to a specific verified venue, "
    "clearly say it is a general suggestion, not a named place."
)


def rank_and_personalize(destination: str, places: list, profile: dict, past_destinations: list) -> dict:
    """
    Returns structured JSON: {top_attractions: [...], hidden_gems: [...], why: str}
    top_attractions/hidden_gems reference only names from `places`.
    """
    client = _get_client()
    interests = ", ".join(profile.get("interests", [])) or "general sightseeing"
    experience = profile.get("experience_level") or "not specified"
    style = profile.get("travel_style") or "not specified"
    past = ", ".join(past_destinations) if past_destinations else "none yet"

    prompt = f"""
{GROUNDING_RULE}

VERIFIED PLACES in {destination}:
{_places_context(places)}

TRAVELER PROFILE:
- Interests: {interests}
- Experience level: {experience}
- Travel style: {style}
- Previously explored destinations on this platform: {past}

TASK:
1. Select up to 6 "top_attractions" from the VERIFIED PLACES list that best match this traveler's interests and experience level.
2. Select up to 4 "hidden_gems" - verified places from the list that are lower-rated/less mainstream but culturally rich, matching their interests.
3. Write a short "why" (2-3 sentences) explaining the personalization logic in plain language.

Respond ONLY as JSON with this exact shape:
{{"top_attractions": [{{"name": "", "reason": ""}}], "hidden_gems": [{{"name": "", "reason": ""}}], "why": ""}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.4),
    )

    try:
        return json.loads(response.text)
    except (json.JSONDecodeError, AttributeError) as e:
        raise GenAIError(f"Gemini returned an unparseable response: {e}")


def generate_story(destination: str, places: list, profile: dict) -> str:
    """Returns immersive narrative text grounded in the verified places."""
    client = _get_client()
    interests = ", ".join(profile.get("interests", [])) or "general sightseeing"

    prompt = f"""
{GROUNDING_RULE}

VERIFIED PLACES in {destination}:
{_places_context(places)}

TASK: Write an immersive, sensory, 250-350 word travel narrative that weaves together 3-5 of the
verified places above into a walkable story of a day exploring {destination}'s culture and heritage,
tailored to someone interested in: {interests}. Use second person ("you"). Ground every named
location in the list above - do not invent venue names.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7),
    )
    if not response.text:
        raise GenAIError("Gemini returned an empty story response.")
    return response.text


def suggest_events_and_culture(destination: str, places: list, profile: dict) -> str:
    """Returns cultural experience / local-event style suggestions, clearly framed as general ideas
    when not tied to a specific verified venue."""
    client = _get_client()
    interests = ", ".join(profile.get("interests", [])) or "general sightseeing"

    prompt = f"""
{GROUNDING_RULE}

VERIFIED PLACES in {destination}:
{_places_context(places)}

TASK: Suggest 4-6 ways this traveler (interested in: {interests}) could engage with local culture
and heritage in {destination} - e.g. types of festivals/seasonal events typically associated with
the region, cultural etiquette tips, or heritage-focused activities near the verified places above.
Clearly label anything that is a general cultural pattern rather than a specific dated event, since
you cannot verify live event calendars. Format as a short markdown bulleted list, each bullet 1-2 sentences.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.6),
    )
    if not response.text:
        raise GenAIError("Gemini returned an empty cultural suggestions response.")
    return response.text
