## Context

Hệ thống cần Telegram bot làm interface chính để tương tác với user. LLM pipeline và database đã sẵn sàng — cần bot để kết nối user với pipeline. Dùng `python-telegram-bot` (v21+, async-native).

Existing code: `config.py` (đã có TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID), `db/` package, `services/` package.

## Goals / Non-Goals

**Goals:**
- Bot chạy được, nhận commands, gửi messages
- Entry point `main.py` khởi tạo DB + bot
- Basic commands: /start, /help, /status
- Proactive message sending function (cho scheduler dùng sau)
- Graceful error handling

**Non-Goals:**
- ConversationHandler (Phase 2)
- APScheduler integration (Phase 1B)
- /next command (Phase 1B — cần Raindrop)
- Message splitting (Phase 1B)
- Webhook mode (dùng polling cho local hosting)

## Decisions

### 1. python-telegram-bot v21+ (async)

**Chọn:** `python-telegram-bot` v21+ (official, async-native)
**Không chọn:** Telethon, aiogram, raw HTTP

**Rationale:** Official library, well-maintained, async-native từ v20+. ConversationHandler built-in sẽ cần cho Phase 2.

### 2. Polling mode

**Chọn:** Long polling
**Không chọn:** Webhook

**Rationale:** Local hosting (PC chạy bot khi bật). Webhook cần public URL + SSL — không phù hợp.

### 3. send_message helper function

**Chọn:** Standalone `send_message(bot, chat_id, text)` function
**Rationale:** Các services khác (scheduler, analyzer) sẽ gọi function này để gửi message chủ động. Tách logic gửi message ra khỏi handler.

### 4. main.py structure

**Chọn:** Minimal entry point — init_db() → build Application → run_polling()
**Rationale:** Đơn giản, dễ thêm scheduler sau. Không dùng class-based app.

## Data Flow

```
User (Telegram)
    │
    ▼
bot/telegram_handler.py  ← command handlers + send_message()
    │
    ├── /status → db/repository.py → count_articles_by_status()
    │
    └── send_message() ← called by services later
    
main.py
    │
    ├── init_db()
    └── Application.run_polling()
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Token bị lộ | `.env` + `.gitignore` đã có |
| Bot crash khi API error | Error handler wrapper, log + continue |
| Async complexity | python-telegram-bot v21 handles event loop internally |
