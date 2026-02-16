# Personal AI Learning Assistant — Agent Rules

> Tất cả implementations trong project này PHẢI tuân theo các rules dưới đây.
> File này là nguồn sự thật (source of truth) cho mọi quyết định kỹ thuật đã chốt.

## 🔴 Anti-Overengineering (MUST follow)

- Không vector DB trong 30 ngày đầu
- Không microservice
- Không dashboard web
- Không scoring hệ thống phức tạp
- Không quá 3 persona (Researcher, Architect, Skeptic) + 1 Synthesizer
- Không multi-model — chỉ 1 LLM model duy nhất
- Không agent framework
- Không FastAPI / web server

## 🔵 Tech Stack (Chốt — không thay đổi)

- **Python 3.11+**
- **python-telegram-bot** — dùng ConversationHandler cho multi-step flows
- **SQLite** — local file, không ORM phức tạp
- **APScheduler** — timezone-aware (`Asia/Ho_Chi_Minh`), multiple scheduled jobs
- **LLM** — 1 model mid-tier, 1 call duy nhất cho daily analysis
- **Article extraction** — trafilatura hoặc Jina Reader API
- **Config** — python-dotenv (`.env` file)

## 🟢 Output & Language Rules

- Output bằng **tiếng Việt**
- Thuật ngữ kỹ thuật giữ **tiếng Anh** (ví dụ: "token", "embedding", "RAG", "pipeline")
- Code comments bằng tiếng Anh
- Variable names, function names bằng tiếng Anh
- Prompt files viết bằng tiếng Việt (vì output cần tiếng Việt)

## 🔷 Code Style

- Dùng `logging` module, **KHÔNG** dùng `print()`
- API keys trong `.env`, **KHÔNG** hardcode
- Type hints: khuyến khích nhưng không bắt buộc
- Docstrings: chỉ cho public functions
- Vietnamese comments chấp nhận được
- Script-level code OK cho MVP — không cần over-abstract
- Mỗi file nên có 1 responsibility rõ ràng

## 🟡 Architecture Decisions (Đã chốt)

### LLM Call Strategy
- **1 LLM call duy nhất** cho daily article analysis (multi-section prompt)
- **1 LLM call riêng** cho weekly synthesis
- **1 LLM call riêng** cho batch digest (5 bài/digest)
- Tuyệt đối KHÔNG tạo multiple calls per article

### Reflection Flow
- **ConversationHandler** (Option B) — bot hỏi từng câu, 3 steps:
  1. `AWAITING_INSIGHT` — "Insight quan trọng nhất?"
  2. `AWAITING_ACTION` — "Bạn sẽ áp dụng gì?"
  3. `AWAITING_CONFIDENCE` — "Confidence (1-10)?"
- **Option C (Inline Keyboard)** lưu cho future enhancement — KHÔNG implement trong MVP

### Article Queue
- Scan **ALL** Raindrop collections
- Pick order: **bài mới nhất trước** (LIFO), trừ khi có `priority = 1`
- Status flow: `queued` → `sent` → `reflected`
- Backlog: `queued` → `digest_reviewed` (nếu qua batch digest)
- On-demand: sau mỗi reflection, bot hỏi muốn làm thêm không (`/next`)

### Streak Calculation
- **KHÔNG** dùng bảng riêng cho streak
- Tính dynamic bằng query từ `reflections.created_at`
- Đếm ngày liên tiếp gần nhất có reflection

### Prompt Structure (Hybrid)
```
prompts/
├── daily_analysis.md       # System prompt + output format template
├── weekly_synthesis.md     # Weekly report prompt
└── personas/
    ├── researcher.md       # Researcher instructions
    ├── architect.md        # Architect instructions
    ├── skeptic.md          # Skeptic instructions
    └── synthesizer.md      # Synthesizer instructions
```
- `daily_analysis.md` là template chứa system prompt + format
- Mỗi persona file chứa instructions riêng, được inject vào template khi build prompt
- Prompt files dùng format `.md`

## 🟠 Schema Rules

### Hai loại action_item — KHÔNG merge
- `articles.action_item` = AI đề xuất (từ synthesizer output)
- `reflections.action_item` = User tự chọn (từ reflection flow)

### Status field trên articles — BẮT BUỘC
- Mọi article PHẢI có status track lifecycle
- Values: `queued`, `sent`, `reflected`, `digest_reviewed`

### Tables (5 tables total)
1. `articles` — bài viết + LLM output
2. `reflections` — user reflection
3. `sessions` — commitment tracking (1h/ngày)
4. `batch_digests` — backlog digest output
5. `weekly_reports` — weekly synthesis output

## 🟣 Schedule Rules

- **Weekday**: Auto gửi 1 bài lúc 21:00 UTC+7 (PC on 20:00)
- **Thứ 7**: Auto gửi 1 bài lúc 12:30 UTC+7 (PC on 12:00)
- **Chủ nhật**: Auto gửi 1 bài lúc 20:30, Weekly Synthesis lúc 23:00 (PC on 20:00)
- Schedule PHẢI configurable qua `.env` hoặc `config.py`
- Bot chạy LOCAL — phải handle gracefully khi PC tắt/mở

## ⚫ Error Handling Rules

- Raindrop API fail → retry 3 lần (exponential backoff) → thông báo lỗi qua Telegram
- Article extraction fail → fallback: dùng Raindrop excerpt
- LLM timeout → retry 2 lần → fallback: gửi raw article link
- Tất cả errors PHẢI log vào file
- Telegram message > 4096 chars → PHẢI split thành nhiều messages

## 📋 OpenSpec Workflow Rules

- Luôn dùng `openspec` CLI commands, **KHÔNG** tạo file/folder thủ công
- Tạo **từng artifact một** (`/opsx:continue`), chờ user review xong mới tạo artifact tiếp
- **KHÔNG** dùng `/opsx:ff` (fast-forward) trừ khi user yêu cầu rõ ràng
- Workflow: `proposal` → user review → `specs` → user review → `design` → user review → `tasks`

## ⚪ Phase Awareness (CRITICAL)

- **Current phase**: Phase 1A (Bot Foundation)
- **KHÔNG** implement features từ phase sau trừ khi được yêu cầu rõ ràng
- Phases:
  - Phase 1A: Bot + SQLite + hardcoded article test + LLM analysis
  - Phase 1B: Raindrop integration + article queue + scheduler + error handling + /next
  - Phase 2: Reflection (ConversationHandler) + session tracking + batch digest
  - Phase 3: Weekly synthesis
  - Phase 4: Micro build loop
- Khi hoàn thành 1 phase, update field này sang phase tiếp theo

## 🔮 Future Context (KHÔNG implement bây giờ, chỉ aware)

- **Inline Keyboard** cho confidence score (Option C reflection)
- **Raindrop filter logic** khi Strategic Intelligence System bắt đầu (tags/collections riêng)
- **Strategic Intelligence System** — product riêng, KHÔNG ảnh hưởng decisions hiện tại
- Schema hiện tại KHÔNG nên thiết kế cho SIS — giữ đơn giản
