## ADDED Requirements

### Requirement: Raindrop API Authentication
Hệ thống MUST xác thực với Raindrop API bằng test token từ `.env`.

#### Scenario: Token hợp lệ
- **WHEN** hệ thống gọi Raindrop API với `RAINDROP_API_TOKEN` hợp lệ
- **THEN** API trả về HTTP 200 với data

#### Scenario: Token thiếu hoặc sai
- **WHEN** `RAINDROP_API_TOKEN` thiếu hoặc không hợp lệ
- **THEN** hệ thống MUST log error và return empty list (không crash)

---

### Requirement: Fetch All Raindrops
Hệ thống MUST fetch tất cả bookmarks từ Raindrop (collectionId=0, tức ALL collections trừ Trash).

#### Scenario: Fetch thành công
- **WHEN** sync được trigger
- **THEN** hệ thống gọi `GET /rest/v1/raindrops/0` với pagination (perpage=50)
- **THEN** trả về list raindrops với fields: `_id`, `title`, `link`, `excerpt`, `created`, `collection.$id`

#### Scenario: Pagination
- **WHEN** user có >50 bookmarks
- **THEN** hệ thống MUST fetch nhiều pages cho đến khi hết dữ liệu

#### Scenario: API timeout hoặc lỗi mạng
- **WHEN** Raindrop API không respond hoặc trả về error
- **THEN** hệ thống MUST retry 3 lần (exponential backoff: 2s, 4s, 8s)
- **THEN** nếu vẫn fail → return empty list và log error

---

### Requirement: Queue Sync (Dedup)
Hệ thống MUST sync raindrops mới vào DB articles table, dedup bằng `raindrop_id`.

#### Scenario: Bài mới chưa có trong DB
- **WHEN** raindrop có `_id` chưa tồn tại trong `articles.raindrop_id`
- **THEN** hệ thống MUST insert vào articles với status='queued'
- **THEN** fields mapping: `_id`→raindrop_id, `title`→title, `link`→source_url, `excerpt`→raw_content, `created`→date, `collection.title`→collection_name

#### Scenario: Bài đã có trong DB
- **WHEN** raindrop có `_id` đã tồn tại trong `articles.raindrop_id`
- **THEN** hệ thống MUST skip (không duplicate, không update)

#### Scenario: Sync report
- **WHEN** sync hoàn tất
- **THEN** hệ thống MUST return count: tổng fetched, mới inserted, đã skip

---

### Requirement: Pick Logic
Hệ thống MUST pick article từ queue theo thứ tự ưu tiên.

#### Scenario: Pick bài tiếp theo
- **WHEN** cần pick bài để phân tích
- **THEN** chọn article có status='queued', ORDER BY priority DESC, queued_at DESC (LIFO)

#### Scenario: Queue rỗng
- **WHEN** không có article nào status='queued'
- **THEN** return None và thông báo "Hôm nay không có bài mới trong Raindrop"

---

### Requirement: Telegram /sync Command
User MUST có thể trigger sync thủ công qua `/sync` command.

#### Scenario: Manual sync
- **WHEN** user gửi `/sync` trên Telegram
- **THEN** bot gửi "⏳ Đang sync Raindrop..." feedback
- **THEN** chạy queue sync
- **THEN** gửi kết quả: "✅ Sync xong: {new} bài mới / {total} tổng"

#### Scenario: Sync fail
- **WHEN** Raindrop API fail sau 3 retries
- **THEN** bot gửi "❌ Sync thất bại. Kiểm tra API token và kết nối mạng."
