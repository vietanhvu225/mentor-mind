## ADDED Requirements

### Requirement: Content Type Detection
Hệ thống MUST auto-detect content type từ URL để chọn extraction strategy phù hợp.

#### Scenario: YouTube URL
- **WHEN** URL match pattern YouTube (youtube.com/watch, youtu.be, youtube.com/shorts)
- **THEN** hệ thống MUST classify là `youtube` và dùng transcript extraction

#### Scenario: Reel/Story URL
- **WHEN** URL match pattern Instagram reel, Facebook reel, TikTok
- **THEN** hệ thống MUST classify là `short_video`
- **THEN** skip extraction, flag "📱 Short video — xem trực tiếp"

#### Scenario: Regular article/blog URL
- **WHEN** URL không match video patterns
- **THEN** hệ thống MUST classify là `article` và dùng text + image extraction

---

### Requirement: Article Text Extraction
Hệ thống MUST extract full text từ article URLs với fallback chain.

#### Scenario: Trafilatura thành công
- **WHEN** trafilatura extract được content ≥200 words
- **THEN** dùng kết quả trafilatura

#### Scenario: Trafilatura fail → Jina Reader fallback
- **WHEN** trafilatura return None hoặc <200 words
- **THEN** fallback sang Jina Reader API (`https://r.jina.ai/{url}`)

#### Scenario: Cả 2 fail → dùng excerpt
- **WHEN** cả trafilatura và Jina Reader fail
- **THEN** dùng Raindrop excerpt từ DB + warning "⚠️ Không extract được full content"

---

### Requirement: Image Extraction cho Multimodal Analysis
Hệ thống MUST extract ảnh quan trọng từ article để gửi kèm text cho Gemini.

#### Scenario: Có ảnh trong article
- **WHEN** article có images với kích thước >100x100px
- **THEN** download tối đa 5 ảnh lớn nhất (skip icons, avatars, ads)
- **THEN** gửi cả text + images cho Gemini multimodal

#### Scenario: Không có ảnh hoặc download fail
- **WHEN** không tìm thấy ảnh đủ lớn hoặc download fail
- **THEN** proceed với text-only analysis (như hiện tại)

#### Scenario: Nhiều ảnh (>5)
- **WHEN** article có >5 ảnh lớn
- **THEN** chọn 5 ảnh lớn nhất + append note "🖼️ Bài có {N} ảnh — chỉ phân tích top 5"

---

### Requirement: YouTube Transcript Extraction
Hệ thống MUST extract transcript từ YouTube videos.

#### Scenario: Video có transcript
- **WHEN** YouTube video có auto-generated hoặc manual captions
- **THEN** extract transcript text + video title
- **THEN** dùng transcript làm content cho LLM analysis

#### Scenario: Video không có transcript
- **WHEN** YouTube video không có captions available
- **THEN** flag "🎬 Video không có transcript — xem trực tiếp: {url}"
- **THEN** dùng video title + description làm minimal content

---

### Requirement: Short Content Detection
Hệ thống MUST detect content quá ngắn (có thể là social post / "link ở comment").

#### Scenario: Content ngắn + có URLs trong body
- **WHEN** extracted content <200 words VÀ body chứa URLs
- **THEN** extract URL dài nhất từ body → follow → extract article từ URL đó
- **THEN** nếu follow thành công, dùng content từ followed URL

#### Scenario: Content ngắn + không có URLs
- **WHEN** extracted content <200 words VÀ không có URLs
- **THEN** flag "⚠️ Bài ngắn — có thể là social post. Xem trực tiếp: {url}"
- **THEN** proceed với short content

---

### Requirement: Update raw_content sau extraction
Hệ thống MUST update `articles.raw_content` trong DB sau extraction thành công.

#### Scenario: Update DB
- **WHEN** extraction thành công (bất kỳ source nào)
- **THEN** update `articles.raw_content` với extracted content
- **THEN** giữ excerpt cũ nếu toàn bộ extraction fail

---

## MODIFIED Requirements

### Requirement: Telegram /analyze Command
Update `/analyze` để pick từ queue + smart extract trước khi gọi LLM.

#### Scenario: Analyze article từ queue
- **WHEN** user gửi `/analyze`
- **THEN** pick bài tiếp theo (status=queued)
- **THEN** smart extract (detect type → extract → images)
- **THEN** gửi extraction warnings nếu có
- **THEN** LLM pipeline → Telegram output

#### Scenario: Queue rỗng
- **WHEN** không có article status=queued
- **THEN** "📭 Queue trống! Dùng /sync để lấy bài mới."
