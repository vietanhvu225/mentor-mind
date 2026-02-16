## Why

Phase 1 hoàn thành: bot sync Raindrop → extract → analyze → gửi Telegram mỗi ngày. Nhưng flow hiện tại chỉ 1 chiều (bot → user). User đọc analysis xong không có cách nào **tương tác ngược** — ghi nhận insight, đặt action item, đánh giá mức hiểu. Không có reflection = không có habit loop = không duy trì được thói quen học.

## What Changes

- **Thêm ConversationHandler 3-step reflection flow**: Sau khi đọc analysis, user bắt đầu `/reflect` → bot hỏi 3 câu tuần tự (insight → action → confidence) → lưu vào DB → update article status → gửi confirmation
- **Thêm streak tracking**: Tính streak từ reflections (mấy ngày liên tiếp có reflect) — hiển thị trong `/status`
- **Thêm session logging**: `/session` command ghi nhận thời gian học (start/end) — hỗ trợ cam kết 1h/ngày
- **Update `/status`**: Thêm streak count, total reflections, average confidence

## Capabilities

### New Capabilities
- `reflection-flow`: ConversationHandler 3-step (insight → action → confidence), streak tracking, session logging

### Modified Capabilities
- `telegram-bot`: Thêm `/reflect`, `/session` commands vào handler + update `/status` hiển thị streak

## Impact

- **Code mới**: `bot/telegram_handler.py` (ConversationHandler + commands)
- **DB**: Dùng tables có sẵn (`reflections`, `sessions`) + repository functions đã implement
- **Dependencies**: Không thêm dependency mới — `ConversationHandler` đã có trong `python-telegram-bot`

## Không làm

- ❌ Inline keyboard reflection (Option C — future enhancement)
- ❌ Spaced repetition / quiz system
- ❌ Dashboard / visualization
- ❌ Gamification phức tạp (badges, levels)
