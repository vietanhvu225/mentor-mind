## Why

Phase 1A xong — bot có thể nhận hardcoded article, phân tích qua LLM, gửi output qua Telegram. Bước tiếp theo: kết nối với nguồn bài thực tế. Raindrop.io là nơi user lưu trữ articles — cần sync bài mới vào queue để bot tự động xử lý.

## What Changes

- Tạo `services/raindrop.py` — Raindrop API client
- Scan ALL collections, lấy bài mới (dedup bằng raindrop_id)
- Queue sync: insert bài mới vào DB (status=queued)
- Pick logic: LIFO (mới nhất trước), trừ khi có priority cao
- Retry logic: 3 lần exponential backoff, fail → thông báo qua Telegram
- Thêm `/sync` command để trigger manual sync

## Capabilities

### New Capabilities
- `raindrop-sync`: Raindrop API client — xác thực, scan collections, fetch articles, queue sync, dedup, retry logic, pick logic

### Modified Capabilities
- (không có)

## Prerequisites

1. Vào [app.raindrop.io/settings/integrations](https://app.raindrop.io/settings/integrations)
2. **Create new app** → đặt tên (VD: "Learning Assistant")
3. Click app → **Create test token** (permanent, full access)
4. Paste vào `.env`:
   ```
   RAINDROP_API_TOKEN=your_token_here
   ```

## Impact

- **Files mới**: `services/raindrop.py`
- **Files sửa**: `bot/telegram_handler.py` (thêm /sync), `config.py` (RAINDROP_API_TOKEN)
- **Dependencies**: `httpx` (đã có)
- **Config**: `RAINDROP_API_TOKEN` trong `.env`

## Known Limitations

- **Ảnh/Infographic**: Raindrop excerpt và text extraction không capture ảnh → bài nặng visual sẽ thiếu context cho LLM
- **"Link ở comment"**: Bookmark URL có thể là social post (LinkedIn, Facebook), article URL thực nằm trong comment → extract content sẽ chỉ được text post, không phải bài viết
- Cả 2 sẽ được xử lý ở change `article-extractor` (#6)

## Không làm

- Article content extraction (change riêng: `article-extractor`)
- Scheduled auto-sync (change riêng: `scheduler-and-commands`)
- Tag filtering hoặc collection filtering
- Pagination phức tạp — fetch recent items đủ dùng
