Personal AI Learning Assistant
Roadmap v1.1 (Personal First – SQLite Based)

> Updated: 2026-02-14 — Reflect all decisions from planning discussion.

1. Vision

Xây dựng một AI-powered personal learning machine giúp:

- Duy trì thói quen học AI hàng ngày (minimum 1 giờ/ngày)
- Tăng chiều sâu tư duy kiến trúc (Architect mindset)
- Chuyển kiến thức → mini build thực tế
- Tạo nền tảng để sau này mở rộng cho team

Nguyên tắc:
- Lean – Structured – Scalable
- Không over-engineer. Không gamification phức tạp.

Product liên quan: Strategic Intelligence System (xem file riêng) — chỉ bắt đầu sau khi product này ổn định 30–60 ngày.

2. Core Architecture (MVP)

Tech Stack (Chốt):
- Python 3.11+
- python-telegram-bot (Telegram Bot API, ConversationHandler)
- SQLite (local file)
- APScheduler (multiple jobs, timezone-aware)
- LLM: 1 model mid-tier duy nhất (TBD — sẽ research riêng qua OpenSpec change)
- Article extraction: trafilatura hoặc Jina Reader API
- Config: python-dotenv (.env file)

Output language: Tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh.

Hosting: Local (bot chạy khi PC bật).

Không dùng:
- ❌ FastAPI (không cần web server cho MVP)
- ❌ Multi-model / multi-agent framework
- ❌ Vector DB
- ❌ Tool calling phức tạp

3. System Flow

```
A. Daily Sync (trước giờ gửi bài):
   Raindrop API → Scan ALL collections → Lấy bài mới (check raindrop_id)
         ↓
   Insert vào articles table, status = 'queued'

B. Scheduled Send:
   Pick bài từ queue (mới nhất trước, có priority)
         ↓
   Extract full content (trafilatura / Jina Reader)
         ↓
   1 LLM call → Multi-section prompt (3 persona + synthesizer)
         ↓
   Format output (< 800 từ, split nếu > 4096 chars)
         ↓
   Send to Telegram → status = 'sent'

C. Reflection (ConversationHandler):
   Bot hỏi từng câu (3 steps):
   1. 💡 Insight quan trọng nhất?
   2. 🔧 Bạn sẽ áp dụng gì?
   3. 📊 Confidence (1-10)?
         ↓
   Lưu reflection → status = 'reflected'
         ↓
   "Muốn làm thêm bài nữa không? 📚 Queue còn {N} bài"
   → User: /next → lặp lại flow B

D. Backlog Digest (cho bài cũ tồn đọng):
   5 bài cũ nhất → 1 LLM call tóm tắt digest
         ↓
   User chọn bài muốn deep-dive → đánh dấu priority cao
```

Raindrop pick logic:
- Scan tất cả collections
- Bài mới nhất trước (LIFO), trừ khi có priority cao
- Nếu không có bài mới → bot thông báo "Hôm nay không có bài mới trong Raindrop"

Error handling:
- Raindrop API fail → retry 3 lần (exponential backoff), nếu vẫn fail → gửi thông báo lỗi qua Telegram
- Article extraction fail → gửi summary từ Raindrop excerpt thay thế
- LLM timeout → retry 2 lần, nếu fail → gửi raw article link + thông báo lỗi
- Tất cả errors được log vào file

4. Schedule (On-demand + Baseline)

```
Weekday (T2-T6):
  20:00  PC on
  21:00  Auto gửi 1 bài (baseline)
         → Sau reflection → /next để lấy thêm

Thứ 7:
  12:00  PC on
  12:30  Auto gửi 1 bài
         → /next để lấy thêm
  14:30  Backlog digest (nếu có)

Chủ nhật:
  20:00  PC on
  20:30  Auto gửi 1 bài
         → /next để lấy thêm
  23:00  Weekly Synthesis + Queue Report
```

Cơ chế:
- Bot tự động gửi 1 bài/ngày (baseline đảm bảo streak)
- User dùng /next để lấy thêm bài bất cứ lúc nào
- Không giới hạn số bài/ngày

5. MVP Scope (30 Days)

Bao gồm:
- Article queue system (scan all Raindrop collections)
- On-demand article processing (/next command)
- 3 persona analysis (Researcher, Architect, Skeptic) + Synthesizer
- Reflection bắt buộc (ConversationHandler — bot hỏi từng câu)
- Batch digest cho backlog (5 bài/digest)
- 1 giờ/ngày commitment tracking (sessions)
- Weekly synthesis
- SQLite lưu trữ

