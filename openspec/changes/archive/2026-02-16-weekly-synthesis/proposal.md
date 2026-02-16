## Why

Hiện tại bot track daily (analyze + reflect + session) nhưng thiếu weekly review. User không biết tuần vừa rồi học gì, themes nào lặp lại, kiến thức nào còn gap. Cần weekly synthesis tự động chạy cuối tuần để tổng hợp tiến độ + gợi ý tuần tới.

## What Changes

- **Thêm `/weekly` command**: Tạo weekly synthesis on-demand
- **Thêm scheduled Sunday job**: Tự động tạo + gửi weekly report lúc 23:00 CN
- **Thêm weekly prompt**: Prompt template cho weekly synthesis
- **Thêm synthesizer service**: `services/synthesizer.py` — thu thập data tuần → LLM synthesis

## Capabilities

### New Capabilities
- `weekly-synthesis`: Tổng hợp tuần — themes, progress, knowledge gaps, gợi ý tuần tới

### Modified Capabilities
- `telegram-bot`: Thêm `/weekly` vào handlers + update `/help`
- `scheduled-jobs`: Thêm Sunday 23:00 job cho weekly synthesis

## Impact

- **Code mới**: `services/synthesizer.py`, `prompts/weekly.md`
- **Code sửa**: `bot/telegram_handler.py` (/weekly + /help), `services/scheduler.py` (Sunday job)
- **DB**: Dùng `weekly_reports` table có sẵn + `add_weekly_report()`
- **Dependencies**: Không thêm dependency mới

## Không làm

- ❌ Weekly comparison (so sánh tuần này vs tuần trước)
- ❌ Dashboard/chart
- ❌ Email report
