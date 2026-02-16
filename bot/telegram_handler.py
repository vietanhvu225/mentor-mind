"""
Telegram bot handler — commands, message sending, error handling.
"""
import logging
from datetime import datetime, date, timedelta

from strings import t

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import config
from db.repository import (
    add_reflection,
    add_session,
    count_articles_by_status,
    get_articles_by_status,
    get_article_by_id,
    get_recent_reflections,
    get_sessions_by_date,
    update_article_analysis,
    update_article_status,
)
from services.analyzer import analyze_article
from services.raindrop import pick_next_article

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
#  REFLECTION STATES
# ═══════════════════════════════════════════════════════════════════
INSIGHT, ACTION, CONFIDENCE = range(3)


# ═══════════════════════════════════════════════════════════════════
#  COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════════

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start — welcome message."""
    logger.info(f">>> CHAT_ID from user: {update.effective_chat.id} (config has: {config.TELEGRAM_CHAT_ID})")
    text = t("start_welcome")
    await update.message.reply_text(text, parse_mode="MarkdownV2")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help — list available commands."""
    text = t("help_text")
    await update.message.reply_text(text, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status — show article statistics + streak + session."""
    try:
        db_path = str(config.DATABASE_PATH)
        counts = count_articles_by_status(db_path)
        total = sum(counts.values()) if counts else 0

        lines = ["📊 *Status*\n"]

        if total == 0:
            lines.append("Chưa có articles nào trong hệ thống.")
        else:
            status_emoji = {
                "queued": "📥",
                "sent": "📤",
                "reflected": "💭",
                "digest_reviewed": "📋",
                "skipped": "⏭️",
            }
            for status, count in counts.items():
                emoji = status_emoji.get(status, "•")
                lines.append(f"{emoji} {status}: {count}")
            lines.append(f"📚 Total: {total}")

        # Streak
        streak = calculate_streak(db_path)
        lines.append(f"\n🔥 Streak: {streak} ngày")

        # Total reflections
        recent = get_recent_reflections(db_path, days=9999)
        total_reflections = len(recent) if recent else 0
        lines.append(f"💭 Reflections: {total_reflections}")

        # Average confidence
        if total_reflections > 0:
            avg_conf = sum(r["confidence_score"] for r in recent) / total_reflections
            lines.append(f"📈 Avg confidence: {avg_conf:.1f}/10")

        # Today's session time
        today_str = date.today().isoformat()
        sessions = get_sessions_by_date(db_path, today_str)
        total_minutes = sum(s["duration_minutes"] for s in sessions) if sessions else 0
        if total_minutes > 0:
            lines.append(f"\n⏱️ Học hôm nay: {total_minutes} phút")
        else:
            lines.append(f"\n⏱️ Chưa có session hôm nay")

        text = "\n".join(lines)
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in /status: {e}")
        await update.message.reply_text("❌ Không thể lấy status. Check logs.")


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /analyze [id] — pick next or specific article, extract, analyze."""
    import asyncio
    from functools import partial
    from services.extractor import extract_content

    db_path = str(config.DATABASE_PATH)

    # 1. Pick article: by ID if provided, else from queue
    article = None
    if context.args and context.args[0].isdigit():
        target_id = int(context.args[0])
        from db.repository import get_article_by_id
        article = get_article_by_id(db_path, target_id)
        if not article:
            await update.message.reply_text(
                f"❌ Không tìm thấy bài với ID={target_id}."
            )
            return
    else:
        article = pick_next_article(db_path)
        if not article:
            await update.message.reply_text(
                "📭 Queue trống! Dùng /sync để lấy bài mới từ Raindrop."
            )
            return

    article_id = article["id"]
    title = article.get("title", "Untitled")
    source_url = article.get("source_url", "")
    excerpt = article.get("raw_content", "")

    await update.message.reply_text(
        f"⏳ Đang xử lý: *{title}*\n"
        f"🆔 ID: {article_id}\n"
        f"🔗 {source_url}\n\n"
        f"Bước 1/3: Extracting content...",
        parse_mode="Markdown",
    )

    try:
        loop = asyncio.get_event_loop()

        # 2. Extract content (smart: detect type → extract text + images)
        extraction = await loop.run_in_executor(
            None, partial(extract_content, source_url, excerpt)
        )

        # Send extraction info
        type_emoji = {"article": "📝", "youtube": "🎬", "short_video": "📱"}
        status_parts = [
            f"{type_emoji.get(extraction.content_type, '📄')} Type: {extraction.content_type}",
            f"📊 Words: {extraction.word_count}",
            f"🖼️ Images: {len(extraction.images)}",
            f"📡 Source: {extraction.source}",
        ]

        if extraction.warnings:
            for w in extraction.warnings:
                await update.message.reply_text(w)

        await update.message.reply_text(
            "Bước 2/3: Analyzing with LLM...\n\n" + "\n".join(status_parts)
        )

        # Update raw_content in DB if we got better content
        if extraction.content and extraction.source != "excerpt":
            from db.repository import _connect
            with _connect(db_path) as conn:
                conn.execute(
                    "UPDATE articles SET raw_content = ? WHERE id = ?",
                    (extraction.content[:10000], article_id),
                )

        # 3. Run LLM analysis (multimodal if images available)
        if not extraction.content:
            await update.message.reply_text(
                "❌ Không extract được content. Dùng /analyze để thử bài khác."
            )
            return

        result = await loop.run_in_executor(
            None,
            partial(
                analyze_article,
                extraction.content,
                article_link=source_url,
                images=extraction.images if extraction.images else None,
            ),
        )

        # 4. Update DB
        update_article_analysis(
            db_path,
            article_id,
            summary=result.stage_2_output or result.stage_1_output or "",
            researcher_output=result.stage_1_output or "",
            synthesizer_output=result.stage_2_output or "",
        )
        update_article_status(db_path, article_id, "sent")

        # 5. Format and send
        lines = [f"📰 *{title}*\n🆔 ID: {article_id}\n🔗 {source_url}\n"]

        if result.stage_1_output:
            lines.append(result.stage_1_output)
        if result.stage_2_output:
            lines.append("\n" + result.stage_2_output)
        if result.warning:
            lines.append("\n⚠️ " + result.warning)

        output_text = "\n".join(lines)

        MAX_LEN = 4096
        if len(output_text) <= MAX_LEN:
            await update.message.reply_text(output_text)
        else:
            chunks = []
            current = ""
            for line in output_text.split("\n"):
                if len(current) + len(line) + 1 > MAX_LEN:
                    if current:
                        chunks.append(current)
                    current = line
                else:
                    current = current + "\n" + line if current else line
            if current:
                chunks.append(current)
            for chunk in chunks:
                await update.message.reply_text(chunk)

        logger.info(f"Analysis sent: id={article_id}, {len(output_text)} chars")

        # 6. If short content, prompt user to paste link from comments
        if extraction.word_count < 200 and extraction.source == "og_meta":
            await update.message.reply_text(
                "📎 Bài ngắn (Facebook preview). Nếu có link ở comment, "
                "gửi URL trực tiếp ở đây — mình sẽ extract & phân tích bổ sung."
            )

        # 7. Show GitHub links found in content
        if extraction.github_links:
            gh_text = "🔗 *GitHub repos trong bài:*\n"
            for gh_url in extraction.github_links:
                gh_text += f"  → {gh_url}\n"
            await update.message.reply_text(gh_text)

    except Exception as e:
        logger.error(f"Error in /analyze: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Phân tích thất bại: {e}\n\n"
            "Kiểm tra:\n• Antigravity proxy chạy chưa?\n• API key đúng chưa?"
        )


async def sync_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /sync — sync new articles from Raindrop."""
    import asyncio
    from services.raindrop import fetch_all_new_raindrops, sync_raindrops_to_db

    await update.message.reply_text("⏳ Đang sync Raindrop...")

    try:
        db_path = str(config.DATABASE_PATH)

        # Run sync in executor (blocking I/O)
        loop = asyncio.get_event_loop()
        new_raindrops = await loop.run_in_executor(
            None, fetch_all_new_raindrops, db_path
        )

        if new_raindrops is None:
            new_raindrops = []

        result = await loop.run_in_executor(
            None, sync_raindrops_to_db, new_raindrops, db_path
        )

        text = (
            f"✅ *Sync hoàn tất!*\n\n"
            f"📥 Fetched: {result.total_fetched}\n"
            f"🆕 Mới: {result.new_inserted}\n"
            f"⏭️ Đã có: {result.skipped}"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Sync failed: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Sync thất bại. Kiểm tra API token và kết nối mạng."
        )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reset — reset all article statuses to 'queued' (dev tool)."""
    try:
        db_path = str(config.DATABASE_PATH)

        with __import__('sqlite3').connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT status, COUNT(*) FROM articles GROUP BY status"
            )
            before = {row[0]: row[1] for row in cursor.fetchall()}

            sent_count = before.get("sent", 0)
            if sent_count == 0:
                await update.message.reply_text(
                    "✅ Không có bài nào cần reset — tất cả đã là 'queued'."
                )
                return

            conn.execute(
                "UPDATE articles SET status = 'queued' WHERE status != 'queued'"
            )

        total = sum(before.values())
        await update.message.reply_text(
            f"🔄 Reset xong!\n\n"
            f"Trước: {before}\n"
            f"Sau: tất cả {total} bài → queued\n\n"
            f"Dùng /analyze để phân tích lại từ đầu."
        )
        logger.info(f"Reset {sent_count} articles to 'queued'")

    except Exception as e:
        logger.error(f"Reset failed: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Reset thất bại: {e}")


