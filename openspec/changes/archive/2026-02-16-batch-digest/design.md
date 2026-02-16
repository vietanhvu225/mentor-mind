## Context

Bot hiện xử lý 1 article/lần qua `/analyze`. Khi queue có nhiều bài, cần cách xử lý batch — tóm tắt nhiều bài thành 1 digest, cho user overview nhanh và chọn bài deep-dive.

DB đã có `batch_digests` table + repository functions (`add_batch_digest`, `get_latest_digest`, `get_oldest_queued_articles`). Cần implement digest logic + Telegram command.

## Goals / Non-Goals

**Goals:**
- User gom N bài queued → 1 LLM call → digest summary
- Digest highlight themes chung, so sánh, gợi ý deep-dive
- Sau digest, user chọn bài analyze chi tiết

**Non-Goals:**
- Auto-trigger digest
- Complex deep-dive selection UI
- Cross-digest comparison

## Decisions

### 1. Digest logic: single service file vs inline

**Chọn: `services/digest.py`** — tách riêng digest logic

- Extract all articles → combine text → single LLM call
- Cleaner separation, reusable cho scheduler nếu cần sau
- Digest prompt khác analyze prompt → cần prompt riêng

### 2. Digest prompt: combined vs per-article

**Chọn: Combined single prompt**

- Gom text tất cả articles vào 1 prompt → LLM tạo digest tổng hợp
- Hợp lý hơn per-article vì mục đích là so sánh + themes chung
- Token limit: 5 bài × ~2000 chars ≈ 10K chars input → OK cho mid-tier model

### 3. Deep-dive selection: ConversationHandler vs simple reply

**Chọn: Simple suggest** — sau digest, bot suggest `/analyze <id>` cho từng bài

- Không cần ConversationHandler phức tạp
- User tự chọn analyze bài nào
- Giữ simple, tránh overengineering

### 4. Extract before digest: yes vs skip

**Chọn: Extract each article** trước khi digest

- Cần content thật để LLM tóm tắt đúng
- Reuse `extract_content()` cho từng bài
- Parallel extraction nếu cần optimize sau

## Data Flow

```
User: /digest 5
  → Bot: "⏳ Đang extract 5 bài..."
  → Extract article 1..5 (reuse extract_content)
  → Bot: "🤖 Đang tạo digest..."
  → LLM: combined prompt with all 5 articles
  → Bot: Digest output (themes, summaries, deep-dive suggestions)
  → DB: INSERT batch_digests + UPDATE articles status → 'digest_reviewed'
```

## File Changes

| File | Action | Notes |
|---|---|---|
| `services/digest.py` | NEW | Digest logic: extract batch → combine → LLM call |
| `prompts/digest.md` | NEW | Digest prompt template |
| `bot/telegram_handler.py` | MODIFY | Add `/digest` command + update `/help` |

## Risks / Trade-offs

- **Risk**: Large combined text exceeds token limit → **Mitigation**: Truncate each article to ~2000 chars, max 10 articles
- **Risk**: Extraction fails for some articles → **Mitigation**: Skip failed, continue with rest, report failures
- **Risk**: Digest output too long for Telegram → **Mitigation**: Reuse `send_long_message` with chunking
