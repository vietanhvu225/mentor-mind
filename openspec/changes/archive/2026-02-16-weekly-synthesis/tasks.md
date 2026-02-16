## 1. Weekly Prompt
- [x] 1.1 Tạo `prompts/weekly.md`

## 2. Synthesizer Service
- [x] 2.1 Tạo `services/synthesizer.py`
- [x] 2.2 Implement `create_weekly_synthesis(db_path)` — gather data → LLM → save

## 3. Telegram /weekly Command
- [x] 3.1 Implement `weekly_command()` trong `telegram_handler.py`
- [x] 3.2 Register handler + update `/help`

## 4. Scheduled Sunday Job
- [x] 4.1 Thêm Sunday 23:00 job trong `services/scheduler.py`

## 5. Verification
- [x] 5.1 Compile check — All OK
- [x] 5.2 Test `/weekly` — cả 2 scenario pass

### Test Cases (script: `scripts/seed_weekly_test.py`)

#### Case A: Active user (`--active`)
- **Input**: 12 articles (sent), 7 reflections (confidence 6-9), 7 sessions (30-45 phút)
- **Expected**: Full report với themes, knowledge gaps, gợi ý tuần tới
- **Result**: ✅ Pass — 32 articles detected (12 test + 20 existing), 7 reflections, LLM output OK
- **Note**: Markdown fallback triggered (400 Bad Request → plain text gửi OK)

#### Case B: Inactive user (`--inactive`)
- **Input**: 2 articles (sent), 1 reflection (confidence 4), 0 sessions
- **Expected**: Report ngắn, nhẹ, khuyến khích học thêm
- **Result**: ✅ Pass — 22 articles detected (2 test + 20 existing), 1 reflection, LLM output OK
- **Note**: Markdown fallback triggered (400 Bad Request → plain text gửi OK)

#### Restore
- `--restore` copy backup file về → data gốc nguyên vẹn ✅