Không leaderboard.
Không group.
Không drama bot.
Không scoring phức tạp.

Future enhancement (lưu context): Inline Keyboard cho confidence score (Option C).

6. Persona Design (Chốt)

1. Researcher — "Chuyện gì đang xảy ra?"
   - Tóm tắt nội dung
   - Key insights (không giới hạn số lượng)
   - Clarify technical concept

2. Architect — "Áp dụng vào thực tế thế nào?"
   - Tác động tới system design
   - Ứng dụng vào CMS / eCommerce
   - Risk & scalability concern

3. Skeptic — "Có thật sự tốt như vậy không?"
   - Chỉ ra hype
   - Giới hạn
   - Alternative approach

4. Synthesizer (auto) — Tổng hợp cuối
   - 5 bullet takeaway
   - 1 action item thực tế (AI đề xuất)

LLM call strategy: 1 call duy nhất với multi-section prompt. Mỗi persona là 1 section trong prompt, output format rõ ràng. Tiết kiệm cost, giảm latency.

7. SQLite Schema

Table: articles
- id INTEGER PRIMARY KEY
- raindrop_id TEXT UNIQUE
- date TEXT
- title TEXT
- source_url TEXT
- raw_content TEXT
- summary TEXT
- key_insights TEXT
- action_item TEXT (AI đề xuất)
- researcher_output TEXT
- architect_output TEXT
- skeptic_output TEXT
- synthesizer_output TEXT
- status TEXT DEFAULT 'queued' (queued/sent/reflected/digest_reviewed)
- queued_at TEXT
- collection_name TEXT
- priority INTEGER DEFAULT 0 (0=normal, 1=high)
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

Table: reflections
- id INTEGER PRIMARY KEY
- article_id INTEGER REFERENCES articles(id)
- reflection_text TEXT
- action_item TEXT (user tự chọn)
- confidence_score INTEGER CHECK(confidence_score BETWEEN 1 AND 10)
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

Note: Streak tính dynamic từ reflections.created_at — không cần bảng daily_streak riêng.

Table: sessions
- id INTEGER PRIMARY KEY
- date TEXT
- start_time TEXT
- end_time TEXT
- duration_minutes INTEGER
- activity_type TEXT (reflection/digest_review/deep_dive)
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

Table: batch_digests
- id INTEGER PRIMARY KEY
- article_ids TEXT (JSON array)
- digest_output TEXT
- deep_dive_selected TEXT (JSON array)
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

Table: weekly_reports
- id INTEGER PRIMARY KEY
- week_start TEXT
- themes_detected TEXT
- knowledge_gap TEXT
- build_suggestion TEXT
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

8. Phase Breakdown

PHASE 1A – Bot Foundation (Week 1)
Goal: Bot hoạt động được với article test cứng.

Tasks:
- Setup project structure + .env config
- Setup Telegram bot (nhận/gửi message)
- Setup SQLite schema (all tables)
- Hardcoded article test → LLM analysis → gửi Telegram
- Basic logging

Definition of Done:
- Bot gửi được message phân tích từ 1 article test
- Output đúng format (3 persona + synthesizer), tiếng Việt
- Lưu vào SQLite
- Logs ghi ra file

PHASE 1B – Full Pipeline (Week 2)
Goal: Bot tự động fetch bài từ Raindrop và gửi đúng giờ.

Tasks:
- Integrate Raindrop API (scan all collections)
- Article queue system (sync → queue → pick)
- Article content extraction (trafilatura / Jina Reader)
- APScheduler jobs (weekday 21:00, Sat 12:30, Sun 20:30)
- Error handling + retry logic
- Telegram message split (nếu > 4096 chars)
- /next command cho on-demand articles

Definition of Done:
- Bot gửi đúng giờ theo schedule
- Output dưới 800 từ, tiếng Việt
- Article queue hoạt động, không bị duplicate
- /next command cho phép lấy thêm bài

PHASE 2 – Reflection & Habit (Week 3)
Goal: Tạo learning loop thay vì chỉ đọc.

Flow (ConversationHandler — bot hỏi từng câu):
1. 💡 Insight quan trọng nhất hôm nay?
2. 🔧 Bạn sẽ áp dụng gì?
3. 📊 Confidence (1–10)?

Commitment Tracking:
- Session tracking (start → duration → done)
- Minimum 1 giờ/ngày
- Nhắc nhở nếu chưa có session lúc 22:00

Definition of Done:
- ConversationHandler 3-step hoạt động
- Nếu không phản hồi trong 12h → bot nhắc
- Streak tính dynamic từ reflections (hiển thị sau mỗi reflection)
- Session tracking ghi nhận thời gian làm việc
- Reflection + action_item (user) được lưu DB

