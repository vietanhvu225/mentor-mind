"""
Database repository — CRUD functions for all tables.

All functions take db_path as first argument and use short-lived connections.
All queries are parameterized to prevent SQL injection.
"""
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Optional


def _dict_factory(cursor, row):
    """Convert sqlite3 rows to dicts."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def _connect(db_path: str) -> sqlite3.Connection:
    """Create a connection with dict row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = _dict_factory
    return conn


# ═══════════════════════════════════════════════════════════════════
#  ARTICLES
# ═══════════════════════════════════════════════════════════════════

def add_article(
    db_path: str,
    raindrop_id: str,
    title: str,
    source_url: str,
    *,
    date: Optional[str] = None,
    raw_content: Optional[str] = None,
    collection_name: Optional[str] = None,
    priority: int = 0,
    queued_at: Optional[str] = None,
) -> int:
    """Insert a new article. Returns the new article ID."""
    if queued_at is None:
        queued_at = datetime.now().isoformat()
    with _connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO articles
               (raindrop_id, title, source_url, date, raw_content,
                collection_name, priority, queued_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (raindrop_id, title, source_url, date, raw_content,
             collection_name, priority, queued_at),
        )
        return cursor.lastrowid


def get_article_by_id(db_path: str, article_id: int) -> Optional[dict]:
    """Get a single article by ID. Returns dict or None."""
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?", (article_id,)
        ).fetchone()
        return row


def get_article_by_raindrop_id(db_path: str, raindrop_id: str) -> Optional[dict]:
    """Get a single article by raindrop_id. Returns dict or None."""
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE raindrop_id = ?", (raindrop_id,)
        ).fetchone()
        return row


def get_articles_by_status(db_path: str, status: str) -> list[dict]:
    """Get all articles with a given status."""
    with _connect(db_path) as conn:
        return conn.execute(
            "SELECT * FROM articles WHERE status = ? ORDER BY queued_at",
            (status,),
        ).fetchall()


def get_article_by_id(db_path: str, article_id: int) -> Optional[dict]:
    """Get a single article by its ID."""
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?",
            (article_id,),
        ).fetchone()
        return dict(row) if row else None


def update_article_status(
    db_path: str, article_id: int, new_status: str
) -> None:
    """Update the status of an article."""
    with _connect(db_path) as conn:
        conn.execute(
            "UPDATE articles SET status = ? WHERE id = ?",
            (new_status, article_id),
        )


def update_article_analysis(
    db_path: str,
    article_id: int,
    *,
    summary: Optional[str] = None,
    key_insights: Optional[str] = None,
    action_item: Optional[str] = None,
    researcher_output: Optional[str] = None,
    architect_output: Optional[str] = None,
    skeptic_output: Optional[str] = None,
    synthesizer_output: Optional[str] = None,
) -> None:
    """Update analysis fields of an article (only non-None fields)."""
    fields = {}
    if summary is not None:
        fields["summary"] = summary
    if key_insights is not None:
        fields["key_insights"] = key_insights
    if action_item is not None:
        fields["action_item"] = action_item
    if researcher_output is not None:
        fields["researcher_output"] = researcher_output
    if architect_output is not None:
        fields["architect_output"] = architect_output
    if skeptic_output is not None:
        fields["skeptic_output"] = skeptic_output
    if synthesizer_output is not None:
        fields["synthesizer_output"] = synthesizer_output

    if not fields:
        return

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [article_id]

    with _connect(db_path) as conn:
        conn.execute(
            f"UPDATE articles SET {set_clause} WHERE id = ?",
            values,
        )


def get_next_queued_article(db_path: str) -> Optional[dict]:
    """Get the oldest queued article (priority DESC, queued_at ASC)."""
    with _connect(db_path) as conn:
        return conn.execute(
            """SELECT * FROM articles
               WHERE status = 'queued'
               ORDER BY priority DESC, queued_at ASC
               LIMIT 1""",
        ).fetchone()


def get_newest_queued_articles(db_path: str, n: int) -> list[dict]:
    """Get the newest n queued articles (priority DESC, newest first)."""
    with _connect(db_path) as conn:
        return conn.execute(
            """SELECT * FROM articles
               WHERE status = 'queued'
               ORDER BY priority DESC, queued_at DESC
               LIMIT ?""",
            (n,),
        ).fetchall()


