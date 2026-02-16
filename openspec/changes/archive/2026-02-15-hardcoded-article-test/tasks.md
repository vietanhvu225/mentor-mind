## 1. Hardcoded Test Data

- [x] 1.1 Tạo `tests/test_article.py` với `SAMPLE_ARTICLE` — ~500 words về AI/LLM topic
- [x] 1.2 Include title, source_url, và raw_content

> **Done khi:** `from tests.test_article import SAMPLE_ARTICLE` thành công.

## 2. Analyze Command

- [x] 2.1 Thêm `async def analyze_command(update, context)` vào `bot/telegram_handler.py`
- [x] 2.2 Gửi "⏳ Đang phân tích..." feedback ngay lập tức
- [x] 2.3 Gọi `add_article()` để lưu article vào DB (status=queued)
- [x] 2.4 Gọi `analyze_article()` từ `services/analyzer.py`
- [x] 2.5 Gọi `update_article_analysis()` + `update_article_status("sent")` sau khi xong
- [x] 2.6 Format output Markdown (4 sections: Researcher, Architect, Skeptic, Synthesizer + Action Item)
- [x] 2.7 Gửi formatted output qua Telegram
- [x] 2.8 Handle error: gửi error message nếu LLM fail, không crash

> **Done khi:** `/analyze` command trigger full flow end-to-end.

## 3. Wiring

- [x] 3.1 Register `/analyze` handler trong `build_application()`
- [x] 3.2 Update `/help` message — thêm /analyze
- [x] 3.3 Tạo `tests/__init__.py`

> **Done khi:** Bot respond `/analyze` command.

## 4. End-to-End Test

- [x] 4.1 Start Antigravity Tools proxy (localhost:8045)
- [x] 4.2 Chạy `python main.py`
- [x] 4.3 Gửi `/analyze` trên Telegram → verify output đúng format
- [x] 4.4 Verify article trong SQLite (article saved with id=3, status=sent)
- [x] 4.5 Gửi `/start` → verify persona names updated

> **Done khi:** Article được phân tích, gửi Telegram, lưu DB thành công. Phase 1A complete!
