"""Thread → Claude session persistence via SQLite.

Maps Slack thread_ts to Claude Agent SDK session_id so that replies in the
same Slack thread continue the same Claude conversation.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    thread_ts   TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    updated_at  INTEGER NOT NULL
);
"""

# Drop mappings older than this so stale sessions don't resurrect weeks later.
MAX_AGE_SECONDS = 7 * 24 * 3600  # 7 days


class SessionStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(_SCHEMA)

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get(self, thread_ts: str) -> str | None:
        cutoff = int(time.time()) - MAX_AGE_SECONDS
        with self._conn() as c:
            row = c.execute(
                "SELECT session_id FROM sessions WHERE thread_ts = ? AND updated_at >= ?",
                (thread_ts, cutoff),
            ).fetchone()
            return row[0] if row else None

    def set(self, thread_ts: str, session_id: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO sessions(thread_ts, session_id, updated_at) VALUES(?, ?, ?) "
                "ON CONFLICT(thread_ts) DO UPDATE SET session_id=excluded.session_id, "
                "updated_at=excluded.updated_at",
                (thread_ts, session_id, int(time.time())),
            )

    def cleanup_stale(self) -> int:
        cutoff = int(time.time()) - MAX_AGE_SECONDS
        with self._conn() as c:
            cur = c.execute("DELETE FROM sessions WHERE updated_at < ?", (cutoff,))
            return cur.rowcount
