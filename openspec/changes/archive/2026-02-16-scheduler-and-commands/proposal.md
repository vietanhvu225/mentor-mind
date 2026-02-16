## Why

Bot hiện tại yêu cầu user thủ công `/sync` + `/analyze` từng bài. Với 120 bài trong queue, workflow lặp đi lặp lại. Cần:
1. **Tự động**: Scheduler sync bài mới + gửi phân tích hàng ngày
2. **Nhanh hơn**: `/next` xem bài tiếp không cần phân tích (scan nhanh)
3. **Không bị cắt**: Telegram giới hạn 4096 chars/message — message dài bị lỗi

## What Changes

- **APScheduler integration**: Auto `/sync` + `/analyze` theo lịch (VD: mỗi sáng 8h)
- **`/next` command**: Xem title + excerpt bài tiếp theo từ queue (không phân tích, không tốn tokens)
- **`/skip` command**: Skip bài hiện tại (chuyển status → skipped), chuyển bài tiếp
- **Message splitting**: Tự động chia message >4000 chars thành nhiều message liên tiếp
- **`/schedule` command**: Xem/thay đổi lịch scheduler từ Telegram
- Update `main.py` để init scheduler cùng bot

## Capabilities

### New Capabilities
- `scheduled-jobs`: APScheduler daily jobs — auto sync + analyze
- `telegram-commands`: `/next`, `/skip`, `/schedule` commands

### Modified Capabilities
- `telegram-bot`: Message splitting cho all output
- `article-flow`: Skip workflow cho articles không quan tâm

## Impact

- **Files mới**: `services/scheduler.py`
- **Files sửa**: `main.py`, `bot/telegram_handler.py`, `config.py`, `.env.example`
- **Dependencies mới**: `apscheduler`

## Known Limitations

- **APScheduler in-process**: Chạy cùng process với bot — nếu bot restart, job reset. Chấp nhận ở phase này, persistent job store (DB) là overkill
- **Single user**: Scheduler chỉ gửi cho 1 CHAT_ID (đã config). Phù hợp personal bot

## Không làm

- Persistent job store (SQLite backed scheduler)
- Multi-user scheduling
- Web dashboard cho scheduler
- Celery/Redis task queue (over-engineering)
