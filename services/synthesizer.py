"""
Weekly Synthesis — gather week data, LLM summary, save report.

Usage:
    from services.synthesizer import create_weekly_synthesis

    result = create_weekly_synthesis(db_path)
    print(result.output)
"""
import logging
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

from db.repository import (
    add_weekly_report,
    get_recent_reflections,
)
from services.llm_client import call_llm_with_fallback, load_prompt

logger = logging.getLogger(__name__)


@dataclass
class WeeklyResult:
    """Result of weekly synthesis."""

    output: Optional[str] = None
    week_start: str = ""
    articles_count: int = 0
    reflections_count: int = 0
    total_session_minutes: int = 0
    avg_confidence: float = 0.0
    success: bool = False
    error: Optional[str] = None


def create_weekly_synthesis(db_path: str) -> WeeklyResult:
    """
    Create a weekly synthesis report.

    Gathers data from the last 7 days:
    - Articles analyzed (status != 'queued')
    - Reflections
    - Sessions
    - Confidence scores

    Returns:
        WeeklyResult with report output and stats.
    """
    result = WeeklyResult()
    today = date.today()
    week_start = today - timedelta(days=7)
    result.week_start = week_start.isoformat()

    # 1. Gather data
    try:
        context_parts = _gather_week_data(db_path, week_start, today, result)
    except Exception as e:
        logger.error(f"Error gathering weekly data: {e}")
        result.error = f"Data gathering failed: {e}"
        return result

    if not context_parts:
        result.error = "Tuần này chưa có hoạt động học tập nào."
        return result

    # 2. Build context for LLM
    context_text = "\n\n---\n\n".join(context_parts)

    # 3. Call LLM
    try:
        logger.info("Generating weekly synthesis...")
        system_prompt = load_prompt("weekly.md")
        synthesis_output = call_llm_with_fallback(
            task_type="weekly_synthesis",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context_text},
            ],
        )
        result.output = synthesis_output
        result.success = True
        logger.info("Weekly synthesis complete ✓")
    except Exception as e:
        logger.error(f"Weekly synthesis LLM failed: {e}")
        result.error = f"LLM synthesis failed: {e}"
        return result

    # 4. Save to DB
    try:
        add_weekly_report(
            db_path,
            week_start=result.week_start,
            themes_detected=synthesis_output,
            knowledge_gap="",
            build_suggestion="",
        )
        logger.info("Weekly report saved to DB")
    except Exception as e:
        logger.error(f"Error saving weekly report: {e}")

    return result


def _gather_week_data(
    db_path: str,
    week_start: date,
    today: date,
    result: WeeklyResult,
) -> list[str]:
    """Gather all learning data from the past week."""
    import sqlite3

    parts = []

    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row

    # ── Articles analyzed this week ──
    start_str = week_start.isoformat()
    end_str = today.isoformat()
    articles = conn.execute(
        """SELECT id, title, source_url, summary, status, created_at
           FROM articles
           WHERE status != 'queued'
             AND created_at >= ? AND created_at <= ?
           ORDER BY created_at DESC""",
        (start_str, end_str + "T23:59:59"),
    ).fetchall()

    result.articles_count = len(articles)
    if articles:
        article_lines = [f"## Articles đã xử lý tuần này ({len(articles)} bài)\n"]
        for a in articles:
            title = a["title"] or "Untitled"
            status = a["status"]
            summary = (a["summary"] or "")[:200]
            article_lines.append(f"- **#{a['id']}: {title}** [{status}]")
            if summary:
                article_lines.append(f"  Tóm tắt: {summary}...")
        parts.append("\n".join(article_lines))

    # ── Reflections ──
    reflections = get_recent_reflections(db_path, days=7)
    result.reflections_count = len(reflections) if reflections else 0
    if reflections:
        ref_lines = [f"## Reflections ({len(reflections)} entries)\n"]
        scores = []
        for r in reflections:
            ref_lines.append(f"- Insight: {r['reflection_text'][:100]}")
            ref_lines.append(f"  Action: {r['action_item'][:100]}")
            ref_lines.append(f"  Confidence: {r['confidence_score']}/10")
            scores.append(r["confidence_score"])
        result.avg_confidence = sum(scores) / len(scores) if scores else 0
        parts.append("\n".join(ref_lines))

    # ── Sessions ──
    sessions = conn.execute(
        """SELECT date, duration_minutes FROM sessions
           WHERE date >= ? AND date <= ?""",
        (start_str, end_str),
    ).fetchall()

    total_minutes = sum(s["duration_minutes"] for s in sessions) if sessions else 0
    result.total_session_minutes = total_minutes
    if sessions:
        parts.append(
            f"## Sessions\n\n"
            f"- Tổng: {len(sessions)} sessions\n"
            f"- Tổng thời gian: {total_minutes} phút\n"
            f"- Trung bình: {total_minutes // len(sessions)} phút/session"
        )

    conn.close()

    # ── Stats summary ──
    if parts:
        stats = (
            f"## Stats Overview\n\n"
            f"- 📚 Articles: {result.articles_count}\n"
            f"- 💭 Reflections: {result.reflections_count}\n"
            f"- ⏱️ Study time: {result.total_session_minutes} phút\n"
            f"- 📈 Avg confidence: {result.avg_confidence:.1f}/10"
        )
        parts.insert(0, stats)

    return parts
