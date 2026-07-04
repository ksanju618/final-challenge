"""
Database access layer.

Uses SQLite for the hackathon build. Kept intentionally thin and
function-based (no ORM) so the whole data layer is auditable in one file.

NOTE ON PERSISTENCE: Streamlit Community Cloud's filesystem is ephemeral.
Data persists for the lifetime of a running app instance but resets on
redeploy or after the app sleeps from inactivity. This is acceptable for a
hackathon demo. To move to real persistence later, swap `get_connection()`
to point at a hosted Postgres instance (e.g. Supabase) - every other
function in this file uses plain SQL that is compatible with both engines
with minimal changes.
"""

import sqlite3
import os
import json
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "data/app.db")


def _ensure_data_dir():
    directory = os.path.dirname(DB_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


@contextmanager
def get_connection():
    """Yields a SQLite connection with foreign keys enabled, and commits/closes safely."""
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Creates all tables if they do not already exist. Safe to call on every app start."""
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS user_profile (
                user_id INTEGER PRIMARY KEY,
                interests TEXT,
                experience_level TEXT,
                travel_style TEXT,
                onboarded INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                destination TEXT NOT NULL,
                query_type TEXT NOT NULL,
                raw_response TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )


# ---------- Users ----------

def create_user(username: str, password_hash: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, password_hash, datetime.now(timezone.utc).isoformat()),
        )
        user_id = cur.lastrowid
        conn.execute(
            "INSERT INTO user_profile (user_id, interests, experience_level, travel_style, onboarded) "
            "VALUES (?, '[]', '', '', 0)",
            (user_id,),
        )
        return user_id


def get_user_by_username(username: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return dict(row) if row else None


def username_exists(username: str) -> bool:
    return get_user_by_username(username) is not None


# ---------- Profile ----------

def get_profile(user_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM user_profile WHERE user_id = ?", (user_id,)
        ).fetchone()
        if not row:
            return None
        profile = dict(row)
        profile["interests"] = json.loads(profile["interests"] or "[]")
        return profile


def save_profile(user_id: int, interests: list, experience_level: str, travel_style: str):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE user_profile
            SET interests = ?, experience_level = ?, travel_style = ?, onboarded = 1
            WHERE user_id = ?
            """,
            (json.dumps(interests), experience_level, travel_style, user_id),
        )


# ---------- Search history ----------

def log_search(user_id: int, destination: str, query_type: str, raw_response: str):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO search_history (user_id, destination, query_type, raw_response, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, destination, query_type, raw_response, datetime.now(timezone.utc).isoformat()),
        )


def get_history(user_id: int, limit: int = 20):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM search_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def get_past_destinations(user_id: int) -> list:
    """Distinct destinations a user has searched before - used to personalize future prompts."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT destination FROM search_history WHERE user_id = ? ORDER BY id DESC LIMIT 10",
            (user_id,),
        ).fetchall()
        return [r["destination"] for r in rows]
