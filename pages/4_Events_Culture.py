import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services import db, recommender, places_service, genai_service
from utils.guard import get_user
from utils.previews import preview_events_culture
from utils.ui import render_banner, render_login_overlay, render_preview_notice
from utils.validators import clean_destination_input

db.init_db()

render_banner(compact=True)
st.title("🎭 Local events & cultural experiences")

user = get_user()
if not user:
    render_preview_notice("Events & Culture")
    preview_events_culture()
    render_login_overlay()
    st.stop()

profile = db.get_profile(user["id"])

if not profile or not profile.get("onboarded"):
    st.warning("Please complete Onboarding first so suggestions can be personalized.")
    st.stop()

destination = st.text_input("Where would you like cultural suggestions for?", placeholder="e.g. Marrakech, Kyoto")

if st.button("Get cultural suggestions", type="primary"):
    try:
        clean_dest = clean_destination_input(destination)
        with st.spinner("Gathering culturally grounded suggestions..."):
            result = recommender.get_culture_and_events(user["id"], clean_dest, profile)

        st.subheader(f"📍 {result['resolved_name']}")
        st.markdown(result["suggestions"])
        st.caption(
            "Note: general cultural patterns and heritage activities are AI-suggested based on verified "
            "location data. For live, dated event calendars, cross-check with local tourism boards."
        )

    except ValueError as e:
        st.error(str(e))
    except places_service.PlacesServiceError as e:
        st.error(f"Couldn't fetch real destination data: {e}")
    except genai_service.GenAIError as e:
        st.error(f"GenAI generation failed: {e}")