def count_articles_by_status(db_path: str) -> dict:
    """Count articles grouped by status. Returns {status: count}."""
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) as count FROM articles GROUP BY status"
        ).fetchall()
        return {row["status"]: row["count"] for row in rows}


# ═══════════════════════════════════════════════════════════════════
#  REFLECTIONS
# ═══════════════════════════════════════════════════════════════════

def add_reflection(
    db_path: str,
    article_id: int,
    reflection_text: str,
    action_item: str,
    confidence_score: int,
) -> int:
    """Add a reflection for an article. Returns the new reflection ID."""
    with _connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO reflections
               (article_id, reflection_text, action_item, confidence_score)
               VALUES (?, ?, ?, ?)""",
            (article_id, reflection_text, action_item, confidence_score),
        )
        return cursor.lastrowid


def get_reflections_by_article(db_path: str, article_id: int) -> list[dict]:
    """Get all reflections for a given article."""
    with _connect(db_path) as conn:
        return conn.execute(
            "SELECT * FROM reflections WHERE article_id = ? ORDER BY created_at",
            (article_id,),
        ).fetchall()


def get_recent_reflections(db_path: str, days: int = 7) -> list[dict]:
    """Get reflections from the last N days."""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    with _connect(db_path) as conn:
        return conn.execute(
            "SELECT * FROM reflections WHERE created_at >= ? ORDER BY created_at DESC",
            (cutoff,),
        ).fetchall()


# ═══════════════════════════════════════════════════════════════════
#  SESSIONS
# ═══════════════════════════════════════════════════════════════════

def add_session(
    db_path: str,
    date: str,
    start_time: str,
    end_time: str,
    duration_minutes: int,
    activity_type: str,
) -> int:
    """Add a learning session. Returns the new session ID."""
    with _connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO sessions
               (date, start_time, end_time, duration_minutes, activity_type)
               VALUES (?, ?, ?, ?, ?)""",
            (date, start_time, end_time, duration_minutes, activity_type),
        )
        return cursor.lastrowid


def get_sessions_by_date(db_path: str, date: str) -> list[dict]:
    """Get all sessions for a given date."""
    with _connect(db_path) as conn:
        return conn.execute(
            "SELECT * FROM sessions WHERE date = ? ORDER BY start_time",
            (date,),
        ).fetchall()


# ═══════════════════════════════════════════════════════════════════
#  BATCH DIGESTS
# ═══════════════════════════════════════════════════════════════════

def add_batch_digest(
    db_path: str,
    article_ids: list[int],
    digest_output: str,
    deep_dive_selected: Optional[list[int]] = None,
) -> int:
    """Add a batch digest. article_ids and deep_dive_selected stored as JSON."""
    with _connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO batch_digests
               (article_ids, digest_output, deep_dive_selected)
               VALUES (?, ?, ?)""",
            (
                json.dumps(article_ids),
                digest_output,
                json.dumps(deep_dive_selected or []),
            ),
        )
        return cursor.lastrowid


def get_latest_digest(db_path: str) -> Optional[dict]:
    """Get the most recent batch digest."""
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM batch_digests ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        if row:
            row["article_ids"] = json.loads(row["article_ids"])
            row["deep_dive_selected"] = json.loads(row["deep_dive_selected"])
        return row


# ═══════════════════════════════════════════════════════════════════
#  WEEKLY REPORTS
# ═══════════════════════════════════════════════════════════════════

def add_weekly_report(
    db_path: str,
    week_start: str,
    themes_detected: str,
    knowledge_gap: str,
    build_suggestion: str,
) -> int:
    """Add a weekly report. Returns the new report ID."""
    with _connect(db_path) as conn:
        cursor = conn.execute(
            """INSERT INTO weekly_reports
               (week_start, themes_detected, knowledge_gap, build_suggestion)
               VALUES (?, ?, ?, ?)""",
            (week_start, themes_detected, knowledge_gap, build_suggestion),
        )
        return cursor.lastrowid


def get_latest_report(db_path: str) -> Optional[dict]:
    """Get the most recent weekly report."""
    with _connect(db_path) as conn:
        return conn.execute(
            "SELECT * FROM weekly_reports ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
