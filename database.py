"""SQLite persistence for parsed candidate records."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("candidates.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection



def init_db():
    with get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT,
            resume_text TEXT,
            source_filename TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")


def add_candidate(data, filename):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO candidates (name,email,phone,skills,education,resume_text,source_filename) VALUES (?,?,?,?,?,?,?)",
            (data["name"], data["email"], data["phone"], ", ".join(data["skills"]), " | ".join(data["education"]), data["resume_text"], filename)
        )
        return cursor.lastrowid


def search_candidates(query=""):
    with get_connection() as conn:
        if query.strip():
            pattern = f"%{query.strip()}%"
            rows = conn.execute("""SELECT * FROM candidates WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? OR skills LIKE ? OR education LIKE ? ORDER BY created_at DESC""",
                               (pattern, pattern, pattern, pattern, pattern)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM candidates ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]


def get_candidate(candidate_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM candidates WHERE id=?", (candidate_id,)).fetchone()
        return dict(row) if row else None
