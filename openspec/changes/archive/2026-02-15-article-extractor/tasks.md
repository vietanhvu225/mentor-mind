## 1. Project Setup

- [x] 1.1 Verify `trafilatura` trong `requirements.txt` + install
- [x] 1.2 Thêm `youtube-transcript-api` vào `requirements.txt` + install
- [x] 1.3 Tạo `services/__init__.py` nếu chưa có

> **Done khi:** `import trafilatura` và `from youtube_transcript_api import YouTubeTranscriptApi` thành công.

## 2. Content Type Detection

- [x] 2.1 Tạo `services/extractor.py` với imports và constants
- [x] 2.2 Implement `detect_content_type(url)` — return "article" | "youtube" | "short_video"
- [x] 2.3 URL patterns: YouTube (youtube.com, youtu.be, shorts), Instagram reels, TikTok, Facebook reels

> **Done khi:** `detect_content_type()` phân loại đúng URL types.

## 3. Article Text Extraction

- [x] 3.1 Implement `extract_with_trafilatura(url)` — fetch + extract text + return HTML
- [x] 3.2 Implement `extract_with_jina(url)` — fallback qua `r.jina.ai`
- [x] 3.3 Implement short content detection (<200 words)
- [x] 3.4 Implement `find_and_follow_urls(text, original_url)` — cho "link ở comment" pattern

> **Done khi:** Text extraction hoạt động với fallback chain.

## 4. Image Extraction

- [x] 4.1 Implement `extract_image_urls(html)` — parse HTML, filter >100px, max 5
- [x] 4.2 Implement `download_images(urls)` — download với timeout, handle errors
- [x] 4.3 Implement `prepare_images_for_gemini(image_data)` — encode Base64 cho API

> **Done khi:** Download được ảnh từ article HTML, sẵn sàng gửi Gemini.

## 5. YouTube Transcript Extraction

- [x] 5.1 Implement `extract_youtube_id(url)` — parse video ID từ URL
- [x] 5.2 Implement `extract_youtube_transcript(url)` — dùng `youtube-transcript-api`
- [x] 5.3 Handle: no transcript available → flag + dùng title/description

> **Done khi:** YouTube transcript extraction hoạt động.

## 6. Orchestrator

- [x] 6.1 Implement `extract_content(url, excerpt)` — main orchestrator
- [x] 6.2 Define `ExtractionResult` dataclass (content, images, content_type, warnings, github_links)
- [x] 6.3 Wire: detect type → extract → images → result

> **Done khi:** `extract_content()` xử lý mọi content type và return unified result.

## 7. Update /analyze + Analyzer

- [x] 7.1 Update `analyze_command` — pick từ queue thay vì hardcoded
- [x] 7.2 Gọi `extract_content(source_url)` → update raw_content
- [x] 7.3 Update `analyzer.py` để accept images (multimodal Gemini input)
- [x] 7.4 Handle queue rỗng, extraction warnings
- [x] 7.5 Gửi content type info + warnings trước analysis output

> **Done khi:** `/analyze` chạy full flow: queue → extract → multimodal LLM → Telegram.

## 8. Camofox Browser Integration

- [x] 8.1 Tạo `services/camofox_client.py` — REST client (health, tab, snapshot, screenshot, links)
- [x] 8.2 Thêm `CAMOFOX_URL`, `CAMOFOX_USER_ID`, `CAMOFOX_API_KEY` vào config
- [x] 8.3 Wire Camofox vào `extract_content()` — Strategy 1 cho walled gardens
- [x] 8.4 Cookie auto-import — parse Netscape format, POST to Camofox API
- [x] 8.5 Screenshot-as-image cho multimodal analysis
- [x] 8.6 Tạo `docs/camofox_setup.md` — setup guide
- [x] 8.7 Test: 8181 chars extracted vs 202 chars OG meta (40x improvement)

> **Done khi:** Camofox extract full Facebook content khi server running, fallback OG meta khi không.

## 9. GitHub Link Detection + README Enrichment

- [x] 9.1 Thêm `github_links` field vào `ExtractionResult`
- [x] 9.2 Regex detect `github.com/owner/repo` trong content (có/không `https://`), deduplicate + normalize
- [x] 9.3 Hiển thị 🔗 GitHub repos trong output Telegram
- [x] 9.4 `fetch_github_readme()` — GET `raw.githubusercontent.com`, try main → master, truncate 3K chars
- [x] 9.5 Auto-enrichment: khi content < 500 words + có GitHub link → append README vào content

> **Done khi:** Bot detect GitHub URLs (kể cả không có https://), fetch README, enrich content cho LLM.

## 10. Dev Tools

- [x] 10.1 `/reset` command — reset tất cả article status về 'queued' từ Telegram
- [x] 10.2 `scripts/reset_status.py` — CLI reset script
- [x] 10.3 `scripts/test_camofox.py` — Camofox integration test

> **Done khi:** Dev có thể reset + re-test nhanh từ Telegram hoặc CLI.

## 11. Camofox Snapshot Cleaning (Dual-layer)

- [x] 11.1 `clean_camofox_snapshot()` — strip UI noise (buttons, links, navigation, toolbars)
- [x] 11.2 Keep: `text:` nodes, `article "Comment by..."`, `heading "..."`
- [x] 11.3 Kết quả: 10,000 raw → 2,884 cleaned chars (72% reduction)
- [x] 11.4 Wire vào extract_content() → Camofox text auto-cleaned

> **Done khi:** Camofox output sạch hơn 70%, fit nhiều content hơn trong cùng budget.

## 12. LLM Robustness

- [x] 12.1 Knowledge cutoff fix — inject `{today_date}` + warning vào system prompt
- [x] 12.2 LLM timeout — `timeout=120.0` trên OpenAI client
- [x] 12.3 Explicit `httpx.ReadTimeout` handling → skip retries → fallback model ngay

> **Done khi:** LLM không hang vô hạn, không đánh giá sai model versions.

## 13. Testing & Verification

- [x] 13.1 Test với blog article URL → verify full text + images extracted
- [x] 13.2 Test với YouTube URL → verify transcript extraction
- [x] 13.3 Test với Reel/TikTok URL → verify flag message
- [x] 13.4 Test `/analyze` end-to-end trên Telegram → verify multimodal output
- [x] 13.5 Chạy `/sync` → `/analyze` → verify bài thực từ Raindrop được phân tích đúng
- [x] 13.6 Test Camofox + cookies → verify full Facebook content
- [x] 13.7 Test GitHub link detection → 5/5 regex cases pass, README fetch OK, normalization OK
- [x] 13.8 Test `/reset` → reset_command exists, SQL logic verified, handler registered

> **Done khi:** End-to-end: /sync → /analyze → smart extract (+ Camofox + README) → multimodal LLM → Telegram. ✅

