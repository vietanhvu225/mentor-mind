## Context

Proposal chốt **2-stage pipeline**: Gemini 3 Pro (phân tích) + Claude Opus 4.6 (planning).
Tất cả models đều có sẵn qua Google AI Ultra subscription ($0 chi phí thêm), quota 100%, reset ~5h.

Hiện tại project chưa có code — đây là technical design cho service layer phân tích bài viết.

## Goals / Non-Goals

**Goals:**
- Design 2-stage LLM pipeline (analysis → planning) với model routing
- Auto-fallback chain khi primary model lỗi
- Config-driven model assignment (dễ swap model qua `.env`)
- Compatible với project structure đã chốt (`services/analyzer.py`)

**Non-Goals:**
- Không implement model switching UI/command
- Không benchmark models
- Không runtime model selection (chỉ config-time)
- Không multi-model cho cùng 1 stage

## Decisions

### Decision 1: 2-Stage Pipeline thay vì 1-Call

**Chọn:** 2 LLM calls tuần tự (Stage 1 → Stage 2)
**Thay vì:** 1 call duy nhất cho tất cả personas

```
Article text
     │
     ▼
┌─────────────────────────────────────┐
│ Stage 1: PHÂN TÍCH (Gemini 3 Pro)   │
│                                     │
│ Input:  article_content + prompt    │
│ Output: researcher_output           │
│         architect_output            │
│         skeptic_output              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Stage 2: KẾ HOẠCH (Claude Opus 4.6) │
│                                     │
│ Input:  stage_1_output + prompt     │
│ Output: synthesizer_output          │
│         action_plan                 │
└─────────────────────────────────────┘
```

**Lý do:**
- Gemini 3 Pro: MMMU 81%, tiếng Việt tốt nhất → phân tích article
- Claude Opus 4.6: ARC-AGI 37.6%, SWE-Bench 80.9% → reasoning + planning
- Mỗi stage dùng 1 model → coherent, không "đánh trống thổi còi"
- 2 calls (~20s total) chấp nhận được cho daily use, không realtime

**Alternatives considered:**
- 1 call (Gemini only): Đơn giản hơn, nhưng action plan kém sâu
- 4 calls (1 per persona): Quá phức tạp, mất coherence giữa personas
- Song song 2 calls: Không được vì Stage 2 cần output Stage 1

### Decision 2: Config-driven Model Routing

**Chọn:** Dict mapping task → model trong `config.py`

```python
# config.py
MODEL_CONFIG = {
    "stage_1_analysis": os.getenv("MODEL_STAGE_1", "gemini-3-pro"),
    "stage_2_planning": os.getenv("MODEL_STAGE_2", "claude-opus-4-6-thinking"),
    "batch_digest":     os.getenv("MODEL_DIGEST", "gemini-3-pro"),
    "weekly_synthesis": os.getenv("MODEL_WEEKLY", "gemini-3-pro"),
}

# Fallback chỉ cần cho app-level — proxy đã xử lý account rotation & 429 retry
FALLBACK_CHAIN = [
    "gemini-3-flash",       # cheap & fast fallback
    "claude-sonnet-4-5",    # mid-tier fallback
]
```

**Lý do:**
- Swap model chỉ cần sửa `.env`, không sửa code
- Anti-overengineering: không cần factory pattern hay plugin system
- Fallback chain đơn giản: try next model trong list
- Proxy đã xử lý account-level retry/rotation → app-level chỉ cần model-level fallback

### Decision 3: API Integration via Antigravity Tools (Manager) Proxy

**Chọn:** Gọi tất cả models qua Antigravity Tools proxy tại `http://127.0.0.1:8045/v1`
**Thay vì:** Gọi trực tiếp Google/Anthropic API riêng lẻ

