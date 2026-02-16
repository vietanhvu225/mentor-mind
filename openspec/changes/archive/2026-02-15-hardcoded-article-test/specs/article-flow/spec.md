## ADDED Requirements

### Requirement: End-to-end article analysis flow
Hệ thống SHALL xử lý 1 article từ đầu đến cuối: analysis → format → gửi Telegram → lưu DB.

#### Scenario: Trigger analysis thành công
- **WHEN** user gửi `/analyze` trên Telegram
- **THEN** bot MUST lấy hardcoded article text
- **THEN** gọi `analyze_article()` với article text
- **THEN** format output thành Markdown message (3 personas + synthesizer)
- **THEN** gửi message đến user qua Telegram
- **THEN** lưu article + analysis output vào SQLite

#### Scenario: Analysis đang chạy — feedback
- **WHEN** user gửi `/analyze`
- **THEN** bot MUST gửi "Đang phân tích..." message ngay lập tức
- **THEN** gửi analysis result sau khi LLM trả về

#### Scenario: LLM failure — graceful degradation
- **WHEN** LLM proxy không available hoặc trả lỗi
- **THEN** bot MUST gửi error message cho user
- **THEN** bot MUST NOT crash

### Requirement: Output format tiếng Việt
Analysis output SHALL được format đúng theo persona structure.

#### Scenario: Format message
- **WHEN** analysis hoàn thành
- **THEN** output MUST chứa 4 sections: 🔬 Researcher, 🏗️ Architect, 🤔 Skeptic, 📝 Synthesizer
- **THEN** output MUST bằng tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh

## MODIFIED Requirements

### Requirement: Command handlers cơ bản
Bot SHALL respond đúng cách với các commands: /start, /help, /status, /analyze.

#### Scenario: /help command
- **WHEN** user gửi `/help`
- **THEN** bot MUST reply với danh sách commands bao gồm /analyze

#### Scenario: /analyze command
- **WHEN** user gửi `/analyze`
- **THEN** bot MUST trigger article analysis flow
