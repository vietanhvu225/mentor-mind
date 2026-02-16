## 1. Project Setup

- [x] 1.1 Thêm `RAINDROP_API_TOKEN` vào `config.py` (load từ `.env`) — đã có sẵn
- [x] 1.2 Thêm `RAINDROP_API_TOKEN` vào `.env.example` — đã có sẵn
- [x] 1.3 Verify `.env` đã có token thực

> **Done khi:** `from config import RAINDROP_API_TOKEN` trả về giá trị hợp lệ.

## 2. Raindrop API Client

- [x] 2.1 Tạo `services/raindrop.py` với imports và constants (`BASE_URL`, `HEADERS`)
- [x] 2.2 Implement `fetch_raindrops(page, perpage)` — gọi `GET /rest/v1/raindrops/0`
- [x] 2.3 Implement retry logic: 3 lần, exponential backoff (2s, 4s, 8s)
- [x] 2.4 Implement `fetch_all_new_raindrops(db_path)` — pagination + stop-at-existing
- [x] 2.5 Handle errors: 401 (token sai), 429 (rate limit), timeout, network error

> **Done khi:** `fetch_all_new_raindrops()` trả về list raindrops từ API.

## 3. Queue Sync

- [x] 3.1 Implement `sync_raindrops_to_db(db_path, raindrops)` — dedup bằng raindrop_id
- [x] 3.2 Map fields: `_id`→raindrop_id, `title`→title, `link`→source_url, `excerpt`→raw_content
- [x] 3.3 Return `SyncResult(total, new, skipped)` dataclass
- [x] 3.4 Implement `pick_next_article(db_path)` — ORDER BY priority DESC, queued_at DESC

> **Done khi:** Articles mới được insert vào DB, duplicates bị skip.

## 4. Telegram Integration

- [x] 4.1 Thêm `async def sync_command(update, context)` vào `telegram_handler.py`
- [x] 4.2 Gửi feedback "⏳ Đang sync Raindrop..."
- [x] 4.3 Gọi `fetch_all_new_raindrops()` + `sync_raindrops_to_db()` qua `run_in_executor`
- [x] 4.4 Gửi kết quả: "✅ Sync xong: {new} bài mới / {total} tổng"
- [x] 4.5 Handle error: gửi thông báo lỗi nếu sync fail
- [x] 4.6 Register `/sync` handler trong `build_application()`
- [x] 4.7 Update `/help` message — thêm /sync

> **Done khi:** `/sync` trên Telegram trigger sync và báo kết quả.

## 5. Testing & Verification

- [x] 5.1 Chạy bot, gửi `/sync` → 110 fetched, 110 mới ✅
- [x] 5.2 Gửi `/sync` lần 2 → 0 fetched, 0 mới (dedup) ✅
- [x] 5.3 Gửi `/status` → queued: 112, sent: 3, Total: 115 ✅

> **Done khi:** Full flow: /sync → DB insert → dedup verified.
