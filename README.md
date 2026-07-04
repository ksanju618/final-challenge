# 🧭 Wayfarer — GenAI Destination Discovery & Cultural Experiences

A GenAI-powered Streamlit app that recommends attractions, surfaces hidden gems,
generates immersive travel storytelling, and suggests cultural/heritage
experiences — personalized to each logged-in user's interests, experience
level, and past searches.

Built for the "Destination Discovery & Cultural Experiences" hackathon challenge.

## Why this isn't just "ask an LLM for travel tips"

The brief explicitly bans hallucinated AI responses. Every attraction name,
rating, and coordinate shown to the user comes from **OpenTripMap's real
dataset** (`services/places_service.py`), with Wikipedia as a fallback for
richer descriptions. Gemini is only ever given that verified data as context
and instructed to personalize/narrate it — never to invent venue names. See
`GROUNDING_RULE` in `services/genai_service.py`.

## Architecture

```
app.py                     Login/signup entrypoint + session routing
pages/
  1_Onboarding.py           Capture interests, experience level, travel style
  2_Discover.py             Personalized attractions + hidden gems (Gemini)
  3_Storytelling.py         Immersive narrative generation (Gemini)
  4_Events_Culture.py       Cultural/heritage suggestions (Gemini)
  5_History.py              Past searches, persisted per user
services/
  auth.py                   Signup/login, bcrypt password hashing
  db.py                     SQLite access layer (users, profiles, history)
  places_service.py         Real data grounding (OpenTripMap + Wikipedia)
  genai_service.py          Gemini prompt templates + API calls
  recommender.py            Orchestrates retrieval -> GenAI -> persistence
utils/
  auth guard, input validators
tests/
  test_db.py, test_auth.py, test_recommender.py, test_e2e.py
```

## Setup

```bash
git clone <this-repo-url>
cd travel-genai
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and fill in your real GEMINI_API_KEY and OPENTRIPMAP_API_KEY
streamlit run app.py
```

- Get a **Gemini API key**: https://aistudio.google.com/
- Get a free **OpenTripMap API key**: https://opentripmap.io/product

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. On https://share.streamlit.io, create a new app pointing at `app.py`.
3. In the app's **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   OPENTRIPMAP_API_KEY = "your_key_here"
   ```
4. Deploy.

> **Persistence note:** Streamlit Community Cloud's filesystem is ephemeral —
> the SQLite database persists for the life of a running app instance but
> resets on redeploy or after the app sleeps from inactivity. This is fine for
> live demos/judging within a session. For durable persistence across
> restarts, swap the connection in `services/db.py` for a hosted Postgres
> instance (e.g. Supabase free tier) — the SQL used is close to drop-in
> compatible.

## Test credentials for judges

```
username: demo_traveler
password: DemoPass123
```

If this account doesn't exist yet on a fresh deploy (e.g. after a filesystem
reset), create it once via the "Create account" tab using these exact
credentials, then proceed to log in.

## Running automated tests

```bash
pytest tests/ -v
```

Tests mock the external Gemini/OpenTripMap calls (so they run free and fast
without API keys), but they exercise the **real** auth, database, and
orchestration logic end-to-end.

## Manual E2E checklist (run before every submission)

- [ ] Sign up a fresh test account
- [ ] Log in with it
- [ ] Complete Onboarding with real interest selections
- [ ] Discover page: search a real destination, confirm attractions + hidden
      gems appear and reference real place names
- [ ] Storytelling page: generate a story, confirm it references the same
      real places
- [ ] Events & Culture page: confirm suggestions render and the "general vs.
      verified" caption is visible
- [ ] History page: confirm all above searches appear with timestamps
- [ ] Log out and log back in: confirm profile/history persisted within the
      session
- [ ] Try an invalid/nonsense destination: confirm a graceful error, not a
      crash or fabricated data

## Security notes

- Passwords are bcrypt-hashed (salted, adaptive cost) — never stored or
  logged in plaintext.
- API keys are read from environment variables / Streamlit secrets, never
  hardcoded, and `.env` is gitignored.
- All free-text inputs (destination, credentials) are validated/sanitized
  before use (`utils/validators.py`).

## Accessibility notes

- All interactive controls use Streamlit's native labeled widgets (no
  custom unlabeled components).
- Status/feedback uses both color and text (e.g. `st.error`/`st.success`
  include explicit wording, not color alone).
- Layout uses Streamlit's responsive default container width.
