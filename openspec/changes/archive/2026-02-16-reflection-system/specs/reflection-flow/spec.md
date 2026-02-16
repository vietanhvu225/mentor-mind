## ADDED Requirements

### Requirement: Reflection Flow (3-step ConversationHandler)
Hệ thống MUST cho phép user reflect sau khi đọc article qua conversation flow 3 bước.

#### Scenario: Bắt đầu reflection cho bài gần nhất
- **WHEN** user gửi `/reflect`
- **THEN** bot MUST tìm article gần nhất có status 'sent'
- **THEN** bot MUST hiển thị title + hỏi "Insight chính của bạn là gì?"

#### Scenario: Reflect bài cụ thể
- **WHEN** user gửi `/reflect <id>`
- **THEN** bot MUST tìm article theo ID
- **THEN** nếu tồn tại → bắt đầu reflection flow cho bài đó
- **THEN** nếu không tồn tại → thông báo lỗi

#### Scenario: Step 1 — Insight
- **WHEN** user trả lời insight
- **THEN** bot MUST lưu tạm response và hỏi "Action item bạn sẽ làm?"

#### Scenario: Step 2 — Action item
- **WHEN** user trả lời action item
- **THEN** bot MUST lưu tạm response và hỏi "Confidence (1-10)?"

#### Scenario: Step 3 — Confidence score
- **WHEN** user trả lời con số 1-10
- **THEN** bot MUST lưu reflection vào DB (reflections table)
- **THEN** bot MUST update article status → 'reflected'
- **THEN** bot MUST hiển thị confirmation + current streak

#### Scenario: Invalid confidence score
- **WHEN** user trả lời không phải số 1-10
- **THEN** bot MUST hỏi lại "Vui lòng nhập số từ 1-10"

#### Scenario: Cancel reflection
- **WHEN** user gửi `/cancel` trong bất kỳ step nào
- **THEN** bot MUST hủy flow và thông báo

#### Scenario: Timeout
- **WHEN** user không trả lời trong 10 phút
- **THEN** conversation MUST tự hủy

#### Scenario: Không có bài để reflect
- **WHEN** user gửi `/reflect` nhưng không có bài status 'sent'
- **THEN** bot MUST thông báo và suggest `/analyze`

---

### Requirement: Streak Tracking
Hệ thống MUST tính và hiển thị streak (số ngày liên tiếp có reflect).

#### Scenario: Tính streak
- **WHEN** cần hiển thị streak
- **THEN** query reflections grouped by date (last 60 days)
- **THEN** đếm consecutive days tính từ hôm nay

#### Scenario: Hiển thị streak sau reflection
- **WHEN** user hoàn thành reflection
- **THEN** confirmation message MUST include current streak (e.g. "🔥 Streak: 5 ngày")

---

### Requirement: Session Tracking
Hệ thống MUST cho phép user track thời gian học.

#### Scenario: Bắt đầu session
- **WHEN** user gửi `/session start`
- **THEN** ghi nhận start_time
- **THEN** confirm "⏱️ Session bắt đầu!"

#### Scenario: Kết thúc session
- **WHEN** user gửi `/session stop`
- **THEN** tính duration = now - start_time
- **THEN** insert vào sessions table
- **THEN** hiển thị duration + tổng thời gian học hôm nay

#### Scenario: Session đang chạy
- **WHEN** user gửi `/session start` khi đã có session đang chạy
- **THEN** thông báo "Session đang chạy — dùng /session stop để kết thúc"

#### Scenario: Stop khi chưa start
- **WHEN** user gửi `/session stop` khi không có session đang chạy
- **THEN** thông báo "Chưa có session nào — dùng /session start"

---

## MODIFIED Requirements

### Requirement: Command handlers cơ bản
Update `/status` và `/help` commands.

#### Scenario: /status command (updated)
- **WHEN** user gửi `/status`
- **THEN** bot MUST reply với:
  - Thống kê articles theo status (queued/sent/reflected)
  - 🔥 Current streak
  - 💭 Total reflections
  - ⏱️ Thời gian học hôm nay

#### Scenario: /help command (updated)
- **WHEN** user gửi `/help`
- **THEN** danh sách commands MUST bao gồm `/reflect`, `/session`
