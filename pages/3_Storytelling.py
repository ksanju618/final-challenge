import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services import db, recommender, places_service, genai_service
from utils.guard import get_user
from utils.previews import preview_storytelling
from utils.ui import render_banner, render_login_overlay, render_preview_notice
from utils.validators import clean_destination_input

db.init_db()

render_banner(compact=True)
st.title("📖 Immersive storytelling")

user = get_user()
if not user:
    render_preview_notice("Storytelling")
    preview_storytelling()
    render_login_overlay()
    st.stop()

profile = db.get_profile(user["id"])

if not profile or not profile.get("onboarded"):
    st.warning("Please complete Onboarding first so your story can be personalized.")
    st.stop()

destination = st.text_input("Which destination should we tell a story about?", placeholder="e.g. Varanasi, Rome")

if st.button("Generate story", type="primary"):
    try:
        clean_dest = clean_destination_input(destination)
        with st.spinner("Weaving a story from verified local landmarks..."):
            result = recommender.get_story(user["id"], clean_dest, profile)

        st.subheader(f"📍 {result['resolved_name']}")
        st.markdown(result["story"])

    except ValueError as e:
        st.error(str(e))
    except places_service.PlacesServiceError as e:
        st.error(f"Couldn't fetch real destination data: {e}")
    except genai_service.GenAIError as e:
        st.error(f"GenAI generation failed: {e}")
