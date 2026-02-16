## Context

Phase 1 hoàn thành — bot tự động sync, extract, analyze, gửi Telegram mỗi ngày. Flow hiện tại 1 chiều: bot → user. Cần habit loop: user đọc → reflect → track → build momentum.

DB tables đã có sẵn (`reflections`, `sessions`) cùng repository functions (`add_reflection`, `add_session`, `get_recent_reflections`, etc.). Chỉ cần implement bot handlers.

## Goals / Non-Goals

**Goals:**
- User có thể reflect sau khi đọc article qua 3-step conversation flow
- Track daily streak để tạo motivation
- Log session time để monitor cam kết 1h/ngày
- `/status` hiển thị streak + reflection stats

**Non-Goals:**
- Inline keyboard UI (future)
- Spaced repetition / quiz
- Gamification (badges, levels)
- Dashboard

## Decisions

### 1. ConversationHandler vs plain commands

**Chọn: ConversationHandler** (from `python-telegram-bot`)

- ✅ Natural 3-step flow: insight → action → confidence
- ✅ Built-in state management, timeout, cancel support
- ✅ Already in project dependencies
- ❌ Alternative (3 separate commands): clunky UX, user phải nhớ thứ tự

```
States: INSIGHT → ACTION → CONFIDENCE → END
Entry: /reflect
Cancel: /cancel tại bất kỳ step nào
Timeout: 10 phút → auto-cancel
```

### 2. Reflection target: last sent article vs explicit ID

**Chọn: Default last sent, optional /reflect <id>**

- User thường reflect bài vừa đọc (last sent)
- Power user có thể `/reflect 42` để reflect bài cụ thể
- Nếu không có bài sent nào → suggest `/analyze` trước

### 3. Streak calculation: stored vs dynamic

**Chọn: Dynamic** (đã quyết định từ planning — no daily_streak table)

- Query reflections grouped by date, đếm consecutive days
- Hiển thị trong `/status`
- Không cần migration, không cần maintain extra table

### 4. Session tracking: timer vs manual

**Chọn: Manual start/end** (`/session start` → `/session stop`)

- Simple, no background timer complexity
- Store start_time in `context.user_data` (in-memory, cleared on restart)
- On `/session stop` → calculate duration → insert to `sessions` table

## Data Flow

```
User: /reflect
  → Bot: "Bài #{id}: {title} — Insight chính của bạn là gì?"
  → User: "Tôi học được rằng..."
  → Bot: "Action item bạn sẽ làm?"
  → User: "Viết thử code XYZ"
  → Bot: "Confidence 1-10?"
  → User: "7"
  → Bot: "✅ Saved! 🔥 Streak: 5 ngày"
  → DB: INSERT reflections + UPDATE articles SET status='reflected'
```

## File Changes

| File | Action | Notes |
|---|---|---|
| `bot/telegram_handler.py` | MODIFY | Add ConversationHandler, `/reflect`, `/session`, update `/status`, `/help` |
| (no new files) | — | Tất cả logic trong telegram_handler.py |

## Risks / Trade-offs

- **Risk**: ConversationHandler conflicts with other handlers → **Mitigation**: Đăng ký ConversationHandler trước plain MessageHandler, dùng `filters.COMMAND` đúng cách
- **Risk**: `context.user_data` session bị mất khi restart bot → **Mitigation**: Acceptable — session chỉ mất nếu restart giữa chừng, edge case nhỏ
- **Risk**: Streak calculation chậm khi nhiều reflections → **Mitigation**: Query giới hạn 60 ngày gần nhất, đủ dùng
