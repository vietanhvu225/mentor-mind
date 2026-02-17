"""
Scheduler Service — APScheduler daily jobs for automated sync + analysis.

Usage:
    from services.scheduler import init_scheduler, get_scheduler_info

    scheduler = init_scheduler(bot)   # start scheduler with bot instance
    info = get_scheduler_info()       # get status for /schedule command
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from strings import t

import config

logger = logging.getLogger(__name__)

# ── Module-level singleton ────────────────────────────────────────
_scheduler: Optional[AsyncIOScheduler] = None
_bot = None  # Telegram bot reference

JOB_ID = "daily_sync_analyze"
WEEKLY_JOB_ID = "weekly_synthesis"


def init_scheduler(bot) -> AsyncIOScheduler:
    """
    Initialize and start the APScheduler.

    Args:
        bot: telegram.Bot instance for sending messages.

    Returns:
        The started AsyncIOScheduler.
    """
    global _scheduler, _bot
    _bot = bot

    _scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)

    if config.SCHEDULE_ENABLED:
        _scheduler.add_job(
            _daily_job,
            CronTrigger(
                hour=config.SCHEDULE_HOUR,
                minute=config.SCHEDULE_MINUTE,
                timezone=config.TIMEZONE,
            ),
            id=JOB_ID,
            name="Daily Sync & Analyze",
            replace_existing=True,
        )
        logger.info(
            "Scheduler started → daily job at %02d:%02d (%s)",
            config.SCHEDULE_HOUR, config.SCHEDULE_MINUTE, config.TIMEZONE,
        )

        # Weekly synthesis — every Sunday at 23:00
        _scheduler.add_job(
            _weekly_job,
            CronTrigger(
                day_of_week="sun",
                hour=23,
                minute=0,
                timezone=config.TIMEZONE,
            ),
            id=WEEKLY_JOB_ID,
            name="Weekly Synthesis",
            replace_existing=True,
        )
        logger.info("Weekly synthesis job → Sunday 23:00 (%s)", config.TIMEZONE)
    else:
        logger.info("Scheduler disabled (SCHEDULE_ENABLED=false)")

    _scheduler.start()
    return _scheduler


async def _daily_job() -> None:
    """
    Daily scheduled job: sync from Raindrop → analyze next article → send to Telegram.

    Mirrors the proven /analyze command pattern for reliability.
    Graceful: if any step fails, send error notification and continue.
    """
    import asyncio as _asyncio
    from functools import partial
    from bot.telegram_handler import send_long_message
    from services.raindrop import fetch_all_new_raindrops, sync_raindrops_to_db
    from services.extractor import extract_content
    from services.analyzer import analyze_article
    from db.repository import update_article_analysis, update_article_status

    chat_id = config.TELEGRAM_CHAT_ID
    if not chat_id:
        logger.warning("TELEGRAM_CHAT_ID not set — skipping daily job")
        return

    logger.info("=== Daily job started ===")

    # Notify user that job has started
    try:
        await _bot.send_message(chat_id=chat_id, text=t("daily_started"))
    except Exception:
        pass

    try:
        db_path = str(config.DATABASE_PATH)
        loop = _asyncio.get_running_loop()

        # Step 1: Sync from Raindrop
        new_raindrops = await loop.run_in_executor(
            None, partial(fetch_all_new_raindrops, db_path)
        )
        if new_raindrops is None:
            new_raindrops = []
        sync_result = await loop.run_in_executor(
            None, partial(sync_raindrops_to_db, new_raindrops, db_path)
        )
        logger.info(f"Synced {sync_result.new_inserted} new articles")

        # Step 2: Pick next queued article (reuse same function as /analyze)
        from services.raindrop import pick_next_article
        article = await loop.run_in_executor(
            None, partial(pick_next_article, db_path)
        )

        if not article:
            await _bot.send_message(
                chat_id=chat_id,
                text=t("daily_queue_empty"),
            )
            return

        article_id = article.get("id")
        title = article.get("title", "Untitled")
        source_url = article.get("source_url", "")
        fallback_text = article.get("raw_content", "")
        logger.info(f"Processing article #{article_id}: {title[:60]}")

        # Step 3: Extract content (blocking → executor, using partial like /analyze)
        extraction = await loop.run_in_executor(
            None, partial(extract_content, source_url, fallback_text)
        )

        if not extraction.content:
            await _bot.send_message(
                chat_id=chat_id,
                text=t("daily_extract_fail", id=article_id, title=title[:60]),
            )
            return

        # Step 4: Analyze (blocking LLM → executor, using partial like /analyze)
        images = extraction.images if extraction.images else None
        analysis = await loop.run_in_executor(
            None,
            partial(
                analyze_article,
                extraction.content,
                article_link=source_url,
                images=images,
            ),
        )

        # Step 5: Save to DB — same as /analyze: update analysis fields + status
        if extraction.content and extraction.source != "excerpt":
            from db.repository import _connect
            with _connect(db_path) as conn:
                conn.execute(
                    "UPDATE articles SET raw_content = ? WHERE id = ?",
                    (extraction.content[:10000], article_id),
                )

        update_article_analysis(
            db_path,
            article_id,
            summary=analysis.stage_2_output or analysis.stage_1_output or "",
            researcher_output=analysis.stage_1_output or "",
            synthesizer_output=analysis.stage_2_output or "",
        )
        update_article_status(db_path, article_id, "sent")

        # Step 6: Send to Telegram — NO parse_mode to avoid 400 errors on LLM output
        lines = [t("daily_analysis_header", id=article_id, title=title, url=source_url)]

        if analysis.stage_1_output:
            lines.append(analysis.stage_1_output)
        if analysis.stage_2_output:
            lines.append("\n" + analysis.stage_2_output)
        if analysis.warning:
            lines.append("\n⚠️ " + analysis.warning)

        output_text = "\n".join(lines)
        await send_long_message(_bot, chat_id, output_text, parse_mode=None)

        logger.info(f"=== Daily job complete: article #{article_id} ===")

    except Exception as e:
        logger.error(f"Daily job failed: {e}", exc_info=True)
        try:
            await _bot.send_message(
                chat_id=chat_id,
                text=t("daily_failed", error=str(e)),
            )
        except Exception:
            pass


async def _weekly_job():
    """
    Weekly scheduled job: generate weekly synthesis → send to Telegram.

    Runs every Sunday at 23:00.
    """
    chat_id = config.TELEGRAM_CHAT_ID
    db_path = str(config.DATABASE_PATH)

    logger.info("=== Weekly synthesis job started ===")

    try:
        from services.synthesizer import create_weekly_synthesis

        result = create_weekly_synthesis(db_path)

        if result.error:
            await _bot.send_message(chat_id=chat_id, text=t("weekly_job_error", error=result.error))
            return

        # Build output
        lines = [
            t("weekly_header", week_start=result.week_start),
            t("weekly_stats",
              articles=result.articles_count,
              reflections=result.reflections_count,
              minutes=result.total_session_minutes),
        ]
        if result.avg_confidence > 0:
            lines.append(t("status_avg_conf", avg=f"{result.avg_confidence:.1f}"))
        lines.append("")
        lines.append(result.output)

        output_text = "\n".join(lines)

        try:
            await _bot.send_message(chat_id=chat_id, text=output_text, parse_mode="Markdown")
        except Exception:
            await _bot.send_message(chat_id=chat_id, text=output_text)

        logger.info(f"=== Weekly synthesis sent: {result.articles_count} articles ===")

    except Exception as e:
        logger.error(f"Weekly job failed: {e}", exc_info=True)
        try:
            await _bot.send_message(chat_id=chat_id, text=t("weekly_job_failed", error=str(e)))
        except Exception:
            pass


# ── Scheduler Control ─────────────────────────────────────────────

def get_scheduler_info() -> dict:
    """Get scheduler status for /schedule command."""
    if not _scheduler:
        return {"status": "not_initialized"}

    job = _scheduler.get_job(JOB_ID)
    if not job:
        return {
            "status": "disabled",
            "enabled": False,
        }

    return {
        "status": "active",
        "enabled": True,
        "hour": config.SCHEDULE_HOUR,
        "minute": config.SCHEDULE_MINUTE,
        "timezone": config.TIMEZONE,
        "next_run": str(job.next_run_time) if job.next_run_time else "paused",
        "paused": job.next_run_time is None,
    }


def reschedule(hour: int, minute: int) -> bool:
    """Change the daily job schedule time."""
    if not _scheduler:
        return False

    job = _scheduler.get_job(JOB_ID)
    if not job:
        # Re-add if was removed
        _scheduler.add_job(
            _daily_job,
            CronTrigger(hour=hour, minute=minute, timezone=config.TIMEZONE),
            id=JOB_ID,
            name="Daily Sync & Analyze",
            replace_existing=True,
        )
    else:
        job.reschedule(
            CronTrigger(hour=hour, minute=minute, timezone=config.TIMEZONE)
        )

    config.SCHEDULE_HOUR = hour
    config.SCHEDULE_MINUTE = minute
    logger.info(f"Rescheduled daily job → {hour:02d}:{minute:02d}")
    return True


def pause_scheduler() -> bool:
    """Pause the daily job."""
    if not _scheduler:
        return False
    job = _scheduler.get_job(JOB_ID)
    if job:
        job.pause()
        logger.info("Scheduler paused")
        return True
    return False


def resume_scheduler() -> bool:
    """Resume the daily job."""
    if not _scheduler:
        return False
    job = _scheduler.get_job(JOB_ID)
    if job:
        job.resume()
        logger.info("Scheduler resumed")
        return True
    return False
