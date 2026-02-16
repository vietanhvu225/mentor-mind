## Context

Bot đã có daily flow (analyze, reflect, session) + overview. Cần weekly summary tổng hợp tất cả hoạt động trong tuần, detect themes, tìm knowledge gaps, gợi ý tuần tới.

DB đã có `weekly_reports` table + `add_weekly_report()`. `MODEL_CONFIG["weekly_synthesis"]` mapped to `gemini-3-pro`.

## Goals / Non-Goals

**Goals:**
- Thu thập data tuần (articles analyzed, reflections, sessions, confidence scores)
- 1 LLM call → weekly synthesis report
- Scheduled Sunday 23:00 + on-demand `/weekly`

**Non-Goals:**
- Cross-week comparison
- Visualization/charts

## Decisions

### 1. Data gathering: query DB directly

**Chọn: Query articles/reflections/sessions trong 7 ngày qua**

- Dùng existing repo functions: `get_recent_reflections(days=7)`, articles by date range
- Thêm helper: `get_articles_by_date_range()` cho articles analyzed trong tuần

### 2. Service architecture

**Chọn: `services/synthesizer.py`** — single function `create_weekly_synthesis(db_path)`

- Gather data → format context → LLM call → save report
- Pattern giống `services/digest.py`

### 3. Scheduled job

**Chọn: Add Sunday 23:00 job trong `init_scheduler()`**

- Separate job ID: `weekly_synthesis`
- Gửi report tự động lên Telegram
- User cũng có thể trigger manual via `/weekly`

## Data Flow

```
Sunday 23:00 (or /weekly)
  → Gather: articles analyzed this week, reflections, sessions
  → Format context cho LLM
  → LLM: weekly synthesis prompt
  → Save to weekly_reports table
  → Send report via Telegram
```

## File Changes

| File | Action | Notes |
|---|---|---|
| `prompts/weekly.md` | NEW | Weekly synthesis prompt |
| `services/synthesizer.py` | NEW | Data gathering + LLM synthesis |
| `bot/telegram_handler.py` | MODIFY | Add `/weekly` + update `/help` |
| `services/scheduler.py` | MODIFY | Add Sunday 23:00 job |
| `db/repository.py` | MODIFY | Add `get_articles_by_date_range()` |
