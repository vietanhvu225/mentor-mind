"""
Internationalization (i18n) — UI string translations.

Usage:
    from strings import t
    message = t("sync_start")
    message = t("analyze_start", id=42)
"""

import config


STRINGS = {
    "vi": {
        # ── Start / Help ─────────────────────────────────────
        "start_welcome": (
            "👋 *Chào\\!* Tôi là MentorMind của bạn\\.\n\n"
            "Dùng /help để xem danh sách commands\\."
        ),
        "help_text": (
            "📋 *Commands*\n\n"
            "📖 *Học tập*\n"
            "/analyze — Phân tích bài tiếp theo\n"
            "/analyze <id> — Phân tích lại bài theo ID\n"
            "/next — Xem bài tiếp theo (không phân tích)\n"
            "/skip — Bỏ qua bài tiếp theo\n"
            "/overview — Overview 5 bài queued cũ nhất\n"
            "/overview <n> — Overview n bài (2-10)\n"
            "/reflect — Reflect bài vừa đọc\n"
            "/reflect <id> — Reflect bài cụ thể\n"
            "/cancel — Hủy reflection đang làm\n"
            "/weekly — Tổng hợp tuần học tập\n\n"
            "⏱️ *Tracking*\n"
            "/session start — Bắt đầu session học\n"
            "/session stop — Kết thúc session\n"
            "/session — Xem session hiện tại\n"
            "/status — Thống kê + streak\n\n"
            "⚙️ *Quản lý*\n"
            "/sync — Sync bài mới từ Raindrop\n"
            "/schedule — Xem/đổi lịch tự động\n"
            "/reset — Reset status (dev)"
        ),

        # ── Status ───────────────────────────────────────────
        "status_error": "❌ Không thể lấy status. Check logs.",

        # ── Sync ─────────────────────────────────────────────
        "sync_start": "⏳ Đang sync Raindrop...",
        "sync_done": "✅ Đã sync {count} bài mới!",
        "sync_no_new": "📭 Không có bài mới.",
        "sync_error": "❌ Sync thất bại: {error}",

        # ── Reset ────────────────────────────────────────────
        "reset_error": "❌ Reset thất bại: {error}",

        # ── Next / Skip ──────────────────────────────────────
        "queue_empty": "📭 Queue trống! Dùng /sync để lấy bài mới.",
        "skip_empty": "📭 Không có bài nào để skip!",
        "queue_empty_short": "📭 Queue trống!",

        # ── Analyze ──────────────────────────────────────────
        "analyze_start": "🔍 Đang phân tích bài #{id}...",
        "analyze_error": "❌ Phân tích thất bại: {error}",

        # ── Overview ─────────────────────────────────────────
        "overview_range_error": "⚠️ Số bài phải từ 2-10. Mặc định: 5",
        "overview_number_error": "⚠️ Số bài phải là số. Ví dụ: /overview 5",
        "overview_start": "⏳ Đang tạo overview cho {n} bài queued cũ nhất...",
        "overview_error": "❌ Overview thất bại: {error}",

        # ── Weekly ───────────────────────────────────────────
        "weekly_start": "⏳ Đang tạo weekly synthesis...",
        "weekly_error": "❌ Weekly synthesis thất bại: {error}",

        # ── Reflect ──────────────────────────────────────────
        "reflect_id_error": "❌ ID phải là số. Ví dụ: /reflect 42",
        "reflect_save_error": "❌ Lỗi khi lưu reflection: {error}",
        "reflect_cancelled": "❌ Reflection đã hủy.",

        # ── Session ──────────────────────────────────────────
        "session_started": "⏱️ Session bắt đầu! Chúc bạn học tốt 📚",
        "session_save_error": "❌ Lỗi khi lưu session: {error}",

        # ── Scheduler ────────────────────────────────────────
        "scheduler_not_init": "⚠️ Scheduler chưa khởi tạo.",
        "scheduler_off": "🔴 Scheduler đã tắt.",
        "scheduler_off_error": "⚠️ Không thể tắt scheduler.",
        "scheduler_on": "🟢 Scheduler đã bật lại!",
        "scheduler_on_error": "⚠️ Không thể bật scheduler.",
        "scheduler_reschedule_error": "⚠️ Không thể đổi lịch.",
    },

    "en": {
        # ── Start / Help ─────────────────────────────────────
        "start_welcome": (
            "👋 *Hi\\!* I'm MentorMind\\.\n\n"
            "Use /help to see available commands\\."
        ),
        "help_text": (
            "📋 *Commands*\n\n"
            "📖 *Learning*\n"
            "/analyze — Analyze next article\n"
            "/analyze <id> — Analyze specific article by ID\n"
            "/next — Preview next article (no analysis)\n"
            "/skip — Skip next article\n"
            "/overview — Overview 5 oldest queued articles\n"
            "/overview <n> — Overview n articles (2-10)\n"
            "/reflect — Reflect on last read article\n"
            "/reflect <id> — Reflect on specific article\n"
            "/cancel — Cancel ongoing reflection\n"
            "/weekly — Weekly learning synthesis\n\n"
            "⏱️ *Tracking*\n"
            "/session start — Start learning session\n"
            "/session stop — End session\n"
            "/session — View current session\n"
            "/status — Stats + streak\n\n"
            "⚙️ *Management*\n"
            "/sync — Sync new articles from Raindrop\n"
            "/schedule — View/change auto schedule\n"
            "/reset — Reset status (dev)"
        ),

        # ── Status ───────────────────────────────────────────
        "status_error": "❌ Cannot get status. Check logs.",

        # ── Sync ─────────────────────────────────────────────
        "sync_start": "⏳ Syncing Raindrop...",
        "sync_done": "✅ Synced {count} new articles!",
        "sync_no_new": "📭 No new articles.",
        "sync_error": "❌ Sync failed: {error}",

        # ── Reset ────────────────────────────────────────────
        "reset_error": "❌ Reset failed: {error}",

        # ── Next / Skip ──────────────────────────────────────
        "queue_empty": "📭 Queue empty! Use /sync to fetch new articles.",
        "skip_empty": "📭 No articles to skip!",
        "queue_empty_short": "📭 Queue empty!",

        # ── Analyze ──────────────────────────────────────────
        "analyze_start": "🔍 Analyzing article #{id}...",
        "analyze_error": "❌ Analysis failed: {error}",

        # ── Overview ─────────────────────────────────────────
        "overview_range_error": "⚠️ Number of articles must be 2-10. Default: 5",
        "overview_number_error": "⚠️ Must be a number. Example: /overview 5",
        "overview_start": "⏳ Creating overview for {n} oldest queued articles...",
        "overview_error": "❌ Overview failed: {error}",

        # ── Weekly ───────────────────────────────────────────
        "weekly_start": "⏳ Creating weekly synthesis...",
        "weekly_error": "❌ Weekly synthesis failed: {error}",

        # ── Reflect ──────────────────────────────────────────
        "reflect_id_error": "❌ ID must be a number. Example: /reflect 42",
        "reflect_save_error": "❌ Error saving reflection: {error}",
        "reflect_cancelled": "❌ Reflection cancelled.",

        # ── Session ──────────────────────────────────────────
        "session_started": "⏱️ Session started! Happy learning 📚",
        "session_save_error": "❌ Error saving session: {error}",

        # ── Scheduler ────────────────────────────────────────
        "scheduler_not_init": "⚠️ Scheduler not initialized.",
        "scheduler_off": "🔴 Scheduler turned off.",
        "scheduler_off_error": "⚠️ Cannot turn off scheduler.",
        "scheduler_on": "🟢 Scheduler turned back on!",
        "scheduler_on_error": "⚠️ Cannot turn on scheduler.",
        "scheduler_reschedule_error": "⚠️ Cannot reschedule.",
    },
}


def t(key: str, **kwargs) -> str:
    """
    Translate a string key to the current locale.

    Args:
        key: String key from STRINGS dict.
        **kwargs: Format arguments for the string template.

    Returns:
        Translated string. Falls back to Vietnamese if key
        not found in current locale, then to the raw key.
    """
    lang = getattr(config, "LANGUAGE", "vi")
    locale_strings = STRINGS.get(lang, STRINGS["vi"])
    template = locale_strings.get(key)

    # Fallback to Vietnamese if not found in current locale
    if template is None:
        template = STRINGS["vi"].get(key, key)

    return template.format(**kwargs) if kwargs else template
