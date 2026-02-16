## ADDED Requirements

### Requirement: Batch Digest Command
Hệ thống MUST cho phép user gom nhiều bài queued thành 1 digest tóm tắt.

#### Scenario: Tạo digest với default 5 bài
- **WHEN** user gửi `/digest`
- **THEN** lấy 5 bài queued cũ nhất
- **THEN** extract content từng bài
- **THEN** gom content → 1 LLM call tạo digest
- **THEN** gửi digest output lên Telegram
- **THEN** lưu vào batch_digests table
- **THEN** update articles status → 'digest_reviewed'

#### Scenario: Tạo digest với số bài custom
- **WHEN** user gửi `/digest <n>` (n = 2-10)
- **THEN** lấy n bài queued cũ nhất và xử lý như trên

#### Scenario: Số bài queued ít hơn yêu cầu
- **WHEN** user gửi `/digest 5` nhưng chỉ có 3 bài queued
- **THEN** digest 3 bài có sẵn + thông báo "Chỉ có 3 bài trong queue"

#### Scenario: Queue rỗng
- **WHEN** user gửi `/digest` nhưng không có bài queued
- **THEN** thông báo "📭 Queue trống — dùng /sync để lấy bài mới"

#### Scenario: Extraction fail cho một số bài
- **WHEN** extract content fail cho 1+ bài trong batch
- **THEN** MUST skip bài fail, tiếp tục digest với bài còn lại
- **THEN** thông báo bài nào bị skip

#### Scenario: Deep-dive suggestion
- **WHEN** digest hoàn thành
- **THEN** message MUST include gợi ý `/analyze <id>` cho từng bài để deep-dive

---

### Requirement: Digest Prompt
Hệ thống MUST có prompt riêng cho batch digest, khác với analyze prompt.

#### Scenario: Digest prompt content
- **WHEN** LLM xử lý batch digest
- **THEN** prompt MUST yêu cầu: themes chung, so sánh giữa các bài, tóm tắt từng bài (ngắn gọn), gợi ý bài nên deep-dive

---

## MODIFIED Requirements

### Requirement: Command handlers cơ bản
Update `/help` command.

#### Scenario: /help command (updated)
- **WHEN** user gửi `/help`
- **THEN** danh sách commands MUST bao gồm `/digest`
