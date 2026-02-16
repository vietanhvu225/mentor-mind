## Context

110 bài trong queue từ Raindrop, nhưng raw_content chỉ là excerpt. Content types đa dạng: blog/article, social posts (Facebook/LinkedIn groups, influencer — nhiều ảnh), YouTube videos, Reels. Cần smart extraction engine xử lý tất cả.

## Goals / Non-Goals

**Goals:**
- Smart content type detection (article vs YouTube vs reel vs social post)
- Text + image extraction cho articles → Gemini multimodal
- YouTube transcript extraction
- Short content / "link ở comment" detection + follow
- Tích hợp vào `/analyze` flow

**Non-Goals:**
- Video download/frame extraction
- Audio transcription (Whisper)
- ~~Headless browser rendering~~ → now supported via Camofox (optional)
- Platform-specific APIs

## Decisions

### 1. Content type detection bằng URL pattern matching
- **Chọn**: Regex patterns cho YouTube, Instagram, TikTok, Facebook reels
- **Lý do**: Đơn giản, nhanh, cover 95% cases. Không cần HEAD request hay content sniffing
- **Alternative**: HTTP HEAD + Content-Type → chậm hơn, overkill

### 2. Multimodal Gemini cho images (thay vì alt text)
- **Chọn**: Download ảnh lớn → gửi Base64/URL cho Gemini 3 Pro vision
- **Lý do**: User bookmark chủ yếu social posts — alt text gần như không có. Gemini đã hỗ trợ multimodal, đang dùng cho Stage 1
- **Alternative**: Alt text extraction → vô dụng cho social media. Screenshot → cần Playwright, quá nặng

### 3. Image filtering: kích thước >100px, max 5 ảnh
- **Chọn**: Filter ảnh >100x100px, skip dưới (icons/avatars). Lấy max 5 ảnh lớn nhất
- **Lý do**: Giảm noise (icons, buttons), giới hạn tokens. 5 ảnh đủ cho hầu hết articles
- **Trade-off**: Có thể miss ảnh nhỏ nhưng quan trọng → acceptable

### 4. YouTube transcript via `youtube-transcript-api`
- **Chọn**: Python library `youtube-transcript-api` — không cần API key
- **Lý do**: Miễn phí, scrape transcript trực tiếp, hỗ trợ auto-generated captions
- **Alternative**: YouTube Data API v3 → cần API key, quota limits

### 5. Short content → follow extracted URLs
- **Chọn**: Khi content <200 words, tìm URL trong body → follow URL dài nhất → extract
- **Lý do**: Pattern "link ở comment" phổ biến — URL thường là URL duy nhất hoặc dài nhất
- **Trade-off**: Có thể follow sai link → nhưng better than no content

### 7. Camofox browser cho walled gardens (optional)
- **Chọn**: Camofox REST API server (Firefox fork, C++ anti-detection) as fallback
- **Lý do**: Facebook/LinkedIn block httpx → chỉ lấy được OG preview. Camofox render full page, bypass detection
- **Integration**: REST API calls via httpx → `localhost:9377`. Graceful degradation: if Camofox not running, fallback to OG meta
- **Trade-off**: Cần Node.js + ~300MB binary. Nhưng optional — bot vẫn hoạt động bình thường nếu không cài

### 6. Data flow

```
URL vào extract_content()
         ↓
    detect_content_type(url)
         ↓
    ┌─ "article" ──→ _is_walled_garden(url)?
    │                  ├─ YES → Camofox (if available) → full render + screenshot
    │                  │        └─ fallback: OG meta tags (httpx)
    │                  ├─ NO  → trafilatura → text + HTML
    │                  │        └─ [fallback] Jina Reader
    │                  ├─ extract_images(html) → filter >100px, max 5
    │                  └─ short? → find_urls() → follow → re-extract
    │
    ├─ "youtube" ──→ extract_youtube(url)
    │                  └─ youtube-transcript-api → transcript text
    │
    └─ "short_video" → flag "📱 Xem trực tiếp"
         ↓
    extract GitHub links → regex github.com/owner/repo → deduplicate
         ↓
    ExtractionResult(text, images[], type, warnings[], github_links[])
         ↓
    Update DB raw_content
         ↓
    analyzer.py → Gemini multimodal (text + images)
```

### 8. Dual-layer content reduction (Camofox → clean_camofox_snapshot)

Khi extract từ walled garden (Facebook, LinkedIn), raw HTML page rất lớn (~200-500KB). Content thực chỉ chiếm ~1-5%. Pipeline tối ưu qua **2 tầng reduction**:

