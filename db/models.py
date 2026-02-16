"""
SQLite schema initialization — creates all tables on first run.
"""
import sqlite3
from pathlib import Path


def init_db(db_path: str) -> None:
    """
    Initialize the SQLite database.

    Creates the database file and all tables if they don't exist.
    Safe to call multiple times — uses CREATE TABLE IF NOT EXISTS.

    Args:
        db_path: Path to the SQLite database file.
    """
    # Auto-create parent directory
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.executescript(_SCHEMA_SQL)


_SCHEMA_SQL = """
-- ── Articles ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS articles (
    id              INTEGER PRIMARY KEY,
    raindrop_id     TEXT UNIQUE,
    date            TEXT,
    title           TEXT,
    source_url      TEXT,
    raw_content     TEXT,
    summary         TEXT,
    key_insights    TEXT,
    action_item     TEXT,
    researcher_output   TEXT,
    architect_output    TEXT,
    skeptic_output      TEXT,
    synthesizer_output  TEXT,
    status          TEXT DEFAULT 'queued',
    queued_at       TEXT,
    collection_name TEXT,
    priority        INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ── Reflections ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reflections (
    id              INTEGER PRIMARY KEY,
    article_id      INTEGER REFERENCES articles(id),
    reflection_text TEXT,
    action_item     TEXT,
    confidence_score INTEGER CHECK(confidence_score BETWEEN 1 AND 10),
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ── Sessions ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY,
    date            TEXT,
    start_time      TEXT,
    end_time        TEXT,
    duration_minutes INTEGER,
    activity_type   TEXT,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ── Batch Digests ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS batch_digests (
    id                  INTEGER PRIMARY KEY,
    article_ids         TEXT,
    digest_output       TEXT,
    deep_dive_selected  TEXT,
    created_at          TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ── Weekly Reports ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_reports (
    id              INTEGER PRIMARY KEY,
    week_start      TEXT,
    themes_detected TEXT,
    knowledge_gap   TEXT,
    build_suggestion TEXT,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);
"""