```python
# services/llm_client.py — CHỈ CẦN 1 PACKAGE: openai
import openai

client = openai.OpenAI(
    api_key=os.getenv("ANTIGRAVITY_API_KEY", "sk-antigravity"),
    base_url=os.getenv("ANTIGRAVITY_BASE_URL", "http://127.0.0.1:8045/v1")
)

# Stage 1: Gemini 3 Pro — qua proxy
response = client.chat.completions.create(
    model="gemini-3-pro",
    messages=[{"role": "user", "content": analysis_prompt}]
)

# Stage 2: Claude Opus 4.6 — CÙNG client, CÙNG endpoint
response = client.chat.completions.create(
    model="claude-opus-4-6-thinking",
    messages=[{"role": "user", "content": planning_prompt}]
)
```

**Lợi ích lớn của Antigravity Tools proxy:**
- **1 package duy nhất** (`openai`) thay vì 2 (`google-generativeai` + `anthropic`)
- **1 endpoint** cho mọi model (Gemini, Claude, GPT)
- **Auto-rotation**: proxy tự chuyển account khi 429/401 (mili-giây)
- **Quota management**: tự track quota, skip account hết quota
- **Health scoring**: tự demote account lỗi, promote account healthy
- **Tiered routing**: Ultra > Pro > Free priority tự động
- **No API key management**: bot chỉ cần 1 `sk-antigravity` key
- **Model mapping**: proxy có thể remap model IDs nếu cần

### Decision 4: Prompt File Structure

**Chọn:** Hybrid prompt files (như đã chốt trong plan)

```
prompts/
├── daily_analysis.md       # Stage 1: system prompt + format template
│                           # Include personas/researcher.md + architect.md + skeptic.md
├── action_planning.md      # Stage 2: synthesizer + action planning prompt
├── weekly_synthesis.md     # Weekly report prompt
├── batch_digest.md         # Backlog digest prompt
└── personas/
    ├── researcher.md
    ├── architect.md
    ├── skeptic.md
    └── synthesizer.md       # Dùng trong Stage 2 prompt
```

**Thay đổi so với plan:**
- Thêm `action_planning.md` cho Stage 2 (Claude Opus)
- `synthesizer.md` vẫn trong `personas/` nhưng inject vào Stage 2 prompt

### Decision 5: Error Handling & Fallback (Simplified by Proxy)

**Proxy đã xử lý:** account rotation, 429 retry, exponential backoff, health scoring
**App chỉ cần xử lý:** model-level fallback + graceful degradation

```
Stage 1: client.create(model="gemini-3-pro", ...)
     │
     │  Proxy tự retry 2x + rotate accounts
     │  Nếu tất cả accounts fail:
     ▼
App nhận error → Try fallback: gemini-3-flash
     │  Proxy lại tự retry + rotate
     │  Nếu vẫn fail:
     ▼
Try fallback: claude-sonnet-4-5
     │  still fail
     ▼
Send error notification via Telegram: "LLM không khả dụng, gửi raw article link"
```

Tương tự cho Stage 2. Nếu Stage 2 fail nhưng Stage 1 OK → vẫn gửi Stage 1 output (3 persona) mà không có synthesizer/action plan.

**Note:** Vì proxy đã handle retry/rotation, app-level fallback chỉ trigger khi **toàn bộ** accounts cho 1 model đều fail → rất hiếm khi xảy ra.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Latency ~20s (2 calls) | User chờ lâu hơn | Chấp nhận — daily use, không realtime |
| Stage 2 hiểu sai Stage 1 output | Action plan sai hướng | Prompt rõ ràng + format output Stage 1 structured |
| Quota hết giữa ngày | Bỏ lỡ scheduled send | Proxy auto-rotation + app-level model fallback |
| Antigravity Tools proxy down | Bot mất kết nối LLM | Health check proxy trước khi call; graceful error msg |
| Output format không consistent | Parse lỗi | Validate output format, retry nếu sai |

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|--------|
| `openai` (Python) | ≥1.0 | Duy nhất 1 LLM client package — gọi mọi models qua proxy |
| Antigravity Tools | ≥4.0 | Local proxy tại `localhost:8045`, cần chạy song song với bot |