**Layer 1 — Camofox Accessibility Snapshot** (~90% reduction)
- Camofox **không trả HTML gốc** — thay vào trả **accessibility tree**: cấu trúc dạng text mô tả semantic các DOM elements
- Kỹ thuật: Playwright `page.accessibility.snapshot()` → duyệt DOM tree → emit text-only representation
- Input: ~300KB HTML → Output: ~10-15KB tree text
- Giữ: text nodes, button labels, link text, headings, image alt text
- Bỏ: CSS, JavaScript, inline styles, attributes, nesting tags

```
Layer 1 example:
  HTML:  <div class="x1a2b3c"><span dir="auto">Hello world</span></div>
  Tree:  - text: "Hello world"
```

**Layer 2 — `clean_camofox_snapshot()`** (~72% reduction tiếp)
- Parse tree text từ Layer 1 → chỉ giữ content thực
- **Giữ**: `- text: "..."` (post body, comments), `article "Comment by ..."` (attribution), `heading "..."` (tiêu đề)
- **Bỏ**: `button`, `link`, `img`, `navigation`, `banner`, `toolbar`, `slider`, `combobox`, `status`, URL lines

```
Layer 2 example:
  Before: - button "Like" [e15]          ← bỏ
          - text: "PROMPT 1: The Arch..." ← giữ
          - link "8h" [e23]              ← bỏ
          - /url: https://facebook...    ← bỏ
  After:  PROMPT 1: The Architecture Strategist...
```

**Kết quả đo được (bài 116 — 9 Claude Opus 4.6 prompts):**

| Layer | Input | Output | Reduction |
|-------|-------|--------|-----------|
| Raw HTML (Facebook) | ~300KB | — | — |
| Layer 1: Accessibility snapshot | ~300KB | 10,000 chars | ~97% |
| Layer 2: clean_camofox_snapshot | 10,000 chars | 2,884 chars | 72% |
| **Tổng cộng** | **~300KB** | **2,884 chars** | **~99%** |

→ 2,884 chars chỉ chứa nội dung thực: tiêu đề, nội dung bài, 4 prompts đầy đủ (PROMPT 1-3 + phần PROMPT 4). Với cùng budget 10K chars, giờ fit được **~3x nhiều content hơn**.

### 9. GitHub link auto-detection + README enrichment (Hybrid)

Nhiều bài trong queue là dạng "giới thiệu nhanh GitHub repo" — content rất ngắn (~100 words), thông tin chính nằm trong README trên GitHub. Pipeline xử lý:

**Step 1 — Detection**: Regex match `github.com/owner/repo` (có hoặc không có `https://`)
```python
# Regex mới: match cả "github.com/..." và "https://github.com/..."
pattern = r'(?:https?://)?github\.com/[\w.-]+/[\w.-]+'
# Normalize: thêm https:// nếu thiếu
```

**Step 2 — README Fetch** (`fetch_github_readme()`):
- GET `https://raw.githubusercontent.com/{owner}/{repo}/main/README.md`
- Fallback: thử branch `master` nếu `main` trả 404
- Truncate: max 3,000 chars → tránh token overflow

**Step 3 — Auto-enrichment** (chỉ khi content ngắn):
- Điều kiện: `word_count < 500` **VÀ** có GitHub link
- Append README (max 2 repos) vào content trước khi gửi LLM
- LLM nhận: bài gốc + README → phân tích sâu hơn

**Step 4 — Telegram output**:
- Hiển thị `🔗 GitHub repos trong bài:` + list link
- User có link để deep dive thêm

```
Flow: FB post (89 words) → detect github.com/AndyMik90/Auto-Claude
      → fetch README (3,021 chars) → append
      → LLM phân tích (89 + 135 = 224 words enriched)
      → Output: analysis + 🔗 link GitHub
```

**Kết quả đo (bài 119):** Content 89 words → enriched 224 words → LLM có đủ context để phân tích features, tech stack, use cases.

## Risks / Trade-offs

- **Image download**: Một số sites block hotlinking → set User-Agent, handle 403
- **Gemini token cost**: Ảnh tốn tokens → max 5 ảnh là balance tốt
- **YouTube transcript quality**: Auto-generated có thể sai → vẫn tốt hơn không có gì
- **Social post extraction**: Facebook/LinkedIn actively block scraping → OG meta tags fallback
- **Follow URL risk**: Có thể follow link quảng cáo → acceptable, user sẽ thấy kết quả sai

## Known Limitations (Enhance Later)

### Facebook "link in comments"
- Facebook comments **không** có trong public HTML — yêu cầu authentication
- **Solved (partial)**: Camofox render full page → `get_links()` lấy tất cả URLs trên trang
- **Solved (manual)**: Bot detect bài ngắn → hỏi user paste URL từ comment (`url_message_handler`)
- **Future**: Camofox + cookie import → full login access → đọc comments trực tiếp
- **Future**: Tìm URL trong Raindrop `note` field (user paste link khi bookmark) → auto-follow

