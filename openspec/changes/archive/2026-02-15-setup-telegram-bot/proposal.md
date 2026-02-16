## Why

Bot cần nhận message từ user và gửi analysis qua Telegram. Đây là interface chính của toàn bộ hệ thống — kết nối user với article analysis pipeline. Cần có trước khi test end-to-end ở change tiếp theo (`hardcoded-article-test`).

## What Changes

- Tạo `bot/telegram_handler.py` — Telegram bot với basic command handlers
- Tạo `main.py` — entry point, khởi tạo DB + bot
- Tạo `bot/__init__.py` — package init
- Cài `python-telegram-bot` dependency
- Update `requirements.txt`

## Capabilities

### New Capabilities
- `telegram-bot`: Telegram bot interface với command handlers (/start, /help, /status), message sending, và basic error handling.

### Modified Capabilities
- None

## Không làm
- ConversationHandler cho reflection (Phase 2)
- /next command (Phase 1B — cần Raindrop trước)
- APScheduler integration (Phase 1B)
- Message splitting cho long messages (Phase 1B)
- Inline keyboard (future enhancement)

## Impact

- **New files:** `main.py`, `bot/telegram_handler.py`, `bot/__init__.py`
- **Modified:** `requirements.txt` (thêm `python-telegram-bot`)
- **Dependencies:** `python-telegram-bot` (~21.x)
- **Requires:** `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID` trong `.env`
