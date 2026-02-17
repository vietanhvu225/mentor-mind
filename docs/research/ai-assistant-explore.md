# AI Assistant Exploration — Explore Notes

> Created: 2026-02-17
> Context: Exploring AI Assistant tools for MentorMind Phase 2

## Background

MentorMind hoàn thành Phase 1 (11 changes archived). Bắt đầu explore hướng tích hợp AI Assistant frameworks.

Full comparison: [COMPARISON.md](../../../COMPARISON.md)

## Key Insight: MentorMind vs AI Assistants

MentorMind và 6 AI Assistant tools ở **2 layers khác nhau**:

```
Layer 3: DOMAIN APP             → MentorMind (learning bot)
Layer 2: AI ASSISTANT FRAMEWORK → OpenClaw / nanobot / ZeroClaw...
Layer 1: LLM API + INFRA        → OpenAI / Anthropic / Ollama...
```

MentorMind = Layer 3, chạy trực tiếp trên Layer 1 (bỏ qua Layer 2).
6 tools = Layer 2 frameworks để xây bất kỳ assistant nào.

| So sánh | MentorMind | 6 Tools (Layer 2) |
|---|---|---|
| Input | Commands (`/analyze`, `/reflect`) | Natural language (mở) |
| Decision | Code logic cố định | AI tự quyết dùng tool nào |
| Scope | Learning only | Anything |
| Channel | Telegram only | Multi-channel |

## Plan: 3 Paths (Sequential)

### Path A: Study (1-2 tuần)
- Cài nanobot → dùng thử → đọc source → hiểu architecture
- Workspace riêng: `g:\Target\2-nanobot-study\`
- Optional: study ZeroClaw (Rust/trait-based, chỉ học concepts)

### Path B: Borrow Patterns — **Discord first** (2-3 tuần)
- **🔥 Discord channel** → Pycord integration, chạy song song Telegram
- Channel abstraction → decouple từ Telegram, tạo ABC interface
- Semantic memory system → kết nối insights giữa articles
- Heartbeat/proactive → spaced repetition reminders

### Path C: Rebuild (3-4 tuần, conditional)
- Rebuild MentorMind trên nanobot framework
- Quyết định sau khi hoàn thành Path B

## Tools Ranked by Fit for MentorMind

| Rank | Tool | Score | Lý do |
|---|---|---|---|
| 🥇 | **nanobot** | ⭐⭐⭐⭐⭐ | Cùng Python stack, ~4K lines dễ đọc, MCP support, Telegram channel, pip install dễ setup |
| 🥈 | **ZeroClaw** | ⭐⭐⭐⭐ | Architecture concepts xuất sắc (trait-based), 22+ providers, nhưng Rust = khác stack |
| 🥉 | **OpenClaw** | ⭐⭐⭐ | Full-featured nhất, nhưng quá nặng (>1GB), TypeScript, cần WSL2, cần subscription |
| 4 | **PicoClaw** | ⭐⭐ | Nhẹ nhưng Go binary, early dev, ít tính năng |
| 5 | **NanoClaw** | ⭐⭐ | Chỉ Claude, chỉ WhatsApp, không Windows |
| 6 | **TinyClaw** | ⭐ | Không Windows native, cần subscription, quá experimental |

### Phản biện COMPARISON.md
- Multi-agent ×1.5 → nên ×0.5 (MentorMind không cần agent orchestration)
- Windows ×2 → giữ nguyên (phù hợp user context)
- Thiếu tiêu chí "Python stack compatibility" — rất quan trọng cho MentorMind
- nanobot re-score cao hơn khi tính Python stack compatibility
- ZeroClaw (Rust) = dealbreaker cho Path C rebuild, chỉ đáng study concepts

## Features Worth Borrowing

| Feature | Source | Priority | Fit |
|---|---|---|---|
| **Discord channel** | Pycord + skill guide | ⭐⭐⭐⭐⭐ | Voice/screen share, team collab, quen thuộc hơn Telegram |
| Channel abstraction | nanobot | ⭐⭐⭐⭐⭐ | Nền tảng cho multi-channel, cần refactor trước |
| Semantic memory | nanobot, ZeroClaw | ⭐⭐⭐⭐ | Kết nối insights, spaced repetition |
| Heartbeat/proactive | nanobot, ZeroClaw | ⭐⭐⭐ | Nhắc ôn bài, push notification |
| Skills/Plugin system | nanobot, ZeroClaw | ⭐⭐ | Khi mở rộng scope |

## Discord Analysis

### Thuận lợi
- Pycord (Python) — cùng stack, `discord-bot-architect` skill có sẵn patterns
- Cùng asyncio — scheduler (APScheduler) hoạt động với cả Telegram + Discord
- Discord unique: threads (1 thread/article), embeds (rich output), voice/screen share
- Slash commands tương đương Telegram commands — mapping 1:1

### Khó khăn
- Chạy 2 bot cùng lúc: cần orchestrate asyncio event loops
- Message format khác: Telegram Markdown vs Discord Embeds → cần formatter layer
- `/reflect` conversation flow: Telegram ConversationHandler vs Discord Modals (khác pattern)
- Rate limit: Discord tighter (5 msg/s vs Telegram 30 msg/s)
- Slash command registration cần deploy script riêng (anti-pattern: sync on every start)

### Command Mapping Telegram → Discord

| Telegram | Discord | Complexity |
|---|---|---|
| `/next`, `/skip`, `/status` | Slash commands | Easy |
| `/analyze`, `/overview`, `/weekly` | Slash cmd → Thread + Embed | Medium |
| `/reflect` (ConversationHandler) | Modal (form) | Redesign |
| URL paste → auto-extract | `on_message` listener | Easy |
| Scheduler output | Send to specific channel | Easy |

## nanobot Study Targets (cho workspace `2-nanobot-study`)

### Target 1: Setup & Run (1-2 ngày)
- [ ] `pip install nanobot-ai`
- [ ] Config Telegram channel (dùng bot token khác MentorMind)
- [ ] Chat thử, test các tính năng cơ bản
- [ ] Ghi nhận: onboarding experience, pain points

### Target 2: Architecture Deep Dive (2-3 ngày)
- [ ] Đọc source code (~4K lines), vẽ architecture diagram
- [ ] Tìm hiểu agent loop: message in → LLM → tool → response
- [ ] Tìm hiểu memory system: persistent memory redesign (02/2026)
- [ ] Tìm hiểu MCP integration: server/client, tool discovery

### Target 3: Multi-Channel Abstraction (FOCUS — 2-3 ngày)
- [ ] Tìm file/module quản lý channels (Telegram, Discord, WhatsApp...)
- [ ] Trace flow: message arrives → channel adapter → core → response → channel adapter
- [ ] Xác định Channel interface/ABC: methods nào? (send, receive, format?)
- [ ] So sánh Telegram adapter vs Discord adapter: khác gì? chung gì?
- [ ] Ghi note: pattern nào apply được cho MentorMind?

### Target 4: Evaluate & Report (1-2 ngày)
- [ ] Viết `notes/vs-mentormind.md`: so sánh architecture
- [ ] Viết `notes/channel-abstraction-pattern.md`: pattern rút ra
- [ ] Quyết định: borrow pattern hay rebuild?
- [ ] Update `docs/research/ai-assistant-explore.md` trong MentorMind

## Next Steps

1. ✅ Update ROADMAP Phase 2 (nâng priority Discord)
2. Mở editor mới cho `g:\Target\2-nanobot-study\`
3. Follow study targets ở trên
4. Rút bài học → apply vào MentorMind Phase 2B (Discord + channel abstraction)
