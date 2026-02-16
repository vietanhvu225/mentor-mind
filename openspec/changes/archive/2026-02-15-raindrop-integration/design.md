## Context

Phase 1A hoàn tất — bot phân tích hardcoded article end-to-end. Giờ cần kết nối với nguồn bài thực tế từ Raindrop.io. User lưu ~60-70 bookmarks AI/tech trong Raindrop, cần sync vào DB để bot tự động xử lý.

## Goals / Non-Goals

**Goals:**
- Raindrop API client hoạt động với test token
- Sync tất cả bookmarks vào articles table (dedup)
- Pick logic cho article queue (LIFO + priority)
- `/sync` command cho Telegram bot

**Non-Goals:**
- Article content extraction (change riêng)
- Auto-scheduled sync (change riêng — scheduler)
- Collection/tag filtering
- OAuth flow (dùng test token)

## Decisions

### 1. Dùng `collectionId=0` thay vì scan từng collection
- **Chọn**: `GET /rest/v1/raindrops/0` — trả về ALL bookmarks
- **Lý do**: 1 API call thay vì N calls (1 per collection). Đơn giản, ít code
- **Alternative**: Scan từng collection → phức tạp hơn, chỉ cần nếu muốn filter

### 2. Dùng `httpx` (đã có) thay vì thêm thư viện mới
- **Chọn**: `httpx` synchronous client
- **Lý do**: Đã là dependency (LLM client dùng). Không thêm overhead
- **Alternative**: `requests` — cũng được nhưng thêm dependency không cần thiết

### 3. Excerpt thay thế raw_content tạm thời
- **Chọn**: Map Raindrop `excerpt` → `articles.raw_content`
- **Lý do**: Raindrop API trả excerpt (~200 chars). Full content extraction là change riêng
- **Trade-off**: LLM analysis trên excerpt sẽ kém hơn full text, nhưng đủ để test flow

### 4. Stop-at-existing strategy cho pagination
- **Chọn**: Khi gặp raindrop_id đã có trong DB → dừng fetch tiếp
- **Lý do**: Tiết kiệm API calls. Bài cũ hơn chắc chắn đã được sync
- **Trade-off**: Nếu user xóa rồi re-add bài cũ thì sẽ miss. Acceptable

### 5. Data flow

```
/sync command (hoặc scheduled trigger)
        ↓
services/raindrop.py
  └─ fetch_new_raindrops() → GET /rest/v1/raindrops/0?sort=-created
        ↓
  └─ sync_to_db() → check raindrop_id, INSERT IF NOT EXISTS
        ↓
Return SyncResult(total=N, new=M, skipped=K)
        ↓
bot/telegram_handler.py → gửi kết quả cho user
```

## Risks / Trade-offs

- **Rate limit** (120 req/min) → Không vấn đề với sync pattern hiện tại
- **Excerpt thiếu context** → LLM analysis sẽ kém hơn → giải quyết ở `article-extractor`
- **Test token expiry** → Test token không expire, nhưng nên handle 401 gracefully
- **Large backlog** (60-70 bài) → Pagination xử lý được, nhưng initial sync sẽ insert nhiều
- **Bài nặng ảnh/infographic** → Text extraction mất ảnh → LLM thiếu visual context → cần multimodal hoặc flag cho user (xử lý ở `article-extractor`)
- **"Link ở comment" pattern** → Bookmark URL ≠ article URL (VD: LinkedIn post → "link ở dưới") → extract content sẽ sai target → cần detect + follow link (xử lý ở `article-extractor`)

## Open Questions

- (Không có — đủ rõ ràng để implement)
