"""Preview content shown to guests before login."""

import streamlit as st


def preview_onboarding():
    st.markdown("#### Your travel profile (preview)")
    st.multiselect(
        "What are you interested in?",
        ["Heritage & history", "Food & culinary culture", "Local festivals & events", "Trekking & mountaineering"],
        default=["Heritage & history", "Food & culinary culture"],
        disabled=True,
    )
    st.select_slider("Your travel experience level", options=["Beginner", "Intermediate", "Expert"], value="Intermediate", disabled=True)
    st.radio("Preferred travel style", ["Solo", "Budget", "Family", "Luxury", "Adventure"], index=2, horizontal=True, disabled=True)
    st.button("Save preferences", use_container_width=True, disabled=True)


def preview_discover():
    st.text_input("Where are you headed?", value="Jaipur, Rajasthan", disabled=True)
    st.button("Get personalized recommendations", type="primary", disabled=True)
    st.subheader("📍 Jaipur")
    st.caption("Personalized from 24 verified real-world locations.")
    st.write("A pink-city adventure blending Mughal architecture, bustling bazaars, and royal Rajasthani cuisine — tailored to your love of heritage and food.")
    st.markdown("### Top attractions for you")
    for name, reason in [
        ("Amber Fort", "A UNESCO-worthy hilltop fortress — perfect for your heritage interest."),
        ("Hawa Mahal", "The iconic Palace of Winds — a photographer's dream at sunrise."),
        ("City Palace", "Living royal residence with museums spanning centuries of Rajput history."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{name}**")
            st.write(reason)
    st.markdown("### Hidden gems")
    with st.container(border=True):
        st.markdown("💎 **Galtaji Temple (Monkey Temple)**")
        st.write("A serene hillside temple complex few tourists schedule — ideal for spiritual explorers.")


def preview_storytelling():
    st.text_input("Which destination should we tell a story about?", value="Varanasi, Uttar Pradesh", disabled=True)
    st.button("Generate story", type="primary", disabled=True)
    st.subheader("📍 Varanasi")
    st.markdown(
        """
        *The first light touches the ghats of Varanasi as the city exhales a breath older than memory.
        Boatmen push their wooden vessels into the Ganga, their oars cutting through water that has
        witnessed a thousand civilizations rise and dissolve...*

        You walk past the Kashi Vishwanath corridor, where pilgrims murmur prayers that have echoed
        unchanged for millennia. The air carries sandalwood, marigold garlands, and the distant
        rhythm of tabla from a lane-side tea stall...

        *(Sign in to generate a full personalized story for any destination.)*
        """
    )


def preview_events_culture():
    st.text_input("Where would you like cultural suggestions for?", value="Kerala", disabled=True)
    st.button("Get cultural suggestions", type="primary", disabled=True)
    st.subheader("📍 Kerala")
    st.markdown(
        """
        **Onam Sadhya** — Experience the grand vegetarian feast served on banana leaves during Kerala's
        harvest festival; each of the 20+ dishes tells a story of the land.

        **Kathakali Performance** — Witness this elaborate classical dance-drama in Kochi or Thrissur;
        arrive early to watch the intricate makeup ritual.

        **Spice Plantation Walk** — Guided tours through Munnar or Thekkady plantations reveal how
        cardamom, pepper & vanilla shaped Kerala's trading history.

        **Vallam Kali (Snake Boat Race)** — If visiting during August–September, the backwater races
        are a thunderous community spectacle unlike anywhere on earth.
        """
    )
    st.caption("Live event dates should be cross-checked with local tourism boards.")


def preview_history():
    st.caption("Past searches personalize your future recommendations.")
    samples = [
        ("Jaipur", "discover", "2025-06-12 14:30"),
        ("Varanasi", "storytelling", "2025-06-10 09:15"),
        ("Kerala", "culture_events", "2025-06-08 18:45"),
    ]
    for dest, qtype, when in samples:
        with st.container(border=True):
            st.markdown(f"**{dest}** · `{qtype}` · {when}")
            with st.expander("View saved response"):
                st.write("(Your AI-generated response will appear here after you search.)")