async def next_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /next — preview next queued article without analyzing."""
    from services.raindrop import pick_next_article

    db_path = str(config.DATABASE_PATH)
    article = pick_next_article(db_path)

    if not article:
        await update.message.reply_text("📭 Queue trống! Dùng /sync để lấy bài mới.")
        return

    article_id = article.get("id")
    title = article.get("title", "Untitled")
    url = article.get("source_url", "")
    raw = article.get("raw_content", "")
    preview = raw[:200] + "..." if len(raw) > 200 else (raw or "(no content)")

    # Count remaining
    counts = count_articles_by_status(db_path)
    queued_count = counts.get("queued", 0)

    text = (
        f"📄 *Bài tiếp theo* (#{article_id})\n\n"
        f"*{title[:100]}*\n\n"
        f"{preview}\n\n"
        f"🔗 {url}\n\n"
        f"📊 Còn {queued_count} bài trong queue\n\n"
        f"→ /analyze để phân tích | /skip để bỏ qua"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def skip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /skip — skip current queued article."""
    from services.raindrop import pick_next_article

    db_path = str(config.DATABASE_PATH)
    article = pick_next_article(db_path)

    if not article:
        await update.message.reply_text("📭 Không có bài nào để skip!")
        return

    article_id = article.get("id")
    title = article.get("title", "Untitled")
    update_article_status(db_path, article_id, "skipped")

    await update.message.reply_text(
        f"⏭️ Đã skip #{article_id}: {title[:60]}..."
    )

    # Show next article preview
    next_article = pick_next_article(db_path)

    if next_article:
        nid = next_article.get("id")
        ntitle = next_article.get("title", "Untitled")
        counts = count_articles_by_status(db_path)
        await update.message.reply_text(
            f"📄 *Bài tiếp:* #{nid} — {ntitle[:80]}\n"
            f"📊 Còn {counts.get('queued', 0)} bài\n"
            f"→ /analyze | /skip | /next",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("📭 Queue trống!")


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /schedule — view or change scheduler settings."""
    from services.scheduler import (
        get_scheduler_info, reschedule, pause_scheduler, resume_scheduler,
    )

    args = context.args

    # No args → show status
    if not args:
        info = get_scheduler_info()
        if info["status"] == "not_initialized":
            await update.message.reply_text("⚠️ Scheduler chưa khởi tạo.")
            return

        status_icon = "🟢" if info.get("enabled") and not info.get("paused") else "🔴"
        text = (
            f"⏰ *Scheduler Status*\n\n"
            f"{status_icon} Trạng thái: {'Active' if info.get('enabled') and not info.get('paused') else 'Paused/Off'}\n"
            f"🕐 Giờ chạy: {info.get('hour', '?'):02d}:{info.get('minute', '?'):02d}\n"
            f"🌏 Timezone: {info.get('timezone', '?')}\n"
            f"⏭️ Lần chạy tiếp: {info.get('next_run', '?')}\n\n"
            f"Dùng: /schedule HH:MM | /schedule on | /schedule off"
        )
        await update.message.reply_text(text, parse_mode="Markdown")
        return

    arg = args[0].lower()

    if arg == "off":
        if pause_scheduler():
            await update.message.reply_text("🔴 Scheduler đã tắt.")
        else:
            await update.message.reply_text("⚠️ Không thể tắt scheduler.")

    elif arg == "on":
        if resume_scheduler():
            await update.message.reply_text("🟢 Scheduler đã bật lại!")
        else:
            await update.message.reply_text("⚠️ Không thể bật scheduler.")

    elif ":" in arg:
        try:
            parts = arg.split(":")
            hour, minute = int(parts[0]), int(parts[1])
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
            if reschedule(hour, minute):
                await update.message.reply_text(
                    f"✅ Đã đổi lịch → {hour:02d}:{minute:02d}"
                )
            else:
                await update.message.reply_text("⚠️ Không thể đổi lịch.")
        except (ValueError, IndexError):
            await update.message.reply_text(
                "⚠️ Format sai. Dùng: /schedule HH:MM (VD: /schedule 9:30)"
            )
    else:
        await update.message.reply_text(
            "⚠️ Dùng: /schedule | /schedule HH:MM | /schedule on | /schedule off"
        )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "🤔 Không hiểu command này. Dùng /help để xem danh sách commands."
    )


# ═══════════════════════════════════════════════════════════════════
#  MESSAGE SENDING + SPLITTING
# ═══════════════════════════════════════════════════════════════════

MAX_MESSAGE_LENGTH = 4000  # Telegram limit is 4096, leave margin


def split_message(text: str, max_len: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """
    Split text into chunks for Telegram, preferring natural break points.

    Split priority: paragraph (\n\n) > line (\n) > space > hard cut.
    """
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        # Find best split point
        split_at = text.rfind("\n\n", 0, max_len)
        if split_at == -1:
            split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = text.rfind(" ", 0, max_len)
        if split_at == -1:
            split_at = max_len
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    return chunks


async def send_message(bot, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
    """
    Send a message to a specific chat. Auto-splits if too long.

    Args:
        bot: telegram.Bot instance
        chat_id: Telegram chat ID
        text: Message text
        parse_mode: "Markdown" or "MarkdownV2"

    Returns:
        True if sent successfully, False otherwise.
    """
    import asyncio
    try:
        chunks = split_message(text)
        for i, chunk in enumerate(chunks):
            await bot.send_message(chat_id=chat_id, text=chunk, parse_mode=parse_mode)
            if i < len(chunks) - 1:
                await asyncio.sleep(0.3)  # avoid rate limit
        logger.info(f"Message sent to {chat_id} ({len(text)} chars, {len(chunks)} chunk(s))")
        return True
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        return False


async def send_long_message(bot, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
    """Alias for send_message (both now support splitting)."""
    return await send_message(bot, chat_id, text, parse_mode)


# ═══════════════════════════════════════════════════════════════════
#  URL MESSAGE HANDLER
# ═══════════════════════════════════════════════════════════════════

async def url_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle regular messages containing URLs.

    When user pastes a URL (e.g., from Facebook comments),
    extract content and analyze it as a supplementary article.
    """
    import asyncio
    import re
    from functools import partial
    from services.extractor import extract_content

    text = update.message.text or ""
    # Find URLs in message
    urls = re.findall(r'https?://[^\s<>"]+', text)
    if not urls:
        return  # Not a URL message, ignore

    url = urls[0]  # Take the first URL
    await update.message.reply_text(
        f"🔗 Đang extract content từ:\n{url}\n\n⏳ Extracting..."
    )

    try:
        loop = asyncio.get_event_loop()
        extraction = await loop.run_in_executor(
            None, partial(extract_content, url)
        )

        if not extraction.content:
            await update.message.reply_text(
                "❌ Không extract được content từ URL này."
            )
            return

        # Send extraction info
        type_emoji = {"article": "📝", "youtube": "🎬", "short_video": "📱"}
        status_parts = [
            f"{type_emoji.get(extraction.content_type, '📄')} Type: {extraction.content_type}",
            f"📊 Words: {extraction.word_count}",
            f"🖼️ Images: {len(extraction.images)}",
            f"📡 Source: {extraction.source}",
        ]

        if extraction.warnings:
            for w in extraction.warnings:
                await update.message.reply_text(w)

        await update.message.reply_text(
            "⏳ Analyzing with LLM...\n\n" + "\n".join(status_parts)
        )

        # Run LLM analysis
        result = await loop.run_in_executor(
            None,
            partial(
                analyze_article,
                extraction.content,
                article_link=url,
                images=extraction.images if extraction.images else None,
            ),
        )

        # Format and send
        lines = [f"📰 *Phân tích bổ sung*\n🔗 {url}\n"]

        if result.stage_1_output:
            lines.append(result.stage_1_output)
        if result.stage_2_output:
            lines.append("\n" + result.stage_2_output)
        if result.warning:
            lines.append("\n⚠️ " + result.warning)

        output_text = "\n".join(lines)

        MAX_LEN = 4096
        if len(output_text) <= MAX_LEN:
            await update.message.reply_text(output_text)
        else:
            chunks = []
            current = ""
            for line in output_text.split("\n"):
                if len(current) + len(line) + 1 > MAX_LEN:
                    if current:
                        chunks.append(current)
                    current = line
                else:
                    current = current + "\n" + line if current else line
            if current:
                chunks.append(current)
            for chunk in chunks:
                await update.message.reply_text(chunk)

        logger.info(f"URL analysis sent: {url}, {len(output_text)} chars")

    except Exception as e:
        logger.error(f"Error in URL handler: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Phân tích thất bại: {e}")


# ═══════════════════════════════════════════════════════════════════
#  BATCH OVERVIEW
# ═══════════════════════════════════════════════════════════════════

async def overview_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /overview [n] — batch overview N queued articles."""
    import asyncio
    from functools import partial
    from services.digest import create_batch_digest

    db_path = str(config.DATABASE_PATH)

    # Parse count argument
    n = 5  # default
    if context.args:
        try:
            n = int(context.args[0])
            if n < 2 or n > 10:
                await update.message.reply_text("⚠️ Số bài phải từ 2-10. Mặc định: 5")
                n = max(2, min(n, 10))
        except ValueError:
            await update.message.reply_text("⚠️ Số bài phải là số. Ví dụ: /overview 5")
            return

    await update.message.reply_text(f"⏳ Đang tạo overview cho {n} bài queued cũ nhất...")

    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None,
            partial(create_batch_digest, db_path, n=n),
        )

        if not result.success:
            await update.message.reply_text(f"❌ {result.error}")
            return

        # Build output message
        lines = [
            f"📚 *Batch Overview — {result.articles_processed} bài*\n",
        ]

        if result.articles_skipped > 0:
            lines.append(f"⚠️ Skipped {result.articles_skipped} bài: {', '.join(result.skipped_titles)}\n")

        lines.append(result.output)

        # Deep-dive suggestions with ID + title
        lines.append("\n\n🔬 *Deep-dive:*")
        for aid in result.article_ids:
            title = result.article_titles.get(aid, "")
            short_title = title[:60] + "..." if len(title) > 60 else title
            lines.append(f"→ /analyze {aid} — {short_title}")

        output_text = "\n".join(lines)

        # Send (split if needed, with Markdown fallback)
        MAX_LEN = 4096
        chunks = []
        if len(output_text) <= MAX_LEN:
            chunks = [output_text]
        else:
            current = ""
            for line in output_text.split("\n"):
                if len(current) + len(line) + 1 > MAX_LEN:
                    if current:
                        chunks.append(current)
                    current = line
                else:
                    current = current + "\n" + line if current else line
            if current:
                chunks.append(current)

        for chunk in chunks:
            try:
                await update.message.reply_text(chunk, parse_mode="Markdown")
            except Exception:
                # Fallback: send without Markdown if parse fails
                await update.message.reply_text(chunk)

        logger.info(f"Overview sent: {result.articles_processed} articles, {len(output_text)} chars")

    except Exception as e:
        logger.error(f"Error in /overview: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Overview thất bại: {e}")


# ── WEEKLY SYNTHESIS ───────────────────────────────────────────────


async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /weekly — generate weekly synthesis report."""
    import asyncio
    from functools import partial
    from services.synthesizer import create_weekly_synthesis

    db_path = str(config.DATABASE_PATH)

    await update.message.reply_text("⏳ Đang tạo weekly synthesis...")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, partial(create_weekly_synthesis, db_path)
        )

        if result.error:
            await update.message.reply_text(f"⚠️ {result.error}")
            return

        # Build output
        lines = [
            f"📊 *Weekly Synthesis* ({result.week_start})\n",
            f"📚 Articles: {result.articles_count}"
            f" | 💭 Reflections: {result.reflections_count}"
            f" | ⏱️ {result.total_session_minutes} phút",
        ]
        if result.avg_confidence > 0:
            lines.append(f"📈 Avg confidence: {result.avg_confidence:.1f}/10")
        lines.append("")
        lines.append(result.output)

        output_text = "\n".join(lines)

        # Send with Markdown fallback
        MAX_LEN = 4096
        chunks = []
        if len(output_text) <= MAX_LEN:
            chunks = [output_text]
        else:
            current = ""
            for line in output_text.split("\n"):
                if len(current) + len(line) + 1 > MAX_LEN:
                    if current:
                        chunks.append(current)
                    current = line
                else:
                    current = current + "\n" + line if current else line
            if current:
                chunks.append(current)

        for chunk in chunks:
            try:
                await update.message.reply_text(chunk, parse_mode="Markdown")
            except Exception:
                await update.message.reply_text(chunk)

        logger.info(f"Weekly synthesis sent: {result.articles_count} articles, {result.reflections_count} reflections")

    except Exception as e:
        logger.error(f"Error in /weekly: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Weekly synthesis thất bại: {e}")


