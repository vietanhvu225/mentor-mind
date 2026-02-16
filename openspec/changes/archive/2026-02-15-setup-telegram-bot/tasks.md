## 1. Project Setup

- [x] 1.1 Tạo `bot/__init__.py`
- [x] 1.2 Thêm `python-telegram-bot` vào `requirements.txt`
- [x] 1.3 Cài `python-telegram-bot` (`python -m pip install python-telegram-bot`)

> **Done khi:** `from telegram import Bot` import thành công.

## 2. Telegram Handler

- [x] 2.1 Tạo `bot/telegram_handler.py` với `/start` command handler — welcome message
- [x] 2.2 Implement `/help` command handler — danh sách commands
- [x] 2.3 Implement `/status` command handler — đọc `count_articles_by_status()` từ DB
- [x] 2.4 Implement `send_message(bot, chat_id, text)` helper — gửi Markdown message với error handling
- [x] 2.5 Implement error handler — log errors, không crash
- [x] 2.6 Implement `build_application(token)` — tạo Application + register handlers

> **Done khi:** Tất cả handlers và send_message function hoạt động.

## 3. Entry Point

- [x] 3.1 Tạo `main.py` — import config, init_db(), build_application(), run_polling()
- [x] 3.2 Validate token trước khi start — exit gracefully nếu thiếu
- [x] 3.3 Add logging setup (basic console logging)

> **Done khi:** `python main.py` khởi động bot thành công.

## 4. Testing & Verification

- [x] 4.1 Test import: `python -c "from bot.telegram_handler import build_application"`
- [x] 4.2 Test syntax compilation: `python -m py_compile bot/telegram_handler.py`
- [x] 4.3 Test token validation: chạy `main.py` với token trống → verify log lỗi + exit
- [x] 4.4 Test với real token: /start, /help, /status commands hoạt động trên Telegram

> **Done khi:** Bot gửi được message trên Telegram.
