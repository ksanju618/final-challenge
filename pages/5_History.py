import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services import db
from utils.guard import get_user
from utils.previews import preview_history
from utils.ui import render_banner, render_login_overlay, render_preview_notice

db.init_db()

render_banner(compact=True)
st.title("🕰️ Your search history")
st.caption("Past searches are stored and used to personalize future recommendations.")

user = get_user()
if not user:
    render_preview_notice("History")
    preview_history()
    render_login_overlay()
    st.stop()

history = db.get_history(user["id"], limit=30)

if not history:
    st.info("No searches yet — try the Discover, Storytelling, or Events & Culture pages.")
else:
    for item in history:
        with st.container(border=True):
            st.markdown(f"**{item['destination']}** · `{item['query_type']}` · {item['created_at'][:19].replace('T', ' ')}")
            with st.expander("View saved response"):
                st.write(item["raw_response"])