# ═══════════════════════════════════════════════════════════════════
#  STREAK CALCULATION
# ═══════════════════════════════════════════════════════════════════

def calculate_streak(db_path: str) -> int:
    """Calculate consecutive days with at least one reflection, counting from today."""
    reflections = get_recent_reflections(db_path, days=60)
    if not reflections:
        return 0

    # Get unique dates with reflections
    reflection_dates = set()
    for r in reflections:
        created = r.get("created_at", "")
        if created:
            try:
                dt = datetime.fromisoformat(created)
                reflection_dates.add(dt.date())
            except (ValueError, TypeError):
                pass

    if not reflection_dates:
        return 0

    # Count consecutive days backwards from today
    today = date.today()
    streak = 0
    check_date = today

    while check_date in reflection_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return streak


# ═══════════════════════════════════════════════════════════════════
#  REFLECTION CONVERSATION HANDLER
# ═══════════════════════════════════════════════════════════════════

async def reflect_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for /reflect [id] — start reflection flow."""
    db_path = str(config.DATABASE_PATH)

    # Check if user provided an article ID
    if context.args:
        try:
            article_id = int(context.args[0])
            article = get_article_by_id(db_path, article_id)
            if not article:
                await update.message.reply_text(
                    f"❌ Không tìm thấy article #{article_id}"
                )
                return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("❌ ID phải là số. Ví dụ: /reflect 42")
            return ConversationHandler.END
    else:
        # Find last sent article
        sent_articles = get_articles_by_status(db_path, "sent")
        if not sent_articles:
            await update.message.reply_text(
                "📭 Không có bài nào đã gửi để reflect.\n"
                "→ Dùng /analyze để phân tích bài trước."
            )
            return ConversationHandler.END
        # Get the most recent one (last in list by ID)
        article = max(sent_articles, key=lambda a: a.get("id", 0))

    article_id = article.get("id")
    title = article.get("title", "Untitled")

    # Store article info for later steps
    context.user_data["reflect_article_id"] = article_id
    context.user_data["reflect_title"] = title

    await update.message.reply_text(
        f"💭 *Reflection — #{article_id}*\n\n"
        f"📰 _{title[:80]}_\n\n"
        f"*Bước 1/3:* Insight chính của bạn từ bài này là gì?",
        parse_mode="Markdown",
    )
    return INSIGHT


async def reflect_insight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 1 — receive insight, ask for action item."""
    context.user_data["reflect_insight"] = update.message.text

    await update.message.reply_text(
        "*Bước 2/3:* Action item — bạn sẽ làm gì với kiến thức này?",
        parse_mode="Markdown",
    )
    return ACTION


