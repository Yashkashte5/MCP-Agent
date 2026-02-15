import sqlite3
from datetime import datetime

DB_PATH = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory_summary (
            session_id TEXT PRIMARY KEY,
            summary TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_memory(session_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO memory (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (session_id, role, str(content), datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def get_memory(session_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT role, content FROM memory WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )

    rows = cur.fetchall()
    conn.close()

    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

def save_summary(session_id, summary):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO memory_summary(session_id, summary)
        VALUES (?, ?)
        ON CONFLICT(session_id)
        DO UPDATE SET summary=excluded.summary
    """, (session_id, summary))

    conn.commit()
    conn.close()


def get_summary(session_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT summary FROM memory_summary WHERE session_id=?",
        (session_id,)
    )

    row = cur.fetchone()
    conn.close()

    return row[0] if row else ""
