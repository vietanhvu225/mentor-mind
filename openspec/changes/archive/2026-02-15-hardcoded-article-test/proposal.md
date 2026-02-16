## Why

3 components đã sẵn sàng: LLM pipeline (`services/analyzer.py`), database (`db/`), Telegram bot (`bot/`). Cần kết nối chúng end-to-end với 1 article test cứng để verify toàn bộ flow hoạt động trước khi integrate Raindrop API. Đây là Definition of Done cho Phase 1A.

## What Changes

- Tạo `/analyze` command trong bot — trigger article analysis on-demand
- Tạo test article data (hardcoded text)
- Wire: hardcoded article → `analyze_article()` → format output → gửi Telegram → lưu SQLite
- Format output đúng 3 personas + synthesizer, tiếng Việt

## Capabilities

### New Capabilities
- `article-flow`: End-to-end flow kết nối article → LLM analysis → Telegram output → database storage.

### Modified Capabilities
- `telegram-bot`: Thêm `/analyze` command cho on-demand article analysis.

## Không làm
- Raindrop integration (Phase 1B)
- Article extraction từ URL (Phase 1B)
- Scheduler tự động (Phase 1B)
- Message splitting (Phase 1B)

## Impact

- **New files:** `tests/test_article.py` (hardcoded article data)
- **Modified:** `bot/telegram_handler.py` (thêm `/analyze` command), `main.py` (minor)
- **Dependencies:** Cần Antigravity Tools proxy running tại localhost:8045
- **Runtime:** LLM calls tốn ~10-30 giây
