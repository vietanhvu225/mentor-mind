## Why

Raindrop sync hoạt động — 110 bài trong queue. Nhưng `raw_content` chỉ là excerpt (~200 chars). User bookmark đa dạng content types: blog articles, social posts (nhiều ảnh), YouTube videos, Reels. Cần module thông minh để extract content tối đa từ mọi loại URL.

## What Changes

- Tạo `services/extractor.py` — smart content extraction engine
- **Content type detection**: Auto-detect URL → Article, YouTube, Reel/Story, Social Post
- **Article extraction**: trafilatura (primary) + Jina Reader (fallback)
- **Image extraction**: Download ảnh quan trọng → gửi multimodal Gemini
- **YouTube**: Extract transcript qua `youtube-transcript-api`
- **Reels/Stories**: Flag + link (không extract, thông báo user xem trực tiếp)
- **Short content / "link ở comment"**: Detect → extract URLs từ post → follow link
- **Camofox browser** (optional): Anti-detection Firefox fork cho Facebook/LinkedIn → full page render, screenshot, link extraction. Graceful degradation nếu không cài
- **GitHub link detection**: Detect `github.com/owner/repo` URLs trong content → hiển thị riêng trong output cho user clone/nghiên cứu
- **`/reset` dev command**: Reset tất cả status về 'queued' từ Telegram, tiện khi dev/test
- Update `/analyze` flow: pick từ queue → smart extract → LLM → Telegram

## Capabilities

### New Capabilities
- `content-extraction`: Smart content extraction — type detection, text + image + video, fallback chain, graceful degradation

### Modified Capabilities
- `article-flow`: Update `/analyze` để pick từ queue + extract trước khi gọi LLM

## Impact

- **Files mới**: `services/extractor.py`, `services/camofox_client.py`, `docs/camofox_setup.md`
- **Files sửa**: `bot/telegram_handler.py`, `services/analyzer.py`, `config.py`, `.env.example`
- **Dependencies mới**: `youtube-transcript-api`
- **Dependencies có**: `trafilatura`, `httpx`
- **External (optional)**: Camofox browser server (Node.js, ~300MB)

## Known Limitations

- **Reels/Stories**: Không extract content — chỉ flag cho user xem trực tiếp
- **Paywall**: Một số bài cần login → partial extract + flag
- **"Link ở comment"**: Camofox `get_links()` giải quyết phần lớn. Fallback: bot hỏi user paste URL
- **Camofox optional**: Cần cài riêng Node.js server. Bot vẫn chạy bình thường nếu không có

## Không làm

- Whisper audio transcription (quá nặng cho local)
- Platform-specific APIs (Instagram/TikTok quá hạn chế)
- PDF extraction
- Video download + frame extraction
- ~~Headless browser (Playwright) — over-engineering~~ → giải quyết bằng Camofox (nhẹ hơn Playwright)
