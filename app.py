import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services import db  # noqa: E402
from utils.ui import APP_ICON, APP_NAME, init_app_shell

st.set_page_config(
    page_title=f"{APP_NAME}",
    page_icon=APP_ICON,
    layout="wide",
)

if "user" not in st.session_state:
    st.session_state.user = None

db.init_db()
init_app_shell()

pg = st.navigation(
    [
        st.Page("views/home.py", title="Home Page", default=True),
        st.Page("pages/1_Onboarding.py", title="Onboarding"),
        st.Page("pages/2_Discover.py", title="Discover"),
        st.Page("pages/3_Storytelling.py", title="Storytelling"),
        st.Page("pages/4_Events_Culture.py", title="Events & Culture"),
        st.Page("pages/5_History.py", title="History"),
    ]
)
pg.run()
