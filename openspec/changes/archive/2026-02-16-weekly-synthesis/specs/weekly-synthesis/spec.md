## ADDED Requirements

### Requirement: Weekly Synthesis Report
Hệ thống MUST tạo weekly synthesis tổng hợp hoạt động học tập trong tuần.

#### Scenario: /weekly command
- **WHEN** user gửi `/weekly`
- **THEN** thu thập data 7 ngày qua (articles, reflections, sessions)
- **THEN** LLM tạo weekly synthesis report
- **THEN** gửi report lên Telegram
- **THEN** lưu vào weekly_reports table

#### Scenario: Tuần không có hoạt động
- **WHEN** user gửi `/weekly` nhưng không có articles/reflections trong tuần
- **THEN** thông báo "Tuần này chưa có hoạt động học tập"

#### Scenario: Scheduled Sunday report
- **WHEN** đến 23:00 Chủ nhật
- **THEN** tự động tạo + gửi weekly synthesis

---

### Requirement: Weekly Synthesis Content
Report MUST bao gồm các phần sau.

#### Scenario: Report content structure
- **WHEN** weekly synthesis được tạo
- **THEN** MUST bao gồm: tóm tắt tuần, themes phát hiện, knowledge gaps, gợi ý tuần tới
- **THEN** MUST hiện stats: số bài analyzed, số reflections, tổng session time, avg confidence

## MODIFIED Requirements

### Requirement: Command handlers cơ bản
Update `/help` command.

#### Scenario: /help command (updated)
- **WHEN** user gửi `/help`
- **THEN** danh sách commands MUST bao gồm `/weekly`
