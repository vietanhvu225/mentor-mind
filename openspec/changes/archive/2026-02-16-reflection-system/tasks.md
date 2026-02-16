## 1. Reflection ConversationHandler

- [x] 1.1 Import `ConversationHandler` trong `telegram_handler.py`
- [x] 1.2 Define states: `INSIGHT`, `ACTION`, `CONFIDENCE`
- [x] 1.3 Implement `reflect_command()` — entry point: tìm last sent article hoặc theo ID
- [x] 1.4 Implement `reflect_insight()` — lưu insight, hỏi action
- [x] 1.5 Implement `reflect_action()` — lưu action, hỏi confidence
- [x] 1.6 Implement `reflect_confidence()` — validate 1-10, save to DB, show streak
- [x] 1.7 Implement `reflect_cancel()` — `/cancel` handler
- [x] 1.8 Register ConversationHandler trong `build_application()`
- [x] 1.9 Set timeout = 10 phút (ConversationHandler.TIMEOUT)

> **Done khi:** `/reflect` → 3 step conversation → saved to reflections table + article status = 'reflected'

## 2. Streak Calculation

- [x] 2.1 Add function `calculate_streak(db_path)` — query reflections, count consecutive days
- [x] 2.2 Show streak in reflection confirmation message
- [x] 2.3 Show streak in `/status` output

> **Done khi:** Streak tính đúng, hiển thị sau reflect + trong /status

## 3. Session Tracking

- [x] 3.1 Implement `session_command()` — parse args (start/stop/status)
- [x] 3.2 `/session start` → lưu start_time vào `context.user_data`
- [x] 3.3 `/session stop` → tính duration → insert DB → show summary
- [x] 3.4 `/session` (no args) → show session đang chạy hoặc tổng hôm nay
- [x] 3.5 Register handler trong `build_application()`

> **Done khi:** `/session start` → `/session stop` → saved to sessions table

## 4. Update Existing Commands

- [x] 4.1 Update `/status` — thêm streak, total reflections, thời gian học hôm nay
- [x] 4.2 Update `/help` — thêm `/reflect`, `/session`, `/cancel`

> **Done khi:** `/status` hiển thị đầy đủ stats + `/help` list commands mới

## 5. Testing & Verification

- [x] 5.1 Test reflection flow: `/reflect` → insight → action → confidence → confirmation
- [x] 5.2 Test `/reflect <id>` với article ID cụ thể
- [x] 5.3 Test `/cancel` tại mỗi step
- [x] 5.4 Test invalid confidence (text, số ngoài range)
- [x] 5.5 Test streak calculation (0 days, 1 day, multiple days)
- [x] 5.6 Test `/session start` → `/session stop`
- [x] 5.7 Test `/status` hiển thị streak + stats
- [x] 5.8 Compile check

> **Done khi:** Tất cả commands hoạt động + reflection flow end-to-end OK
