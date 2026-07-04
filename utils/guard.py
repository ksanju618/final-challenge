"""Shared guard — preview mode for guests, full access for logged-in users."""

import streamlit as st

from utils.ui import prompt_login, render_login_overlay, render_preview_notice


def get_user():
    return st.session_state.get("user")


def is_logged_in():
    return bool(get_user())


def require_login():
    """Return user if logged in; otherwise render preview gate and stop."""
    user = get_user()
    if user:
        return user

    render_preview_notice("this page")
    render_login_overlay()
    st.stop()


def require_login_or_none():
    """Return user or None without stopping — for pages that render their own preview."""
    return get_user()


def gate_interaction():
    """Call before processing a form/button. Returns True if user may proceed."""
    if is_logged_in():
        return True
    prompt_login()
    return False
