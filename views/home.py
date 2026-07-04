import streamlit as st

from services import db
from utils.ui import (
    APP_ICON,
    APP_NAME,
    FEATURES,
    render_banner,
    render_featured_destinations,
    render_how_it_works,
    render_stats,
)

if "user" not in st.session_state:
    st.session_state.user = None

render_banner()

if st.session_state.user:
    profile = db.get_profile(st.session_state.user["id"])
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## Welcome back, `{st.session_state.user['username']}`!")
        if profile and profile.get("onboarded"):
            interests = ", ".join(profile["interests"][:4])
            st.success(f"Your interests: {interests}. Pick a feature below to continue exploring.")
        else:
            st.info("Complete **Onboarding** to unlock personalized recommendations across India.")
    with col2:
        st.html(
            '<div style="text-align:center;padding:1rem;background:#E8F5E9;border-radius:12px;">'
            '<div style="font-size:2rem">✅</div>'
            '<div style="font-size:0.85rem;color:#2E7D32">You\'re signed in</div></div>'
        )
else:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("## Explore India — before you even pack your bags")
        st.markdown(
            "Browse destinations, features & cultural highlights below. "
            "**Log in at the top right** to unlock personalized AI journeys."
        )
    with col2:
        st.html(
            '<div style="text-align:center;padding:1rem;background:#FFF3E0;border-radius:12px;border:1px dashed #FFB74D;">'
            '<div style="font-size:2rem">🔐</div>'
            '<div style="font-size:0.85rem;color:#E65100">Log in to start your journey</div></div>'
        )

st.divider()
render_stats()

st.markdown("### 🚀 What you can do")
feat_cols = st.columns(len(FEATURES))
for col, feat in zip(feat_cols, FEATURES):
    with col:
        st.html(
            f'<div class="bb-dest-card" style="text-align:center">'
            f'<div style="font-size:2rem">{feat["icon"]}</div>'
            f'<div class="bb-dest-name">{feat["title"]}</div>'
            f'<div class="bb-dest-blurb">{feat["desc"]}</div>'
            f"</div>"
        )
        if st.button(f"Open {feat['title']}", key=f"nav_{feat['title']}", use_container_width=True):
            st.switch_page(feat["page"])

st.divider()
render_featured_destinations()

st.divider()
render_how_it_works()

st.markdown("---")
st.caption(
    f"{APP_ICON} **{APP_NAME}** — Every recommendation is grounded in verified location data. "
    "Gemini personalizes; it never invents place names."
)
