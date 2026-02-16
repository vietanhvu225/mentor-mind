## ADDED Requirements

### Requirement: LLM Client kết nối qua Antigravity Tools Proxy
Hệ thống SHALL cung cấp một LLM client duy nhất sử dụng OpenAI SDK, kết nối đến Antigravity Tools proxy tại `http://127.0.0.1:8045/v1`. Tất cả LLM calls (Gemini, Claude, GPT) MUST đi qua proxy endpoint này.

#### Scenario: Client khởi tạo thành công
- **WHEN** bot khởi động và load config
- **THEN** LLM client MUST được tạo với `base_url` từ env `ANTIGRAVITY_BASE_URL` (default: `http://127.0.0.1:8045/v1`) và `api_key` từ env `ANTIGRAVITY_API_KEY` (default: `sk-antigravity`)

#### Scenario: Proxy không chạy khi bot khởi động
- **WHEN** bot khởi động nhưng không connect được đến proxy endpoint
- **THEN** hệ thống MUST log warning nhưng vẫn khởi động (proxy có thể start sau)

#### Scenario: Proxy down giữa chừng
- **WHEN** LLM call fail do proxy unreachable (ConnectionError)
- **THEN** hệ thống MUST retry sau 5 giây, tối đa 2 lần, trước khi báo lỗi

---

### Requirement: 2-Stage Pipeline cho Daily Analysis
Hệ thống SHALL thực hiện phân tích bài viết qua 2 LLM calls tuần tự. Stage 1 tạo phân tích từ 3 personas, Stage 2 tổng hợp và tạo action plan.

#### Scenario: Phân tích bài viết thành công (happy path)
- **WHEN** hệ thống nhận bài viết cần phân tích
- **THEN** hệ thống MUST gọi Stage 1 với model `MODEL_STAGE_1` (default: `gemini-3-pro`) để tạo output 3 personas (Researcher, Architect, Skeptic)
- **THEN** hệ thống MUST gọi Stage 2 với model `MODEL_STAGE_2` (default: `claude-opus-4-6-thinking`) với input là output Stage 1, để tạo Synthesizer summary + Action Plan

#### Scenario: Stage 1 thành công, Stage 2 fail (graceful degradation)
- **WHEN** Stage 1 hoàn thành nhưng Stage 2 fail sau tất cả retries và fallbacks
- **THEN** hệ thống MUST vẫn gửi kết quả Stage 1 (3 personas) cho user qua Telegram
- **THEN** message MUST ghi chú rằng phần tổng hợp không khả dụng

#### Scenario: Stage 1 fail
- **WHEN** Stage 1 fail sau tất cả retries và fallbacks
- **THEN** hệ thống MUST gửi Telegram notification với link bài viết gốc
- **THEN** hệ thống MUST KHÔNG gọi Stage 2

---

### Requirement: Config-driven Model Assignment
Hệ thống SHALL cho phép cấu hình model cho từng task qua environment variables, không cần sửa code.

#### Scenario: Override model qua environment variable
- **WHEN** env `MODEL_STAGE_1` được set thành `gemini-3-flash`
- **THEN** Stage 1 MUST sử dụng model `gemini-3-flash` thay vì default `gemini-3-pro`

#### Scenario: Không có env override
- **WHEN** env `MODEL_STAGE_1` không được set
- **THEN** Stage 1 MUST sử dụng default model `gemini-3-pro`

#### Scenario: Config cho tất cả task types
- **WHEN** hệ thống load config
- **THEN** MUST có mapping cho ít nhất 4 task types: `stage_1_analysis`, `stage_2_planning`, `batch_digest`, `weekly_synthesis`

---

### Requirement: Model-level Fallback Chain
Hệ thống SHALL có fallback chain để thử model khác khi primary model fail. Đây là app-level fallback — proxy đã xử lý account-level retry/rotation.

#### Scenario: Primary model fail, fallback thành công
- **WHEN** primary model trả error sau proxy đã retry tất cả accounts
- **THEN** hệ thống MUST thử model tiếp theo trong `FALLBACK_CHAIN` (default: `["gemini-3-flash", "claude-sonnet-4-5"]`)

#### Scenario: Tất cả models trong fallback chain fail
- **WHEN** primary model VÀ tất cả fallback models đều fail
- **THEN** hệ thống MUST gửi error notification qua Telegram với message mô tả lỗi

#### Scenario: Fallback chain configurable
- **WHEN** env `FALLBACK_CHAIN` được set (comma-separated)
- **THEN** hệ thống MUST sử dụng danh sách models đó thay vì default

---

### Requirement: Prompt Files cho mỗi Stage
Hệ thống SHALL load prompt templates từ markdown files, tách biệt logic và nội dung prompt.

#### Scenario: Load prompt cho Stage 1
- **WHEN** Stage 1 được gọi
- **THEN** hệ thống MUST load system prompt từ `prompts/daily_analysis.md`
- **THEN** prompt MUST include nội dung của 3 persona files: `prompts/personas/researcher.md`, `prompts/personas/architect.md`, `prompts/personas/skeptic.md`

#### Scenario: Load prompt cho Stage 2
- **WHEN** Stage 2 được gọi
- **THEN** hệ thống MUST load system prompt từ `prompts/action_planning.md`
- **THEN** prompt MUST include nội dung của `prompts/personas/synthesizer.md`

#### Scenario: Prompt file missing
- **WHEN** prompt file không tồn tại tại expected path
- **THEN** hệ thống MUST raise lỗi rõ ràng (FileNotFoundError) chứ KHÔNG fallback về empty prompt

---

### Requirement: Antigravity Proxy Health Check
Hệ thống SHALL kiểm tra proxy availability trước khi thực hiện LLM calls quan trọng.

#### Scenario: Health check trước scheduled analysis
- **WHEN** scheduled job trigger phân tích bài viết
- **THEN** hệ thống SHOULD gọi proxy health endpoint trước
- **THEN** nếu proxy unreachable, MUST log warning và vẫn thử gọi LLM (proxy có thể recover nhanh)

#### Scenario: Health check endpoint
- **WHEN** hệ thống cần check proxy status
- **THEN** MUST gọi `GET http://127.0.0.1:8045/health` hoặc `GET http://127.0.0.1:8045/healthz`
- **THEN** response `{"status": "ok"}` = proxy healthy
