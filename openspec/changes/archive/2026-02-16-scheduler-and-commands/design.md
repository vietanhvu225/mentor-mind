# Design: Scheduler & Commands

## Architecture Overview

```
main.py
  ├── init_db()
  ├── build_application(token)     ← register new handlers
  ├── init_scheduler(app.bot)      ← NEW: start APScheduler
  └── app.run_polling()

services/scheduler.py (NEW)
  ├── init_scheduler(bot)          ← create AsyncIOScheduler
  ├── daily_sync_and_analyze(bot)  ← job: sync → analyze → send
  └── get_scheduler_info()         ← status for /schedule command
```

## Design Decisions

### 1. APScheduler AsyncIO integration

APScheduler v3 `AsyncIOScheduler` chạy trên cùng event loop với python-telegram-bot. Không cần thread riêng.

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
scheduler.add_job(daily_job, CronTrigger(hour=8, minute=0), id="daily_sync")
scheduler.start()
```

**Tại sao AsyncIO**: python-telegram-bot v20+ dùng asyncio. `BackgroundScheduler` sẽ gọi coroutine từ thread khác → phức tạp. `AsyncIOScheduler` native asyncio → đơn giản.

### 2. Message splitting strategy

Telegram limit: **4096 chars/message**. Chiến lược split:

```python
MAX_MESSAGE_LENGTH = 4000  # safe margin

def split_message(text: str, max_len: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split text into chunks, preferring split at paragraph/line breaks."""
    if len(text) <= max_len:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        # Find split point: prefer \n\n > \n > space
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
```

**Split point priority**: `\n\n` (paragraph) → `\n` (line) → ` ` (space) → hard cut. Giữ Markdown formatting coherent.

### 3. /next command — zero-cost preview

```
/next → show title + excerpt + URL + type
        NO extraction, NO LLM call
        User quyết định: /analyze hoặc /skip
```

**Flow**: Query DB `WHERE status='queued' ORDER BY id LIMIT 1` → format message → send.

### 4. /skip command — queue management

```
/skip → mark current queued article as 'skipped'
        show next queued article preview
```

**Status flow**: `queued → skipped` (new status). User có thể dùng `/analyze <id>` để analyze lại bài đã skip.

### 5. /schedule command — scheduler control

```
/schedule           → show current schedule + next run time
/schedule 8:00      → change daily time to 8:00 AM
/schedule off       → disable scheduler
/schedule on        → enable scheduler
```

### 6. Config additions

```python
# config.py
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8"))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))
SCHEDULE_ENABLED = os.getenv("SCHEDULE_ENABLED", "true").lower() == "true"
```

### 7. Daily job flow

```
daily_sync_and_analyze(bot):
  1. sync_from_raindrop()     → get new articles
  2. pick queued article      → extract content
  3. analyze_article()        → LLM pipeline
  4. send results to chat     → with message splitting
  5. update article status    → 'sent'
  
  If any step fails → send error notification → continue tomorrow
```

## Risks / Trade-offs

- **APScheduler in-memory**: Jobs reset on restart → acceptable for personal bot
- **Timezone**: Dùng `Asia/Ho_Chi_Minh` từ config — quan trọng cho cron đúng giờ
- **Bot restart**: Scheduler mất state → job chạy lại lần tới theo cron
- **Message split + Markdown**: Split giữa markdown formatting block có thể break rendering → split ở paragraph boundaries giảm thiểu
