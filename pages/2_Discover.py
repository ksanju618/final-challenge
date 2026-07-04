import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services import db, recommender, places_service, genai_service
from utils.guard import get_user
from utils.previews import preview_discover
from utils.ui import render_banner, render_login_overlay, render_preview_notice
from utils.validators import clean_destination_input

db.init_db()

render_banner(compact=True)
st.title("🔍 Discover a destination")

user = get_user()
if not user:
    render_preview_notice("Discover")
    preview_discover()
    render_login_overlay()
    st.stop()

profile = db.get_profile(user["id"])

if not profile or not profile.get("onboarded"):
    st.warning("Please complete Onboarding first so recommendations can be personalized.")
    st.stop()

destination = st.text_input("Where are you headed?", placeholder="e.g. Jaipur, Kyoto, Lisbon")

if st.button("Get personalized recommendations", type="primary"):
    try:
        clean_dest = clean_destination_input(destination)
        with st.spinner("Fetching verified attraction data and personalizing with Gemini..."):
            result = recommender.get_personalized_attractions(user["id"], clean_dest, profile)

        st.subheader(f"📍 {result['resolved_name']}")
        st.caption(f"Personalized from {result['source_place_count']} verified real-world locations.")
        st.write(result.get("why", ""))

        st.markdown("### Top attractions for you")
        for a in result.get("top_attractions", []):
            with st.container(border=True):
                st.markdown(f"**{a['name']}**")
                st.write(a.get("reason", ""))

        st.markdown("### Hidden gems")
        for g in result.get("hidden_gems", []):
            with st.container(border=True):
                st.markdown(f"💎 **{g['name']}**")
                st.write(g.get("reason", ""))

    except ValueError as e:
        st.error(str(e))
    except places_service.PlacesServiceError as e:
        st.error(f"Couldn't fetch real destination data: {e}")
    except genai_service.GenAIError as e:
        st.error(f"GenAI generation failed: {e}")
