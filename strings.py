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
        "status_header": "📊 *Status*\n",
        "status_empty": "Chưa có articles nào trong hệ thống.",
        "status_total": "📚 Total: {total}",
        "status_streak": "\n🔥 Streak: {streak} ngày",
        "status_reflections": "💭 Reflections: {count}",
        "status_avg_conf": "📈 Avg confidence: {avg}/10",
        "status_session_today": "\n⏱️ Học hôm nay: {minutes} phút",
        "status_no_session": "\n⏱️ Chưa có session hôm nay",
        "status_error": "❌ Không thể lấy status. Check logs.",

        # ── Analyze ──────────────────────────────────────────
        "analyze_not_found": "❌ Không tìm thấy bài với ID={id}.",
        "analyze_queue_empty": "📭 Queue trống! Dùng /sync để lấy bài mới từ Raindrop.",
        "analyze_processing": (
            "⏳ Đang xử lý: *{title}*\n"
            "🆔 ID: {id}\n"
            "🔗 {url}\n\n"
            "Bước 1/3: Extracting content..."
        ),
        "analyze_step_llm": "Bước 2/3: Analyzing with LLM...\n\n",
        "analyze_no_content": "❌ Không extract được content. Dùng /analyze để thử bài khác.",
        "analyze_short_content": (
            "📎 Bài ngắn (Facebook preview). Nếu có link ở comment, "
            "gửi URL trực tiếp ở đây — mình sẽ extract & phân tích bổ sung."
        ),
        "analyze_github_repos": "🔗 *GitHub repos trong bài:*\n",
        "analyze_error_detail": (
            "❌ Phân tích thất bại: {error}\n\n"
            "Kiểm tra:\n• Antigravity proxy chạy chưa?\n• API key đúng chưa?"
        ),

        # ── Sync ─────────────────────────────────────────────
        "sync_start": "⏳ Đang sync Raindrop...",
        "sync_complete": (
            "✅ *Sync hoàn tất!*\n\n"
            "📥 Fetched: {fetched}\n"
            "🆕 Mới: {new}\n"
            "⏭️ Đã có: {skipped}"
        ),
        "sync_error": "❌ Sync thất bại: {error}",

        # ── Reset ────────────────────────────────────────────
        "reset_nothing": "✅ Không có bài nào cần reset — tất cả đã là 'queued'.",
        "reset_done": (
            "🔄 Reset xong!\n\n"
            "Trước: {before}\n"
            "Sau: tất cả {total} bài → queued\n\n"
            "Dùng /analyze để phân tích lại từ đầu."
        ),
        "reset_error": "❌ Reset thất bại: {error}",

        # ── Next / Skip ──────────────────────────────────────
        "queue_empty": "📭 Queue trống! Dùng /sync để lấy bài mới.",
        "skip_empty": "📭 Không có bài nào để skip!",
        "queue_empty_short": "📭 Queue trống!",
        "next_preview": (
            "📄 *Bài tiếp theo* (#{id})\n\n"
            "*{title}*\n\n"
            "{preview}\n\n"
            "🔗 {url}\n\n"
            "📊 Còn {queued} bài trong queue\n\n"
            "→ /analyze để phân tích | /skip để bỏ qua"
        ),
        "skip_done": "⏭️ Đã skip #{id}: {title}",
        "skip_next_preview": (
            "📄 *Bài tiếp:* #{id} — {title}\n"
            "📊 Còn {queued} bài\n"
            "→ /analyze | /skip | /next"
        ),

        # ── Schedule ─────────────────────────────────────────
        "scheduler_not_init": "⚠️ Scheduler chưa khởi tạo.",
        "schedule_status": (
            "⏰ *Scheduler Status*\n\n"
            "{icon} Trạng thái: {status}\n"
            "🕐 Giờ chạy: {time}\n"
            "🌏 Timezone: {tz}\n"
            "⏭️ Lần chạy tiếp: {next_run}\n\n"
            "Dùng: /schedule HH:MM | /schedule on | /schedule off"
        ),
        "scheduler_off": "🔴 Scheduler đã tắt.",
        "scheduler_off_error": "⚠️ Không thể tắt scheduler.",
        "scheduler_on": "🟢 Scheduler đã bật lại!",
        "scheduler_on_error": "⚠️ Không thể bật scheduler.",
        "schedule_rescheduled": "✅ Đã đổi lịch → {time}",
        "scheduler_reschedule_error": "⚠️ Không thể đổi lịch.",
        "schedule_format_error": "⚠️ Format sai. Dùng: /schedule HH:MM (VD: /schedule 9:30)",
        "schedule_usage": "⚠️ Dùng: /schedule | /schedule HH:MM | /schedule on | /schedule off",

        # ── Overview ─────────────────────────────────────────
        "overview_range_error": "⚠️ Số bài phải từ 2-10. Mặc định: 5",
        "overview_number_error": "⚠️ Số bài phải là số. Ví dụ: /overview 5",
        "overview_start": "⏳ Đang tạo overview cho {n} bài queued cũ nhất...",
        "overview_error": "❌ Overview thất bại: {error}",

        # ── Weekly ───────────────────────────────────────────
        "weekly_start": "⏳ Đang tạo weekly synthesis...",
        "weekly_header": "📊 *Weekly Synthesis* ({week_start})\n",
        "weekly_stats": "📚 Articles: {articles} | 💭 Reflections: {reflections} | ⏱️ {minutes} phút",
        "weekly_error": "❌ Weekly synthesis thất bại: {error}",

        # ── Reflect ──────────────────────────────────────────
        "reflect_not_found": "❌ Không tìm thấy article #{id}",
        "reflect_id_error": "❌ ID phải là số. Ví dụ: /reflect 42",
        "reflect_no_sent": (
            "📭 Không có bài nào đã gửi để reflect.\n"
            "→ Dùng /analyze để phân tích bài trước."
        ),
        "reflect_step1": (
            "💭 *Reflection — #{id}*\n\n"
            "📰 _{title}_\n\n"
            "*Bước 1/3:* Insight chính của bạn từ bài này là gì?"
        ),
        "reflect_step2": "*Bước 2/3:* Action item — bạn sẽ làm gì với kiến thức này?",
        "reflect_step3": (
            "*Bước 3/3:* Confidence — bạn hiểu bài này ở mức nào?\n"
            "_(Nhập số từ 1-10, 1 = chưa hiểu, 10 = hiểu rõ)_"
        ),
        "reflect_confidence_error": "⚠️ Vui lòng nhập số từ *1-10*.",
        "reflect_saved": (
            "✅ *Reflection saved!*\n\n"
            "📰 #{id}: {title}\n"
            "💡 Insight: {insight}\n"
            "🎯 Action: {action}\n"
            "📊 Confidence: {score}/10\n\n"
            "🔥 Streak: {streak} ngày liên tiếp!"
        ),
        "reflect_save_error": "❌ Lỗi khi lưu reflection: {error}",
        "reflect_cancelled": "❌ Reflection đã hủy.",

        # ── Session ──────────────────────────────────────────
        "session_running": "⏱️ Session đang chạy: {minutes} phút\n→ /session stop để kết thúc",
        "session_today": "📊 Hôm nay: {count} session, {minutes} phút\n→ /session start để bắt đầu",
        "session_already_running": "⚠️ Session đang chạy ({minutes} phút)!\n→ /session stop để kết thúc trước",
        "session_started": "⏱️ Session bắt đầu! Chúc bạn học tốt 📚",
        "session_no_active": "⚠️ Chưa có session nào đang chạy.\n→ /session start để bắt đầu",
        "session_stopped": "✅ Session kết thúc!\n\n⏱️ Thời gian: {duration} phút\n📊 Tổng hôm nay: {total} phút",
        "session_save_error": "❌ Lỗi khi lưu session: {error}",
        "session_usage": "Usage: /session start | /session stop | /session",

        # ── URL Handler ──────────────────────────────────────
        "url_extracting": "🔗 Đang extract content từ:\n{url}\n\n⏳ Extracting...",
        "url_no_content": "❌ Không extract được content từ URL này.",
        "url_analyzing": "⏳ Analyzing with LLM...\n\n",
        "url_supplementary": "📰 *Phân tích bổ sung*\n🔗 {url}\n",
        "url_error": "❌ Phân tích thất bại: {error}",

        # ── Unknown ──────────────────────────────────────────
        "unknown_command": "🤔 Không hiểu command này. Dùng /help để xem danh sách commands.",

        # ── Scheduler Jobs ───────────────────────────────────
        "daily_started": "⏰ Daily job started...",
        "daily_queue_empty": "📭 Daily Update\n\nQueue trống! Bookmark thêm bài trên Raindrop.",
        "daily_extract_fail": "⚠️ Daily job: không extract được content cho #{id}: {title}",
        "daily_analysis_header": "☀️ Daily Analysis — #{id}\n📰 {title}\n🔗 {url}\n",
        "daily_failed": "⚠️ Daily job failed\n\n{error}",
        "weekly_job_error": "⚠️ Weekly: {error}",
        "weekly_job_failed": "⚠️ Weekly job failed\n\n{error}",
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
        "status_header": "📊 *Status*\n",
        "status_empty": "No articles in the system yet.",
        "status_total": "📚 Total: {total}",
        "status_streak": "\n🔥 Streak: {streak} days",
        "status_reflections": "💭 Reflections: {count}",
        "status_avg_conf": "📈 Avg confidence: {avg}/10",
        "status_session_today": "\n⏱️ Studied today: {minutes} min",
        "status_no_session": "\n⏱️ No sessions today",
        "status_error": "❌ Cannot get status. Check logs.",

        # ── Analyze ──────────────────────────────────────────
        "analyze_not_found": "❌ Article with ID={id} not found.",
        "analyze_queue_empty": "📭 Queue empty! Use /sync to fetch new articles from Raindrop.",
        "analyze_processing": (
            "⏳ Processing: *{title}*\n"
            "🆔 ID: {id}\n"
            "🔗 {url}\n\n"
            "Step 1/3: Extracting content..."
        ),
        "analyze_step_llm": "Step 2/3: Analyzing with LLM...\n\n",
        "analyze_no_content": "❌ Cannot extract content. Use /analyze to try another article.",
        "analyze_short_content": (
            "📎 Short content (Facebook preview). If there's a link in comments, "
            "send the URL here — I'll extract & analyze it."
        ),
        "analyze_github_repos": "🔗 *GitHub repos in article:*\n",
        "analyze_error_detail": (
            "❌ Analysis failed: {error}\n\n"
            "Check:\n• Is proxy running?\n• Is API key correct?"
        ),

        # ── Sync ─────────────────────────────────────────────
        "sync_start": "⏳ Syncing Raindrop...",
        "sync_complete": (
            "✅ *Sync complete!*\n\n"
            "📥 Fetched: {fetched}\n"
            "🆕 New: {new}\n"
            "⏭️ Already exists: {skipped}"
        ),
        "sync_error": "❌ Sync failed: {error}",

        # ── Reset ────────────────────────────────────────────
        "reset_nothing": "✅ No articles to reset — all are already 'queued'.",
        "reset_done": (
            "🔄 Reset done!\n\n"
            "Before: {before}\n"
            "After: all {total} articles → queued\n\n"
            "Use /analyze to re-analyze."
        ),
        "reset_error": "❌ Reset failed: {error}",

        # ── Next / Skip ──────────────────────────────────────
        "queue_empty": "📭 Queue empty! Use /sync to fetch new articles.",
        "skip_empty": "📭 No articles to skip!",
        "queue_empty_short": "📭 Queue empty!",
        "next_preview": (
            "📄 *Next article* (#{id})\n\n"
            "*{title}*\n\n"
            "{preview}\n\n"
            "🔗 {url}\n\n"
            "📊 {queued} articles in queue\n\n"
            "→ /analyze to analyze | /skip to skip"
        ),
        "skip_done": "⏭️ Skipped #{id}: {title}",
        "skip_next_preview": (
            "📄 *Next:* #{id} — {title}\n"
            "📊 {queued} articles left\n"
            "→ /analyze | /skip | /next"
        ),

        # ── Schedule ─────────────────────────────────────────
        "scheduler_not_init": "⚠️ Scheduler not initialized.",
        "schedule_status": (
            "⏰ *Scheduler Status*\n\n"
            "{icon} Status: {status}\n"
            "🕐 Time: {time}\n"
            "🌏 Timezone: {tz}\n"
            "⏭️ Next run: {next_run}\n\n"
            "Usage: /schedule HH:MM | /schedule on | /schedule off"
        ),
        "scheduler_off": "🔴 Scheduler turned off.",
        "scheduler_off_error": "⚠️ Cannot turn off scheduler.",
        "scheduler_on": "🟢 Scheduler turned back on!",
        "scheduler_on_error": "⚠️ Cannot turn on scheduler.",
        "schedule_rescheduled": "✅ Rescheduled → {time}",
        "scheduler_reschedule_error": "⚠️ Cannot reschedule.",
        "schedule_format_error": "⚠️ Wrong format. Use: /schedule HH:MM (e.g. /schedule 9:30)",
        "schedule_usage": "⚠️ Usage: /schedule | /schedule HH:MM | /schedule on | /schedule off",

        # ── Overview ─────────────────────────────────────────
        "overview_range_error": "⚠️ Number of articles must be 2-10. Default: 5",
        "overview_number_error": "⚠️ Must be a number. Example: /overview 5",
        "overview_start": "⏳ Creating overview for {n} oldest queued articles...",
        "overview_error": "❌ Overview failed: {error}",

        # ── Weekly ───────────────────────────────────────────
        "weekly_start": "⏳ Creating weekly synthesis...",
        "weekly_header": "📊 *Weekly Synthesis* ({week_start})\n",
        "weekly_stats": "📚 Articles: {articles} | 💭 Reflections: {reflections} | ⏱️ {minutes} min",
        "weekly_error": "❌ Weekly synthesis failed: {error}",

        # ── Reflect ──────────────────────────────────────────
        "reflect_not_found": "❌ Article #{id} not found",
        "reflect_id_error": "❌ ID must be a number. Example: /reflect 42",
        "reflect_no_sent": (
            "📭 No analyzed articles to reflect on.\n"
            "→ Use /analyze first."
        ),
        "reflect_step1": (
            "💭 *Reflection — #{id}*\n\n"
            "📰 _{title}_\n\n"
            "*Step 1/3:* What's your key insight from this article?"
        ),
        "reflect_step2": "*Step 2/3:* Action item — what will you do with this knowledge?",
        "reflect_step3": (
            "*Step 3/3:* Confidence — how well do you understand this?\n"
            "_(Enter 1-10, 1 = not clear, 10 = fully understood)_"
        ),
        "reflect_confidence_error": "⚠️ Please enter a number from *1-10*.",
        "reflect_saved": (
            "✅ *Reflection saved!*\n\n"
            "📰 #{id}: {title}\n"
            "💡 Insight: {insight}\n"
            "🎯 Action: {action}\n"
            "📊 Confidence: {score}/10\n\n"
            "🔥 Streak: {streak} consecutive days!"
        ),
        "reflect_save_error": "❌ Error saving reflection: {error}",
        "reflect_cancelled": "❌ Reflection cancelled.",

        # ── Session ──────────────────────────────────────────
        "session_running": "⏱️ Session running: {minutes} min\n→ /session stop to end",
        "session_today": "📊 Today: {count} sessions, {minutes} min\n→ /session start to begin",
        "session_already_running": "⚠️ Session already running ({minutes} min)!\n→ /session stop to end first",
        "session_started": "⏱️ Session started! Happy learning 📚",
        "session_no_active": "⚠️ No active session.\n→ /session start to begin",
        "session_stopped": "✅ Session ended!\n\n⏱️ Duration: {duration} min\n📊 Total today: {total} min",
        "session_save_error": "❌ Error saving session: {error}",
        "session_usage": "Usage: /session start | /session stop | /session",

        # ── URL Handler ──────────────────────────────────────
        "url_extracting": "🔗 Extracting content from:\n{url}\n\n⏳ Extracting...",
        "url_no_content": "❌ Cannot extract content from this URL.",
        "url_analyzing": "⏳ Analyzing with LLM...\n\n",
        "url_supplementary": "📰 *Supplementary analysis*\n🔗 {url}\n",
        "url_error": "❌ Analysis failed: {error}",

        # ── Unknown ──────────────────────────────────────────
        "unknown_command": "🤔 Unknown command. Use /help to see available commands.",

        # ── Scheduler Jobs ───────────────────────────────────
        "daily_started": "⏰ Daily job started...",
        "daily_queue_empty": "📭 Daily Update\n\nQueue empty! Bookmark more articles on Raindrop.",
        "daily_extract_fail": "⚠️ Daily job: cannot extract content for #{id}: {title}",
        "daily_analysis_header": "☀️ Daily Analysis — #{id}\n📰 {title}\n🔗 {url}\n",
        "daily_failed": "⚠️ Daily job failed\n\n{error}",
        "weekly_job_error": "⚠️ Weekly: {error}",
        "weekly_job_failed": "⚠️ Weekly job failed\n\n{error}",
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