async def reflect_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 2 — receive action, ask for confidence."""
    context.user_data["reflect_action"] = update.message.text

    await update.message.reply_text(
        "*Bước 3/3:* Confidence — bạn hiểu bài này ở mức nào?\n"
        "_(Nhập số từ 1-10, 1 = chưa hiểu, 10 = hiểu rõ)_",
        parse_mode="Markdown",
    )
    return CONFIDENCE


async def reflect_confidence(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 3 — receive confidence score, save reflection, show streak."""
    text = update.message.text.strip()

    # Validate confidence score
    try:
        score = int(text)
        if score < 1 or score > 10:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "⚠️ Vui lòng nhập số từ *1-10*.",
            parse_mode="Markdown",
        )
        return CONFIDENCE  # Ask again

    db_path = str(config.DATABASE_PATH)
    article_id = context.user_data.get("reflect_article_id")
    title = context.user_data.get("reflect_title", "")
    insight = context.user_data.get("reflect_insight", "")
    action = context.user_data.get("reflect_action", "")

    # Save reflection
    try:
        add_reflection(
            db_path,
            article_id=article_id,
            reflection_text=insight,
            action_item=action,
            confidence_score=score,
        )
        # Update article status
        update_article_status(db_path, article_id, "reflected")

        # Calculate streak
        streak = calculate_streak(db_path)

        await update.message.reply_text(
            f"✅ *Reflection saved!*\n\n"
            f"📰 #{article_id}: {title[:60]}\n"
            f"💡 Insight: {insight[:100]}{'...' if len(insight) > 100 else ''}\n"
            f"🎯 Action: {action[:100]}{'...' if len(action) > 100 else ''}\n"
            f"📊 Confidence: {score}/10\n\n"
            f"🔥 Streak: {streak} ngày liên tiếp!",
            parse_mode="Markdown",
        )

    except Exception as e:
        logger.error(f"Error saving reflection: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Lỗi khi lưu reflection: {e}")

    # Clean up user_data
    for key in ["reflect_article_id", "reflect_title", "reflect_insight", "reflect_action"]:
        context.user_data.pop(key, None)

    return ConversationHandler.END


