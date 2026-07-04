"""
Real-world data grounding layer.

This is the anti-hallucination backbone of the app: every attraction name,
coordinate, and category shown to the user (and fed to the GenAI layer)
originates here, from OpenTripMap's real dataset, not from the language
model. Gemini is only ever allowed to *synthesize and narrate* this data,
never invent new venues.
"""

import os
import requests
from functools import lru_cache
from typing import Any, Optional

OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY", "")
OPENTRIPMAP_BASE = "https://api.opentripmap.com/0.1/en/places"
WIKIPEDIA_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

REQUEST_TIMEOUT = 10  # seconds


class PlacesServiceError(Exception):
    """Raised when the upstream places API cannot be reached or returns bad data."""
    pass


@lru_cache(maxsize=64)
def _geocode(destination: str) -> tuple[float, float, str]:
    """Resolves a free-text destination name to lat/lon using OpenTripMap's geoname endpoint."""
    try:
        resp = requests.get(
            f"{OPENTRIPMAP_BASE}/geoname",
            params={"name": destination, "apikey": OPENTRIPMAP_API_KEY},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        raise PlacesServiceError(f"Geocoding network request failed for '{destination}': {e}") from e

    if resp.status_code != 200:
        raise PlacesServiceError(f"Could not geocode '{destination}' (status {resp.status_code}).")
    data = resp.json()
    if "lat" not in data or "lon" not in data:
        raise PlacesServiceError(f"'{destination}' was not recognized as a real location.")
    return float(data["lat"]), float(data["lon"]), str(data.get("name", destination))


def _fetch_place_detail(xid: str) -> Optional[dict[str, Any]]:
    try:
        resp = requests.get(
            f"{OPENTRIPMAP_BASE}/xid/{xid}",
            params={"apikey": OPENTRIPMAP_API_KEY},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    return resp.json()


@lru_cache(maxsize=64)
def _wikipedia_summary(title: str) -> Optional[str]:
    try:
        resp = requests.get(WIKIPEDIA_SUMMARY_URL.format(title=title), timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            return resp.json().get("extract")
    except requests.RequestException:
        pass
    return None


def get_destination_places(destination: str, radius_m: int = 12000, limit: int = 20) -> dict[str, Any]:
    """
    Returns a list of real, verifiable places near `destination`.

    Each item: {name, kinds, rating, lat, lon, description}
    Raises PlacesServiceError if the destination cannot be geocoded or the
    API key is missing/invalid - callers should surface this to the user
    rather than silently falling back to invented data.
    """
    if not OPENTRIPMAP_API_KEY:
        raise PlacesServiceError("OPENTRIPMAP_API_KEY is not configured.")

    lat, lon, resolved_name = _geocode(destination)

    try:
        resp = requests.get(
            f"{OPENTRIPMAP_BASE}/radius",
            params={
                "radius": radius_m,
                "lon": lon,
                "lat": lat,
                "kinds": "interesting_places,cultural,historic,museums,architecture",
                "rate": 1,
                "format": "json",
                "limit": limit,
                "apikey": OPENTRIPMAP_API_KEY,
            },
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        raise PlacesServiceError(f"Places lookup query failed for '{destination}': {e}") from e

    if resp.status_code != 200:
        raise PlacesServiceError(f"Places lookup failed for '{destination}' (status {resp.status_code}).")

    raw_places = resp.json()
    places = []
    for p in raw_places:
        if not p.get("name"):
            continue  # skip unnamed points - not useful and not verifiable to the user
        detail = _fetch_place_detail(p["xid"]) or {}
        description = None
        wiki_extract = (detail.get("wikipedia_extracts") or {}).get("text")
        if wiki_extract:
            description = wiki_extract
        else:
            description = _wikipedia_summary(p["name"].replace(" ", "_"))

        places.append(
            {
                "name": p["name"],
                "kinds": p.get("kinds", ""),
                "rating": p.get("rate", 0),
                "lat": p.get("point", {}).get("lat"),
                "lon": p.get("point", {}).get("lon"),
                "description": description or "No verified description available for this location.",
            }
        )

    if not places:
        raise PlacesServiceError(
            f"No verified attractions found for '{destination}'. Try a nearby larger city or check spelling."
        )

    return {"resolved_name": resolved_name, "places": places}
