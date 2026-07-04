import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services import db
from utils.guard import get_user
from utils.previews import preview_onboarding
from utils.ui import render_banner, render_login_overlay, render_preview_notice
from utils.validators import clean_interests

db.init_db()

render_banner(compact=True)
st.title("🧳 Tell us about you")
st.caption("This shapes every recommendation you'll get — done once, editable anytime.")

user = get_user()
if not user:
    render_preview_notice("Onboarding")
    preview_onboarding()
    render_login_overlay()
    st.stop()

profile = db.get_profile(user["id"]) or {}

INTEREST_OPTIONS = [
    "Trekking & mountaineering", "Heritage & history", "Food & culinary culture",
    "Art & museums", "Local festivals & events", "Wildlife & nature",
    "Photography", "Spiritual & religious sites", "Nightlife & music",
    "Architecture", "Off-the-beaten-path / hidden gems",
]

with st.form("onboarding_form"):
    interests = st.multiselect(
        "What are you interested in?", INTEREST_OPTIONS,
        default=profile.get("interests", []),
    )
    experience = st.select_slider(
        "Your travel experience level",
        options=["Beginner", "Intermediate", "Expert"],
        value=profile.get("experience_level") or "Intermediate",
    )
    style = st.radio(
        "Preferred travel style",
        ["Solo", "Budget", "Family", "Luxury", "Adventure"],
        index=(["Solo", "Budget", "Family", "Luxury", "Adventure"].index(profile.get("travel_style"))
               if profile.get("travel_style") in ["Solo", "Budget", "Family", "Luxury", "Adventure"] else 0),
        horizontal=True,
    )
    submitted = st.form_submit_button("Save preferences", use_container_width=True)

    if submitted:
        try:
            cleaned = clean_interests(interests)
            db.save_profile(user["id"], cleaned, experience, style)
            st.success("Preferences saved! Head to the Discover page to see personalized recommendations.")
        except ValueError as e:
            st.error(str(e))