async def reflect_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the reflection flow."""
    # Clean up user_data
    for key in ["reflect_article_id", "reflect_title", "reflect_insight", "reflect_action"]:
        context.user_data.pop(key, None)

    await update.message.reply_text("❌ Reflection đã hủy.")
    return ConversationHandler.END


# ═══════════════════════════════════════════════════════════════════
#  SESSION TRACKING
# ═══════════════════════════════════════════════════════════════════

async def session_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /session [start|stop] — track learning sessions."""
    db_path = str(config.DATABASE_PATH)
    args = context.args

    if not args:
        # Show current session status
        session_start = context.user_data.get("session_start")
        if session_start:
            elapsed = datetime.now() - session_start
            minutes = int(elapsed.total_seconds() / 60)
            await update.message.reply_text(
                f"⏱️ Session đang chạy: {minutes} phút\n"
                f"→ /session stop để kết thúc"
            )
        else:
            # Show today's total
            today_str = date.today().isoformat()
            sessions = get_sessions_by_date(db_path, today_str)
            total_min = sum(s["duration_minutes"] for s in sessions) if sessions else 0
            count = len(sessions) if sessions else 0
            await update.message.reply_text(
                f"📊 Hôm nay: {count} session, {total_min} phút\n"
                f"→ /session start để bắt đầu"
            )
        return

    action = args[0].lower()

    if action == "start":
        if context.user_data.get("session_start"):
            elapsed = datetime.now() - context.user_data["session_start"]
            minutes = int(elapsed.total_seconds() / 60)
            await update.message.reply_text(
                f"⚠️ Session đang chạy ({minutes} phút)!\n"
                f"→ /session stop để kết thúc trước"
            )
            return

        context.user_data["session_start"] = datetime.now()
        await update.message.reply_text("⏱️ Session bắt đầu! Chúc bạn học tốt 📚")

    elif action == "stop":
        session_start = context.user_data.get("session_start")
        if not session_start:
            await update.message.reply_text(
                "⚠️ Chưa có session nào đang chạy.\n"
                "→ /session start để bắt đầu"
            )
            return

        end_time = datetime.now()
        duration = end_time - session_start
        duration_minutes = max(1, int(duration.total_seconds() / 60))

        # Save to DB
        try:
            add_session(
                db_path,
                date=date.today().isoformat(),
                start_time=session_start.strftime("%H:%M"),
                end_time=end_time.strftime("%H:%M"),
                duration_minutes=duration_minutes,
                activity_type="reflection",
            )

            # Get today's total
            today_sessions = get_sessions_by_date(db_path, date.today().isoformat())
            total_min = sum(s["duration_minutes"] for s in today_sessions) if today_sessions else 0

            await update.message.reply_text(
                f"✅ Session kết thúc!\n\n"
                f"⏱️ Thời gian: {duration_minutes} phút\n"
                f"📊 Tổng hôm nay: {total_min} phút"
            )

        except Exception as e:
            logger.error(f"Error saving session: {e}", exc_info=True)
            await update.message.reply_text(f"❌ Lỗi khi lưu session: {e}")

        # Clean up
        context.user_data.pop("session_start", None)

    else:
        await update.message.reply_text(
            "Usage: /session start | /session stop | /session"
        )