PHASE 2B – Backlog Digest
Goal: Xử lý 60-70 bài tồn đọng trong Raindrop.

Flow:
- 5 bài cũ nhất → 1 LLM call → digest 3 dòng/bài
- User reply chọn bài deep-dive → priority = 1
- Bài không chọn → status = 'digest_reviewed'

Definition of Done:
- Batch digest hoạt động
- User có thể chọn bài deep-dive
- Backlog giảm 10-15 bài/tuần

PHASE 3 – Weekly Synthesis (Week 4)
Goal: Biến dữ liệu thành insight meta.

Chủ nhật 23:00 bot gửi:
```
📊 Tuần này bạn đã học:
- Topic A
- Topic B
- Topic C

🔁 Recurring Themes:
- ...

🏗️ Architectural Pattern:
- ...

🔧 Suggested Mini Build:
- ...

📚 Queue Status:
- Processed: X bài tuần này
- Remaining: Y bài trong queue
```

Definition of Done:
- LLM call riêng với prompt weekly_synthesis.md
- Input: full articles + reflections của tuần (không truncate)
- Không cần vector DB

PHASE 4 – Micro Build Loop (Week 5–6)
Goal: Knowledge → Execution

Mỗi 2 tuần:
- Chọn 1 concept
- Build mini POC
- Commit lên Git
- Viết reflection

Ví dụ:
- Mini RAG demo
- Agent orchestration script
- Prompt evaluation framework
- AI plugin idea cho CMS

Definition of Done:
- Có 1 repo nhỏ
- Có README
- Có learning summary

9. Project Structure

```
personal-ai-learning/
├── .env                    # API keys
├── .env.example            # Template
├── config.py               # Settings, timezone (UTC+7), schedules
├── main.py                 # Entry point, APScheduler setup
├── bot/
│   └── telegram_handler.py # Telegram bot, ConversationHandler, /next
├── services/
│   ├── raindrop.py         # Raindrop API client, scan all collections
│   ├── extractor.py        # Article content extraction
│   ├── analyzer.py         # LLM multi-persona analysis (1 call)
│   └── synthesizer.py      # Weekly synthesis generation
├── db/
│   ├── models.py           # SQLite schema + init
│   └── repository.py       # DB CRUD operations
├── prompts/
│   ├── daily_analysis.md   # System prompt + format template
│   ├── weekly_synthesis.md # Weekly report prompt
│   └── personas/
│       ├── researcher.md   # Researcher persona instructions
│       ├── architect.md    # Architect persona instructions
│       ├── skeptic.md      # Skeptic persona instructions
│       └── synthesizer.md  # Synthesizer persona instructions
├── tests/                  # Critical path tests (parse output, DB ops)
├── logs/                   # Log files
├── requirements.txt        # Dependencies
└── README.md
```

10. 30-Day KPI

- ≥ 25 ngày active streak
- ≥ 20 reflections
- ≥ 25 giờ total session time (1h/ngày × 25 ngày)
- ≥ 1 mini build hoàn chỉnh
- ≥ 1 weekly synthesis chất lượng
- Backlog < 10 bài remaining

11. Budget

Usage: ~120k tokens / tháng (có thể cao hơn với on-demand + digest)
Dự kiến: $10–25 / tháng

12. Anti-Overengineering Rules

- Không vector DB trong 30 ngày đầu
- Không microservice
- Không dashboard web
- Không scoring hệ thống
- Không persona quá 3
- Không multi-model
- Không agent framework

13. Future Expansion (Not Now)

Chỉ xem xét sau 30 ngày thành công:
- Inline Keyboard cho reflection confidence (Option C)
- Invite 3–5 dev
- Add basic contribution tracking
- Add lightweight leaderboard
- Add memory retrieval (RAG)
- Xem xét Strategic Intelligence System (product riêng)
  - Note: Cần Raindrop filter logic để phân biệt bài learning vs business

14. Success Criteria Before Inviting Others

Bạn chỉ mở rộng khi:
- 30 ngày không bị đứt streak
- Bạn build ít nhất 1 POC
- Weekly synthesis thật sự hữu ích
- Bạn cảm thấy "không có bot thì thiếu"

15. Founder Commitment

- 30 ngày kỷ luật
- Mỗi ngày tối thiểu 1 giờ (session tracking)
- Mỗi ngày phản hồi bot
- Mỗi tuần review nghiêm túc
- Không thay đổi scope giữa chừng

Final Principle

Build a Personal AI Learning Machine first.
Scale only after discipline is proven.