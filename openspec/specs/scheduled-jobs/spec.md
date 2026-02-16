## Purpose

Automated daily scheduling for syncing articles from Raindrop and running LLM analysis. Includes queue management commands (/next, /skip) and scheduler control (/schedule).

## Requirements

### Requirement: Daily Scheduled Sync & Analysis
Hệ thống MUST tự động sync và phân tích bài viết theo lịch hàng ngày.

#### Scenario: Scheduled job chạy đúng giờ
- **WHEN** đến giờ scheduled (default 8:00 AM)
- **THEN** hệ thống MUST tự động sync bài mới từ Raindrop
- **THEN** pick 1 bài queued → extract → analyze → gửi Telegram
- **THEN** update article status → 'sent'

#### Scenario: Sync không có bài mới
- **WHEN** scheduled job chạy nhưng Raindrop không có bài mới
- **THEN** vẫn pick 1 bài queued đã có → analyze → gửi

#### Scenario: Queue rỗng
- **WHEN** scheduled job chạy nhưng queue rỗng
- **THEN** gửi notification "📭 Queue trống — bookmark thêm bài trên Raindrop!"

#### Scenario: Job fail
- **WHEN** bất kỳ step nào trong job fail
- **THEN** gửi error notification → bot tiếp tục chạy → retry ngày mai

---

### Requirement: /next Command (Zero-cost Preview)
Hệ thống MUST cho phép user xem bài tiếp theo mà không tốn LLM tokens.

#### Scenario: Có bài trong queue
- **WHEN** user gửi `/next`
- **THEN** hiển thị title, excerpt, URL, content type của bài queued tiếp theo
- **THEN** KHÔNG extract content, KHÔNG gọi LLM

#### Scenario: Queue rỗng
- **WHEN** user gửi `/next` và queue rỗng
- **THEN** hiện "📭 Queue trống!"

---

### Requirement: /skip Command (Queue Management)
Hệ thống MUST cho phép user skip bài không muốn đọc.

#### Scenario: Skip bài hiện tại
- **WHEN** user gửi `/skip`
- **THEN** mark bài queued đầu tiên → status 'skipped'
- **THEN** hiển thị bài queued tiếp theo (như /next)

#### Scenario: Skip khi queue rỗng
- **WHEN** user gửi `/skip` và queue rỗng
- **THEN** hiện "📭 Không có bài nào để skip!"

---

### Requirement: /schedule Command
Hệ thống MUST cho phép user xem và thay đổi lịch scheduler.

#### Scenario: Xem lịch hiện tại
- **WHEN** user gửi `/schedule`
- **THEN** hiển thị: trạng thái (on/off), giờ chạy, next run time

#### Scenario: Đổi giờ
- **WHEN** user gửi `/schedule 9:30`
- **THEN** update cron job → giờ mới
- **THEN** confirm "⏰ Đã đổi lịch → 9:30 AM"

#### Scenario: Tắt/bật
- **WHEN** user gửi `/schedule off` hoặc `/schedule on`
- **THEN** pause/resume scheduler
- **THEN** confirm trạng thái mới
