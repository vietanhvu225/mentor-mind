"""Integration tests for database layer."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))


def log(msg):
    with open("test_results.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)


with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write("=== Database Integration Test Results ===\n\n")

# Use temp file for testing
db_path = os.path.join(tempfile.gettempdir(), "test_learning.db")

# Clean up from previous runs
if os.path.exists(db_path):
    os.remove(db_path)

# ── Test 1: init_db ────────────────────────────────────────────────
log("TEST 1: Database initialization...")
try:
    from db.models import init_db
    init_db(db_path)
    assert os.path.exists(db_path), "DB file not created"

    import sqlite3
    conn = sqlite3.connect(db_path)
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    table_names = [t[0] for t in tables]
    conn.close()

    expected = ["articles", "batch_digests", "reflections", "sessions", "weekly_reports"]
    assert table_names == expected, f"Expected {expected}, got {table_names}"
    log(f"  Tables: {table_names}")
    log("  RESULT: PASS ✓\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 2: Article CRUD ──────────────────────────────────────────
log("TEST 2: Article CRUD...")
try:
    from db.repository import (
        add_article, get_article_by_id, get_articles_by_status,
        update_article_status, update_article_analysis,
        get_next_queued_article, get_oldest_queued_articles,
        count_articles_by_status,
    )

    # Add
    id1 = add_article(db_path, "rd_001", "Test Article 1", "https://example.com/1")
    id2 = add_article(db_path, "rd_002", "Test Article 2", "https://example.com/2", priority=1)
    log(f"  Added articles: id={id1}, id={id2}")

    # Get by ID
    art = get_article_by_id(db_path, id1)
    assert art is not None, "Article not found"
    assert art["title"] == "Test Article 1"
    assert art["status"] == "queued"
    log(f"  Get by ID: {art['title']}, status={art['status']}")

    # Get by status
    queued = get_articles_by_status(db_path, "queued")
    assert len(queued) == 2, f"Expected 2 queued, got {len(queued)}"
    log(f"  Queued articles: {len(queued)}")

    # Update status
    update_article_status(db_path, id1, "sent")
    art = get_article_by_id(db_path, id1)
    assert art["status"] == "sent"
    log(f"  Status updated: {art['status']}")

    # Update analysis
    update_article_analysis(db_path, id1, summary="Test summary", researcher_output="Test output")
    art = get_article_by_id(db_path, id1)
    assert art["summary"] == "Test summary"
    assert art["researcher_output"] == "Test output"
    log(f"  Analysis updated: summary='{art['summary']}'")

    # Queue helpers
    next_art = get_next_queued_article(db_path)
    assert next_art["id"] == id2, "Priority article should be first"
    log(f"  Next queued (priority): {next_art['title']}")

    oldest = get_oldest_queued_articles(db_path, 5)
    assert len(oldest) == 1, f"Expected 1 queued, got {len(oldest)}"
    log(f"  Oldest queued: {len(oldest)}")

    counts = count_articles_by_status(db_path)
    assert counts.get("sent") == 1
    assert counts.get("queued") == 1
    log(f"  Counts: {counts}")

    # Duplicate prevention
    try:
        add_article(db_path, "rd_001", "Duplicate", "https://dup.com")
        log("  Duplicate: FAIL ✗ — should have raised")
    except sqlite3.IntegrityError:
        log("  Duplicate prevention: OK ✓")

    log("  RESULT: PASS ✓\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 3: Reflection CRUD ───────────────────────────────────────
log("TEST 3: Reflection CRUD...")
try:
    from db.repository import add_reflection, get_reflections_by_article, get_recent_reflections

    ref_id = add_reflection(db_path, id1, "Learned RAG", "Build demo", 8)
    log(f"  Added reflection: id={ref_id}")

    refs = get_reflections_by_article(db_path, id1)
    assert len(refs) == 1
    assert refs[0]["confidence_score"] == 8
    log(f"  Get by article: {len(refs)}, confidence={refs[0]['confidence_score']}")

    recent = get_recent_reflections(db_path, days=7)
    assert len(recent) >= 1
    log(f"  Recent reflections: {len(recent)}")

    # Confidence validation
    try:
        add_reflection(db_path, id1, "Bad", "Bad", 11)
        log("  Confidence validation: FAIL ✗ — should have raised")
    except sqlite3.IntegrityError:
        log("  Confidence 11 rejected: OK ✓")

    try:
        add_reflection(db_path, id1, "Bad", "Bad", 0)
        log("  Confidence validation: FAIL ✗ — should have raised")
    except sqlite3.IntegrityError:
        log("  Confidence 0 rejected: OK ✓")

    log("  RESULT: PASS ✓\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 4: Session, Batch, Weekly ─────────────────────────────────
log("TEST 4: Sessions, Batch Digests, Weekly Reports...")
try:
    from db.repository import (
        add_session, get_sessions_by_date,
        add_batch_digest, get_latest_digest,
        add_weekly_report, get_latest_report,
    )

    # Session
    sid = add_session(db_path, "2026-02-15", "21:00", "22:00", 60, "reflection")
    sessions = get_sessions_by_date(db_path, "2026-02-15")
    assert len(sessions) == 1
    assert sessions[0]["duration_minutes"] == 60
    log(f"  Session: id={sid}, duration={sessions[0]['duration_minutes']}min")

    # Batch digest
    bid = add_batch_digest(db_path, [1, 2, 3], "Digest output", [2])
    digest = get_latest_digest(db_path)
    assert digest["article_ids"] == [1, 2, 3]
    assert digest["deep_dive_selected"] == [2]
    log(f"  Batch digest: id={bid}, articles={digest['article_ids']}")

    # Weekly report
    wid = add_weekly_report(db_path, "2026-02-10", "AI trends", "MLOps gap", "Build RAG demo")
    report = get_latest_report(db_path)
    assert report["themes_detected"] == "AI trends"
    log(f"  Weekly report: id={wid}, themes='{report['themes_detected']}'")

    log("  RESULT: PASS ✓\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 5: Second init doesn't reset data ─────────────────────────
log("TEST 5: Second init_db preserves data...")
try:
    init_db(db_path)  # Run again
    art = get_article_by_id(db_path, id1)
    assert art is not None, "Data lost after second init"
    assert art["title"] == "Test Article 1"
    log(f"  After second init: article still exists — '{art['title']}'")
    log("  RESULT: PASS ✓\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# Clean up
try:
    os.remove(db_path)
except PermissionError:
    pass  # Windows file lock — harmless
log("=== All tests done ===")