# ═══════════════════════════════════════════════════════════════════
#  ERROR HANDLER
# ═══════════════════════════════════════════════════════════════════

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and continue running."""
    logger.error(f"Update {update} caused error: {context.error}")


# ═══════════════════════════════════════════════════════════════════
#  APPLICATION BUILDER
# ═══════════════════════════════════════════════════════════════════

async def _post_init(app: Application) -> None:
    """Called after Application.initialize() — start scheduler on the event loop."""
    from services.scheduler import init_scheduler
    init_scheduler(app.bot)
    logger.info("Scheduler initialized via post_init")


def build_application(token: str) -> Application:
    """
    Build the Telegram Application with all handlers registered.

    Args:
        token: Telegram bot token

    Returns:
        Configured Application ready for run_polling()
    """
    app = Application.builder().token(token).post_init(_post_init).build()

    # Reflection ConversationHandler (must be before plain command handlers)
    reflect_handler = ConversationHandler(
        entry_points=[CommandHandler("reflect", reflect_command)],
        states={
            INSIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, reflect_insight)],
            ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, reflect_action)],
            CONFIDENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, reflect_confidence)],
        },
        fallbacks=[CommandHandler("cancel", reflect_cancel)],
        conversation_timeout=600,  # 10 minutes
    )
    app.add_handler(reflect_handler)

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("analyze", analyze_command))
    app.add_handler(CommandHandler("sync", sync_command))
    app.add_handler(CommandHandler("next", next_command))
    app.add_handler(CommandHandler("skip", skip_command))
    app.add_handler(CommandHandler("schedule", schedule_command))
    app.add_handler(CommandHandler("session", session_command))
    app.add_handler(CommandHandler("overview", overview_command))
    app.add_handler(CommandHandler("weekly", weekly_command))
    app.add_handler(CommandHandler("reset", reset_command))

    # URL message handler (user sends a URL → extract & analyze)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'https?://'),
        url_message_handler,
    ))

    # Unknown command handler (must be last)
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Error handler
    app.add_error_handler(error_handler)

    return app
