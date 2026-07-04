"""Shared UI components and styling for Bharat Bhraman."""

from pathlib import Path

import streamlit as st

APP_NAME = "Bharat Bhraman"
APP_TAGLINE = "GenAI-powered discovery of India's heritage, culture & hidden gems"
APP_ICON = "🇮🇳"

BANNER_IMAGE = Path(__file__).resolve().parent.parent / "assets" / "banner.jpg"

FEATURED_DESTINATIONS = [
    {"name": "Jaipur", "tag": "Pink City", "emoji": "🏰", "blurb": "Palaces, bazaars & royal Rajasthani cuisine"},
    {"name": "Varanasi", "tag": "Spiritual", "emoji": "🪔", "blurb": "Ghats, Ganga aarti & timeless devotion"},
    {"name": "Kerala", "tag": "Backwaters", "emoji": "🌴", "blurb": "Houseboats, spice gardens & Ayurveda"},
    {"name": "Ladakh", "tag": "Himalayan", "emoji": "🏔️", "blurb": "Monasteries, passes & starlit skies"},
    {"name": "Hampi", "tag": "Heritage", "emoji": "🛕", "blurb": "Vijayanagara ruins & boulder landscapes"},
    {"name": "Rishikesh", "tag": "Adventure", "emoji": "🧘", "blurb": "Yoga capital, rafting & the Ganges"},
]

FEATURES = [
    {
        "icon": "🧳",
        "title": "Onboarding",
        "desc": "Tell us your interests, travel style & experience level for tailored journeys.",
        "page": "pages/1_Onboarding.py",
    },
    {
        "icon": "🔍",
        "title": "Discover",
        "desc": "Personalized attractions & hidden gems grounded in real-world location data.",
        "page": "pages/2_Discover.py",
    },
    {
        "icon": "📖",
        "title": "Storytelling",
        "desc": "Immersive AI-crafted narratives woven from verified local landmarks.",
        "page": "pages/3_Storytelling.py",
    },
    {
        "icon": "🎭",
        "title": "Events & Culture",
        "desc": "Festivals, heritage walks, culinary trails & cultural experiences.",
        "page": "pages/4_Events_Culture.py",
    },
    {
        "icon": "🕰️",
        "title": "History",
        "desc": "Your past searches — used to refine future recommendations.",
        "page": "pages/5_History.py",
    },
]


def inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600&display=swap');

        .block-container { padding-top: 0.6rem; max-width: 1100px; }

        h1, h2, h3, .bb-title {
            font-family: 'Playfair Display', serif !important;
        }

        .bb-hero {
            position: relative;
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 1.5rem;
            min-height: 220px;
            background: linear-gradient(135deg, #FF9933 0%, #E8751A 35%, #C45A00 70%, #1B5E20 100%);
            box-shadow: 0 12px 40px rgba(232, 117, 26, 0.25);
        }
        .bb-hero-bg {
            position: absolute; inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.35;
        }
        .bb-hero-overlay {
            position: absolute; inset: 0;
            background: linear-gradient(90deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.15) 60%, transparent 100%);
        }
        .bb-hero-content {
            position: relative; z-index: 2;
            padding: 2.5rem 2rem;
            color: white;
        }
        .bb-hero-content h1 {
            font-size: 2.6rem; margin: 0 0 0.4rem 0;
            text-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }
        .bb-hero-content p {
            font-family: 'Poppins', sans-serif;
            font-size: 1.05rem; margin: 0; opacity: 0.95;
            max-width: 520px;
        }
        .bb-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.4);
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.8rem;
            margin-bottom: 0.8rem;
            font-family: 'Poppins', sans-serif;
        }

        .bb-stat-row {
            display: flex; gap: 1rem; flex-wrap: wrap;
            margin: 1.2rem 0 1.8rem 0;
        }
        .bb-stat {
            flex: 1; min-width: 140px;
            background: linear-gradient(145deg, #FFF5E8, #FFE8CC);
            border: 1px solid #FFD9A8;
            border-radius: 14px;
            padding: 1rem 1.2rem;
            text-align: center;
        }
        .bb-stat-num {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem; font-weight: 700;
            color: #C45A00;
        }
        .bb-stat-label {
            font-family: 'Poppins', sans-serif;
            font-size: 0.78rem; color: #6B5344;
            margin-top: 2px;
        }

        .bb-dest-card {
            background: white;
            border: 1px solid #F0DCC8;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            height: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .bb-dest-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(232,117,26,0.15);
        }
        .bb-dest-emoji { font-size: 1.8rem; }
        .bb-dest-name {
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem; font-weight: 700;
            color: #1A1A2E; margin: 0.3rem 0;
        }
        .bb-dest-tag {
            display: inline-block;
            background: #E8F5E9; color: #2E7D32;
            font-size: 0.7rem; padding: 2px 8px;
            border-radius: 10px; font-family: 'Poppins', sans-serif;
        }
        .bb-dest-blurb {
            font-family: 'Poppins', sans-serif;
            font-size: 0.82rem; color: #6B6B6B;
            margin-top: 0.5rem; line-height: 1.4;
        }

        .bb-step {
            background: white;
            border-left: 4px solid #FF9933;
            border-radius: 0 12px 12px 0;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.7rem;
            font-family: 'Poppins', sans-serif;
        }
        .bb-step strong { color: #C45A00; }

        .bb-preview-banner {
            background: linear-gradient(90deg, #FFF3E0, #FFECB3);
            border: 1px dashed #FFB74D;
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 1rem;
            font-family: 'Poppins', sans-serif;
            font-size: 0.9rem;
            color: #5D4037;
        }

        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFF9F3 0%, #FFF0E0 100%);
        }
        section[data-testid="stSidebar"] > div {
            display: flex;
            flex-direction: column;
        }
        section[data-testid="stSidebar"] .bb-sidebar-brand-block {
            order: -1;
        }

        .bb-sidebar-brand {
            font-family: 'Playfair Display', serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #C45A00;
            margin-bottom: 0.2rem;
        }
        .bb-sidebar-tagline {
            font-family: 'Poppins', sans-serif;
            font-size: 0.78rem;
            color: #6B5344;
            line-height: 1.4;
            margin-bottom: 0.5rem;
        }

        div[data-testid="stPopover"] button {
            background: #E8751A !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_branding():
    """App name & tagline at the top of the sidebar, above page navigation."""
    with st.sidebar:
        st.markdown(
            f'<div class="bb-sidebar-brand-block">'
            f'<div class="bb-sidebar-brand">{APP_ICON} {APP_NAME}</div>'
            f'<div class="bb-sidebar-tagline">{APP_TAGLINE}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
        st.divider()


def render_top_auth():
    """Login / signup popover pinned to the top-right of the main area."""
    _, auth_col = st.columns([5, 1.2])
    with auth_col:
        if st.session_state.get("user"):
            st.markdown(
                f'<p style="text-align:right;margin:0 0 4px 0;font-size:0.82rem;color:#6B5344">'
                f'👤 <strong>{st.session_state.user["username"]}</strong></p>',
                unsafe_allow_html=True,
            )
            if st.button("Log out", key="top_logout", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        else:
            with st.popover("Log in", use_container_width=True):
                tab_login, tab_signup = st.tabs(["Log in", "Sign up"])
                with tab_login:
                    with st.form("top_login"):
                        username = st.text_input("Username", key="top_login_user")
                        password = st.text_input("Password", type="password", key="top_login_pass")
                        if st.form_submit_button("Log in", use_container_width=True):
                            _handle_login(username, password, use_sidebar=False)
                with tab_signup:
                    with st.form("top_signup"):
                        new_user = st.text_input("Username", key="top_signup_user")
                        new_pass = st.text_input("Password", type="password", key="top_signup_pass")
                        confirm = st.text_input("Confirm", type="password", key="top_signup_confirm")
                        if st.form_submit_button("Create account", use_container_width=True):
                            _handle_signup(new_user, new_pass, confirm, use_sidebar=False)
                with st.expander("Demo credentials"):
                    st.code("username: demo_traveler\npassword: DemoPass123", language="text")


def init_app_shell():
    inject_styles()
    render_sidebar_branding()
    render_top_auth()
    show_login_dialog_if_needed()


def render_banner(compact: bool = False):
    bg_div = ""
    if BANNER_IMAGE.exists():
        img_style = f"background-image: url('data:image/jpeg;base64,{_banner_b64()}');"
        bg_div = f"<div class='bb-hero-bg' style='{img_style}'></div>"

    height = "160px" if compact else "220px"
    title_size = "1.8rem" if compact else "2.6rem"

    st.html(
        f'<div class="bb-hero" style="min-height:{height}">'
        f"{bg_div}"
        f'<div class="bb-hero-overlay"></div>'
        f'<div class="bb-hero-content">'
        f'<span class="bb-badge">{APP_ICON} AI-Powered Indian Travel</span>'
        f'<h1 style="font-size:{title_size}">{APP_NAME}</h1>'
        f"<p>{APP_TAGLINE}</p>"
        f"</div></div>"
    )


def _banner_b64():
    import base64
    return base64.b64encode(BANNER_IMAGE.read_bytes()).decode()


def render_stats():
    st.html(
        '<div class="bb-stat-row">'
        '<div class="bb-stat"><div class="bb-stat-num">28+</div>'
        '<div class="bb-stat-label">States & Union Territories</div></div>'
        '<div class="bb-stat"><div class="bb-stat-num">40+</div>'
        '<div class="bb-stat-label">UNESCO World Heritage Sites</div></div>'
        '<div class="bb-stat"><div class="bb-stat-num">AI</div>'
        '<div class="bb-stat-label">Grounded Recommendations</div></div>'
        '<div class="bb-stat"><div class="bb-stat-num">∞</div>'
        '<div class="bb-stat-label">Stories Waiting to Unfold</div></div>'
        "</div>"
    )


def render_featured_destinations():
    st.markdown("### ✨ Featured Destinations")
    cols = st.columns(3)
    for i, dest in enumerate(FEATURED_DESTINATIONS):
        with cols[i % 3]:
            st.html(
                f'<div class="bb-dest-card">'
                f'<div class="bb-dest-emoji">{dest["emoji"]}</div>'
                f'<div class="bb-dest-name">{dest["name"]}</div>'
                f'<span class="bb-dest-tag">{dest["tag"]}</span>'
                f'<div class="bb-dest-blurb">{dest["blurb"]}</div>'
                f"</div>"
            )


def render_how_it_works():
    st.markdown("### 🗺️ How Bharat Bhraman Works")
    steps = [
        ("Create an account", "Sign up in seconds — your journey is personal and saved."),
        ("Complete onboarding", "Share interests like heritage, food, trekking or festivals."),
        ("Discover & explore", "Get verified attractions, hidden gems & cultural stories."),
        ("Build your history", "Every search refines your next adventure across Bharat."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.html(
            f'<div class="bb-step"><strong>Step {i} — {title}</strong><br>{desc}</div>'
        )


def _handle_login(username, password, use_sidebar=False):
    from services import auth
    try:
        st.session_state.user = auth.login(username, password)
        st.rerun()
    except auth.AuthError as e:
        (st.sidebar if use_sidebar else st).error(str(e))


def _handle_signup(username, password, confirm, use_sidebar=False):
    from services import auth
    target = st.sidebar if use_sidebar else st
    if password != confirm:
        target.error("Passwords do not match.")
        return
    try:
        auth.signup(username, password)
        target.success("Account created — log in above.")
    except auth.AuthError as e:
        target.error(str(e))


@st.dialog("Login required")
def _login_dialog():
    st.markdown(
        f"### {APP_ICON} Welcome to {APP_NAME}\n\n"
        "Please **log in** or **create an account** using the **Log in** button at the top right."
    )
    if st.button("Got it", use_container_width=True, type="primary"):
        st.session_state.pop("_show_login_dialog", None)
        st.rerun()


def prompt_login():
    st.session_state["_show_login_dialog"] = True


def show_login_dialog_if_needed():
    if st.session_state.get("_show_login_dialog") and not st.session_state.get("user"):
        _login_dialog()


def gated_button(label, key, **kwargs):
    if st.button(label, key=key, **kwargs):
        if st.session_state.get("user"):
            return True
        prompt_login()
        st.rerun()
    return False


def render_preview_notice(page_name: str):
    st.html(
        f'<div class="bb-preview-banner">'
        f"👀 <strong>Preview mode</strong> — You're viewing {page_name}. "
        f"Log in at the <strong>top right</strong> to interact. "
        f"Clicking any control will prompt you to sign in."
        f"</div>"
    )


def render_login_overlay():
    if st.session_state.get("user"):
        return

    import streamlit.components.v1 as components

    components.html(
        """
        <script>
        (function() {
            if (window.__bbOverlay) return;
            window.__bbOverlay = true;

            const overlay = document.createElement('div');
            overlay.id = 'bb-login-overlay';
            overlay.style.cssText = `
                position: fixed; z-index: 9998; cursor: pointer;
                background: rgba(255, 249, 243, 0.01);
            `;

            const modal = document.createElement('div');
            modal.id = 'bb-login-modal';
            modal.style.cssText = `
                display: none; position: fixed; top: 50%; left: 50%;
                transform: translate(-50%, -50%); z-index: 9999;
                background: white; border-radius: 16px;
                padding: 28px 32px; max-width: 400px; width: 90%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.25);
                font-family: 'Poppins', sans-serif; text-align: center;
                border: 2px solid #FF9933;
            `;
            modal.innerHTML = `
                <div style="font-size:2.5rem;margin-bottom:8px">🇮🇳</div>
                <h2 style="margin:0 0 8px;font-family:Georgia,serif;color:#C45A00">
                    Login Required
                </h2>
                <p style="color:#555;font-size:0.95rem;line-height:1.5;margin-bottom:18px">
                    Click <strong>Log in</strong> at the top right to explore Bharat Bhraman.
                </p>
                <button id="bb-close-modal" style="
                    background:#E8751A;color:white;border:none;
                    padding:10px 28px;border-radius:8px;cursor:pointer;
                    font-size:0.95rem;font-weight:600;
                ">Got it</button>
            `;

            function positionOverlay() {
                const main = document.querySelector('section.main');
                if (!main) return;
                const rect = main.getBoundingClientRect();
                overlay.style.top = rect.top + 'px';
                overlay.style.left = rect.left + 'px';
                overlay.style.width = rect.width + 'px';
                overlay.style.height = rect.height + 'px';
            }

            document.body.appendChild(overlay);
            document.body.appendChild(modal);
            positionOverlay();
            window.addEventListener('resize', positionOverlay);

            overlay.addEventListener('click', function() {
                document.getElementById('bb-login-modal').style.display = 'block';
            });

            document.getElementById('bb-close-modal').addEventListener('click', function() {
                document.getElementById('bb-login-modal').style.display = 'none';
            });
        })();
        </script>
        """,
        height=0,
    )
