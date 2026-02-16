## Context

LLM pipeline (`services/analyzer.py`), database (`db/`), và Telegram bot (`bot/`) đã hoạt động riêng lẻ. Cần wire chúng lại thành 1 flow end-to-end. Dùng hardcoded article text để test — chưa cần Raindrop hay URL extraction.

## Goals / Non-Goals

**Goals:**
- `/analyze` command trigger full flow
- "Đang phân tích..." feedback khi LLM đang xử lý
- Format output Markdown với 4 sections (3 personas + synthesizer)
- Lưu article + analysis vào SQLite
- Graceful error handling khi LLM fail

**Non-Goals:**
- Real article từ Raindrop
- URL extraction
- Multiple articles
- Message splitting (giả sử output < 4096 chars)

## Decisions

### 1. Hardcoded article text

**Chọn:** 1 đoạn article ngắn (~500 words) về AI topic, embeded trực tiếp trong code
**Rationale:** Đơn giản nhất để test. Không cần network call, không cần extraction. Dễ reproduce.

### 2. Async flow trong handler

**Chọn:** Send "Đang phân tích..." → await analyze → Send result
**Rationale:** LLM call mất 10-30 giây, user cần biết bot đang xử lý.

### 3. Output format

**Chọn:** Markdown text với emoji headers cho mỗi persona
```
📰 [Article Title]

🔬 Researcher: [...]
🏗️ Architect: [...]
🤔 Skeptic: [...]
📝 Tổng hợp: [...]
🎯 Action Item: [...]
```

### 4. Database storage

**Chọn:** `add_article()` trước khi analyze → `update_article_analysis()` sau khi xong → `update_article_status()` → "sent"
**Rationale:** Track article ngay từ đầu. Nếu LLM fail, article vẫn trong DB với status "queued".

## Data Flow

```
User → /analyze
  │
  ├── 1. Bot gửi "Đang phân tích..."
  ├── 2. add_article(hardcoded) → DB (status=queued)
  ├── 3. analyze_article(text) → LLM proxy → analysis result
  ├── 4. update_article_analysis(result) → DB
  ├── 5. update_article_status("sent") → DB
  └── 6. send_message(formatted_output) → Telegram
```
