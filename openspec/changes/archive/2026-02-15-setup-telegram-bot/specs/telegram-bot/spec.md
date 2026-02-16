## ADDED Requirements

### Requirement: Bot khởi tạo và kết nối Telegram
Bot SHALL kết nối Telegram API thông qua `python-telegram-bot` library và sẵn sàng nhận commands.

#### Scenario: Bot khởi động thành công
- **WHEN** `main.py` được chạy với `TELEGRAM_BOT_TOKEN` hợp lệ trong `.env`
- **THEN** bot MUST kết nối Telegram API và bắt đầu polling
- **THEN** bot MUST gọi `init_db()` trước khi bắt đầu polling

#### Scenario: Thiếu token
- **WHEN** `TELEGRAM_BOT_TOKEN` trống hoặc không được set
- **THEN** bot MUST log lỗi rõ ràng và exit gracefully

### Requirement: Command handlers cơ bản
Bot SHALL respond đúng cách với các commands: /start, /help, /status.

#### Scenario: /start command
- **WHEN** user gửi `/start`
- **THEN** bot MUST reply với welcome message giới thiệu chức năng

#### Scenario: /help command
- **WHEN** user gửi `/help`
- **THEN** bot MUST reply với danh sách commands có sẵn và mô tả ngắn

#### Scenario: /status command
- **WHEN** user gửi `/status`
- **THEN** bot MUST reply với thống kê: số articles theo status (queued/sent/reflected)

### Requirement: Gửi message đến user
Bot SHALL có khả năng gửi message chủ động đến user qua `TELEGRAM_CHAT_ID`.

#### Scenario: Gửi analysis result
- **WHEN** hệ thống cần gửi article analysis cho user
- **THEN** bot MUST gửi message đến `TELEGRAM_CHAT_ID` với format Markdown
- **THEN** message MUST được gửi thành công hoặc log lỗi

#### Scenario: Chat ID không hợp lệ
- **WHEN** `TELEGRAM_CHAT_ID` trống hoặc sai
- **THEN** bot MUST log warning nhưng MUST NOT crash

### Requirement: Error handling
Bot SHALL xử lý lỗi gracefully và không bị crash.

#### Scenario: Telegram API error
- **WHEN** Telegram API trả lỗi (network, rate limit, etc.)
- **THEN** bot MUST log error và tiếp tục chạy
- **THEN** bot MUST NOT crash hoặc stop polling

#### Scenario: Unknown command
- **WHEN** user gửi command không được recognize
- **THEN** bot SHOULD reply với gợi ý dùng /help
