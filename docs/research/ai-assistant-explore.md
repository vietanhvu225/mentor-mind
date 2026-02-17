# AI Assistant Exploration — Explore Notes

> Created: 2026-02-17
> Context: Exploring AI Assistant tools for MentorMind Phase 2

## Background

MentorMind hoàn thành Phase 1 (11 changes archived). Bắt đầu explore hướng tích hợp AI Assistant frameworks.

Full comparison: [COMPARISON.md](../../../COMPARISON.md)

## Key Insight: MentorMind vs AI Assistants

MentorMind và 6 AI Assistant tools ở **2 layers khác nhau**:

```
Layer 3: DOMAIN APP         → MentorMind (learning bot)
Layer 2: AI ASSISTANT FRAMEWORK → OpenClaw / nanobot / ZeroClaw...
Layer 1: LLM API + INFRA    → OpenAI / Anthropic / Ollama...
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
- Optional: study ZeroClaw (Rust/trait-based)

### Path B: Borrow Patterns (2-3 tuần)
- Semantic memory system → kết nối insights giữa articles
- Heartbeat/proactive → spaced repetition reminders
- Channel abstraction → decouple từ Telegram

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

## Features Worth Borrowing

| Feature | Source | Priority | Fit |
|---|---|---|---|
| Semantic memory | nanobot, ZeroClaw | ⭐⭐⭐⭐⭐ | Kết nối insights, spaced repetition |
| Heartbeat/proactive | nanobot, ZeroClaw | ⭐⭐⭐⭐ | Nhắc ôn bài, push notification |
| Channel abstraction | All | ⭐⭐⭐ | Multi-channel support |
| Skills/Plugin system | nanobot, ZeroClaw | ⭐⭐ | Khi mở rộng scope |
| MCP | nanobot | ⭐⭐ | Khi cần tool server protocol |

## Next Steps

1. Mở editor mới cho `g:\Target\2-nanobot-study\`
2. Cài nanobot, setup Telegram bot mới
3. Dùng thử 1-2 tuần, ghi notes
4. Rút bài học → apply vào MentorMind Phase 2B
