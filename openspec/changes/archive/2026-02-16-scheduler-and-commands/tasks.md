## 1. Project Setup

- [x] 1.1 Thêm `apscheduler` vào `requirements.txt` + install
- [x] 1.2 Thêm config vars: `SCHEDULE_HOUR`, `SCHEDULE_MINUTE`, `SCHEDULE_ENABLED`
- [x] 1.3 Update `.env.example` với scheduler config

> **Done khi:** `from apscheduler.schedulers.asyncio import AsyncIOScheduler` thành công.

## 2. Message Splitting

- [x] 2.1 Implement `split_message(text, max_len=4000)` trong `telegram_handler.py`
- [x] 2.2 Update `send_message()` — gọi `split_message()`, gửi lần lượt
- [x] 2.3 Delay 0.3s giữa các chunks để tránh rate limit

> **Done khi:** Message >4000 chars tự split và gửi nhiều message liên tiếp.

## 3. /next Command

- [x] 3.1 Implement `next_command()` — query DB `WHERE status='queued' ORDER BY id LIMIT 1`
- [x] 3.2 Format: title + excerpt (100 chars) + URL + content_type
- [x] 3.3 Register handler trong `build_application()`

> **Done khi:** `/next` hiển thị preview bài tiếp theo, zero LLM cost.

## 4. /skip Command

- [x] 4.1 Implement `skip_command()` — update status → 'skipped'
- [x] 4.2 After skip, tự show next queued (reuse logic /next)
- [x] 4.3 Register handler trong `build_application()`

> **Done khi:** `/skip` mark bài hiện tại, hiện bài tiếp theo.

## 5. Scheduler Service

- [x] 5.1 Tạo `services/scheduler.py` với `AsyncIOScheduler`
- [x] 5.2 Implement `init_scheduler(bot)` — tạo + start scheduler
- [x] 5.3 Implement `daily_sync_and_analyze(bot)` — full job flow
- [x] 5.4 Implement `get_scheduler_info()` — status, next run, config

> **Done khi:** Scheduler start cùng bot, job chạy đúng giờ.

## 6. /schedule Command

- [x] 6.1 Implement `schedule_command()` — parse args (xem/đổi giờ/on/off)
- [x] 6.2 Register handler trong `build_application()`

> **Done khi:** User control scheduler từ Telegram.

## 7. Main.py Integration

- [x] 7.1 Import + call `init_scheduler(app.bot)` trong `main()`
- [x] 7.2 Update help text với commands mới

> **Done khi:** Bot start → scheduler auto-start.

## 8. Testing & Verification

- [x] 8.1 Test message split với text >4000 chars
- [x] 8.2 Test `/next` → verify preview hiển thị đúng
- [x] 8.3 Test `/skip` → verify status change + next preview
- [x] 8.4 Test `/schedule` → verify status display
- [x] 8.5 Compile check tất cả files
- [x] 8.6 End-to-end: restart bot → verify scheduler start log

> **Done khi:** Tất cả commands hoạt động + scheduler start OK.
