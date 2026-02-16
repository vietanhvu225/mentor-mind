## Why

Hiện tại bot xử lý 1 bài/ngày (scheduler) hoặc on-demand (user gọi /analyze). Khi backlog nhiều (>5 bài queued), user phải analyze từng bài một — mất thời gian và thiếu cross-article insights. Cần batch digest: gom 5 bài → 1 digest tóm tắt, user chọn bài deep-dive.

## What Changes

- **Thêm `/digest` command**: Gom N bài queued cũ nhất (default 5) → extract all → LLM tạo digest tóm tắt → gửi Telegram
- **Thêm `/digest <n>` variant**: User chọn số bài muốn gom (2-10)
- **Thêm digest prompt**: Prompt riêng cho batch digest — tóm tắt themes chung, so sánh, gợi ý deep-dive
- **Save digest**: Lưu vào `batch_digests` table, update articles status → 'digest_reviewed'
- **Deep-dive selection**: Sau digest, user chọn bài muốn /analyze chi tiết

## Capabilities

### New Capabilities
- `batch-digest`: Digest processing cho backlog articles — gom nhiều bài thành 1 digest summary

### Modified Capabilities
- `telegram-bot`: Thêm `/digest` command vào handlers + update `/help`
- `scheduled-jobs`: Scheduler có thể trigger batch digest khi backlog > threshold (optional)

## Impact

- **Code mới**: `services/digest.py` (digest logic), `prompts/digest.md` (prompt template)
- **Code sửa**: `bot/telegram_handler.py` (thêm `/digest` command + update `/help`)
- **DB**: Dùng tables có sẵn (`batch_digests`) + repository functions
- **LLM**: 1 LLM call cho digest (text dài hơn analyze đơn lẻ)
- **Dependencies**: Không thêm dependency mới

## Không làm

- ❌ Auto-trigger digest (giữ manual via `/digest`)
- ❌ Digest scheduling riêng (dùng manual command)
- ❌ Digest comparison across weeks
- ❌ Complex UI cho deep-dive selection (dùng simple text reply)
