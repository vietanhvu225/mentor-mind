# So sánh AI Assistant: OpenClaw vs nanobot vs PicoClaw vs TinyClaw vs NanoClaw vs ZeroClaw

> **Đối tượng:** Software Developer / Tech Lead trên Windows  
> **Ngày phân tích:** 2026-02-17  
> **Bối cảnh:** 6 giải pháp thuộc hệ sinh thái "Personal AI Assistant" mã nguồn mở. OpenClaw là dự án gốc (145K+ GitHub stars), 5 giải pháp còn lại lấy cảm hứng và tối ưu theo hướng riêng.

---

## 1. Tổng quan nhanh

| Tiêu chí | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **Ngôn ngữ** | TypeScript/Node.js (≥22) | Python (≥3.11) | Go (≥1.21) | TypeScript/Node.js (v14+) + Bash | TypeScript/Node.js (≥20) | **Rust** (stable) |
| **Triết lý** | Full-featured, production-grade | Ultra-lightweight, research-ready | Ultra-efficient, edge/embedded | Multi-agent, multi-team | Minimal, auditable, container-isolated | **Zero overhead, fully swappable, deploy anywhere** |
| **Codebase** | Lớn (430K+ dòng) | ~4,000 dòng core | Single binary, <10MB RAM | TypeScript + Bash | ~35K tokens (~8 files) | **Single binary 3.4MB**, 1,017 tests |
| **Tổ chức** | Peter Steinberger + community | HKUDS (HKU Data Science) | Sipeed (hardware) | Community (jlia0) | Community (gavrielc) | ZeroClaw Labs (27+ contributors) |
| **License** | MIT | MIT | MIT | MIT | MIT | **Apache 2.0** |
| **Maturity** | **Production-ready** | v0.1.3.post7 (active dev) | Early dev (pre-v1.0) | Experimental | Early, opinionated | Active dev, 1,017 tests, CI/CD |
| **Stars** | **145K+** | Phổ biến nhanh | 12K / tuần | Đang phát triển | Mới | Đang phát triển |
| **LLM Backend** | Anthropic/OpenAI (OAuth) | 13+ providers | 3-7 providers | Claude Code/Codex CLI | Claude Agent SDK | **22+ providers** (trait-based) |

---

## 2. Bối cảnh: Phong trào Personal AI Assistant 2026

Năm 2026 đánh dấu sự chuyển dịch mạnh mẽ từ AI chatbot thụ động sang **AI Agent tự chủ** (Agentic AI):

- **OpenClaw** — dự án gốc, full-featured, 145K+ GitHub stars, xây dựng bởi Peter Steinberger. Là "foundational standard" cho phong trào personal AI assistant mã nguồn mở
- **nanobot** — bản rút gọn Python (~4,000 dòng), tập trung research & extensibility
- **PicoClaw** — rewrite Go từ nanobot, tối ưu cho embedded/edge hardware $10
- **TinyClaw** — wrapper multi-agent trên Claude Code CLI / Codex CLI
- **NanoClaw** — phản đề của OpenClaw: cùng core functionality nhưng codebase đủ nhỏ để 1 người đọc hiểu toàn bộ, bảo mật bằng container isolation thay vì application-level checks
- **ZeroClaw** — rewrite Rust từ đầu: 3.4MB binary, <5MB RAM, <10ms startup, 22+ providers, trait-based architecture cho phép swap mọi subsystem, **Windows native**, bảo mật multi-layer (pairing + sandbox + allowlists + tunnel + encrypted secrets)
- **Xu hướng chính:** AI assistant chạy local, bảo mật dữ liệu cá nhân, tích hợp đa kênh chat, tự động hóa workflow
- **85% developer** đã sử dụng AI tools trong coding (theo khảo sát cuối 2025)
- Các giải pháp thương mại (GitHub Copilot, Cursor, Windsurf) tập trung vào **coding assistant trong IDE**, trong khi nhóm này hướng đến **personal AI assistant đa năng 24/7**

---

## 3. So sánh chi tiết theo tiêu chí

### 3.1. Khả năng chạy trên Windows ⚠️

| Tiêu chí | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **Windows native** | ⚠️ WSL2 "strongly recommended" | ✅ Tốt (Python cross-platform) | ⚠️ Cần build Go binary cho Windows | ❌ Yêu cầu macOS/Linux, tmux, Bash 4.0+ | ❌ macOS hoặc Linux (có RFS `/setup-windows`) | ✅ **Windows native** (MSVC + Rust toolchain) |
| **WSL2 support** | ✅ Có docs riêng cho Windows/WSL2 | ✅ Hoạt động tốt | ✅ Hoạt động tốt | ⚠️ Khả thi qua WSL2 nhưng không chính thức | ⚠️ Có RFS skill nhưng chưa implement | ✅ Không cần (native Windows) |
| **Docker** | ✅ Có Docker docs | ✅ Có Dockerfile | ✅ Có Docker Compose | ❌ Không đề cập | ✅ **Core architecture** — agents chạy trong container | ✅ Docker sandboxed runtime (`runtime.kind = "docker"`) |
| **Nix support** | ✅ Có nix-openclaw | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Cài đặt** | `npm install -g openclaw@latest` | `pip install nanobot-ai` | Build from source hoặc prebuilt binary | `curl \| bash` hoặc clone + npm install | `git clone` → `claude` → `/setup` | `cargo install --path .` hoặc `cargo build --release` |
| **Onboarding** | ✅ **Wizard tương tác** (`openclaw onboard`) | ✅ `nanobot onboard` | ✅ `picoclaw onboard` | ✅ Setup wizard | ✅ AI-native: Claude Code `/setup` | ✅ **`zeroclaw onboard`** (quick / interactive / channels-only) |

> **Nhận xét cho Windows user:** **ZeroClaw là lựa chọn Windows-native tốt nhất** — Rust binary chạy trực tiếp, không cần WSL2/Python/Node.js. nanobot vẫn thân thiện nhất (Python cross-platform). OpenClaw có docs WSL2 đầy đủ nhất. TinyClaw và NanoClaw cần WSL2/Linux.

### 3.2. Kiến trúc & Thiết kế

| Tiêu chí | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **Mô hình agent** | **Multi-agent routing** (sessions isolate) | Single agent + subagent (spawn) | Single agent + subagent (spawn) | **Multi-agent, multi-team** | Single agent + **Agent Swarms** | Single agent + daemon mode |
| **Control plane** | ✅ **Gateway WS control plane** | CLI-based | CLI-based | File-based queue | Single Node.js process + SQLite | **Gateway HTTP** (127.0.0.1:8080) + pairing |
| **Agent loop** | Pi agent runtime (RPC) + tool/block streaming | LLM ↔ Tool execution loop | LLM ↔ Tool execution loop | File-based queue → parallel processing | Claude Agent SDK trong container | **Trait-based** Provider ↔ Tool loop |
| **Memory system** | Session model + session pruning | Persistent memory (redesigned 02/2026) | Long-term memory (MEMORY.md) | Persistent sessions per agent | Per-group `CLAUDE.md` + isolated filesystem | **SQLite hybrid search** (FTS5 + vector cosine), Lucid bridge, Markdown |
| **Tool system** | **Browser, Canvas, Nodes, Cron, Skills** | Built-in tools + MCP support | Built-in tools (file, exec, web) | Claude Code CLI / Codex CLI | Claude Code tools + web search | **Trait-based**: shell, file R/W, memory, browser (agent-browser/rust-native/computer-use), Composio |
| **Cấu trúc code** | Full-stack TypeScript monorepo | Modular Python packages | Single Go binary | TypeScript + Bash orchestration | ~8 source files | **Rust binary** — mọi subsystem là trait, swap qua config |
| **Extensibility** | **ClawHub** skills platform | Plugin SDK, MCP, dễ thêm provider | Đang phát triển | Agent config + team config | Claude Code Skills (`/add-*`) | **8 traits** (Provider, Channel, Memory, Tool, Observer, Runtime, Tunnel, Security) + TOML skill manifests |
| **Companion Apps** | ✅ **macOS, iOS, Android** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Container isolation** | Docker sandbox (non-main sessions) | ❌ | ❌ | ❌ | ✅ **Core design** — per group | ✅ Docker sandboxed runtime (optional) |
| **Identity system** | Markdown files | Markdown files | Markdown files | Config files | CLAUDE.md per group | **OpenClaw markdown + AIEOS v1.1 JSON** (portable AI identity) |

### 3.3. LLM Provider Support

| Provider | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **Anthropic (Claude)** | ✅ OAuth (Pro/Max) | ✅ API key | ⚠️ To be tested | ✅ (Claude Code CLI) | ✅ Claude Agent SDK | ✅ |
| **OpenAI** | ✅ OAuth (ChatGPT/Codex) | ✅ API key | ⚠️ To be tested | ✅ (Codex CLI) | ❌ | ✅ |
| **OpenRouter** (multi-model) | ❌ | ✅ | ⚠️ To be tested | ❌ | ❌ | ✅ |
| **DeepSeek** | ❌ | ✅ | ⚠️ To be tested | ❌ | ❌ | ✅ |
| **Gemini** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ (không đề cập) |
| **Zhipu (GLM)** | ❌ | ✅ | ✅ (primary) | ❌ | ❌ | ❌ |
| **Groq** | ❌ | ✅ (+ voice) | ✅ (+ voice) | ❌ | ❌ | ✅ |
| **Moonshot/Kimi** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **MiniMax** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Ollama (local)** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **vLLM (local)** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Mistral / xAI / Together / Fireworks / Perplexity / Cohere / Bedrock / Venice** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (tất cả) |
| **Custom OpenAI-compatible** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ (`custom:https://your-api.com`) |
| **Model failover/rotation** | ✅ **Auth rotation + fallback** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Tổng** | **2** (OAuth) | **13+** | **3-7** | **2** | **1** | **22+** (trait-based, no lock-in) |

> **Nhận xét:** **ZeroClaw vượt trội về số lượng provider (22+)** với kiến trúc trait-based — thêm provider mới chỉ cần implement `Provider` trait. nanobot vẫn mạnh về channels châu Á (Gemini, Zhipu, Moonshot). NanoClaw chỉ dùng Claude. OpenClaw cần subscription.

### 3.4. Kênh Chat (Channels)

| Channel | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **WhatsApp** | ✅ (Baileys) | ✅ | ❌ | ✅ | ✅ (primary, Baileys) | ✅ **(Business Cloud API)** |
| **Telegram** | ✅ (grammY) | ✅ | ✅ | ✅ | ❌ (RFS) | ✅ |
| **Discord** | ✅ (discord.js) | ✅ | ✅ | ✅ | ❌ (RFS) | ✅ |
| **Slack** | ✅ (Bolt) | ✅ | ❌ | ❌ | ❌ (RFS) | ✅ |
| **Google Chat** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Signal** | ✅ (signal-cli) | ❌ | ❌ | ❌ | ❌ | ❌ |
| **iMessage** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Microsoft Teams** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Matrix** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Zalo / Zalo Personal** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **WebChat** | ✅ (built-in Gateway) | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Webhook (generic)** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Gmail** | ❌ (Pub/Sub webhook) | ❌ | ❌ | ❌ | ✅ (skill) | ❌ |
| **Email (IMAP/SMTP)** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Feishu (飞书)** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **DingTalk (钉钉)** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **QQ** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **LINE** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Mochat** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **CLI** | ✅ | ✅ | ✅ | ✅ | ✅ (Claude Code) | ✅ |
| **Tổng built-in** | **13+** | **10** | **6** | **4** | **2** | **8** (CLI, Telegram, Discord, Slack, iMessage, Matrix, WhatsApp, Webhook) |

> **Nhận xét:** OpenClaw dẫn đầu channels phương Tây (13+). ZeroClaw đứng thứ 2 với 8 channels built-in (bao gồm iMessage + Matrix + Webhook). nanobot dẫn đầu channels châu Á. NanoClaw chỉ có WhatsApp mặc định.

### 3.5. Tính năng nâng cao

| Tính năng | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **MCP (Model Context Protocol)** | ❌ (Skills riêng) | ✅ (02/2026) | ❌ | ❌ | ❌ | ❌ |
| **Skills/Plugin platform** | ✅ **ClawHub** | ✅ Skills loader | ❌ | ❌ | ✅ Claude Code Skills | ✅ **TOML skill manifests** + community packs |
| **Browser control** | ✅ **CDP Chrome** | ❌ | ❌ | ❌ | ❌ | ✅ **agent-browser / rust-native / computer-use** (3 backends) |
| **Live Canvas (A2UI)** | ✅ **Visual workspace** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Voice Wake + Talk Mode** | ✅ **Always-on speech** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Companion Apps** | ✅ **macOS, iOS, Android** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Scheduled Tasks (Cron)** | ✅ + webhooks | ✅ | ✅ | ❌ (heartbeat) | ✅ Recurring jobs | ❌ (dùng heartbeat) |
| **Heartbeat (proactive)** | ❌ (cron/webhooks) | ✅ | ✅ | ✅ | ❌ | ✅ **HEARTBEAT.md** periodic tasks |
| **Multi-agent / Swarms** | ✅ (session routing) | ❌ (single) | ❌ (single) | ✅ **Multi-team** | ✅ **Agent Swarms** | ❌ (single agent) |
| **Team collaboration** | ✅ (sessions_send) | ❌ | ❌ | ✅ **Chain + fan-out** | ✅ Agents in chat | ❌ |
| **Agent Social Network** | ❌ | ✅ (Moltbook) | ✅ (ClawdChat) | ❌ | ❌ | ❌ |
| **Web Search** | ✅ (browser) | ✅ (Brave) | ✅ (Brave+DDG) | ❌ | ✅ | ✅ (Brave + allowlist) |
| **Voice transcription** | ✅ (media) | ✅ (Groq) | ✅ (Groq) | ❌ | ❌ | ❌ |
| **Live TUI Dashboard** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Control UI (Web)** | ✅ **Dashboard** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Remote access / Tunnel** | ✅ **Tailscale** | ❌ | ❌ | ❌ | ❌ | ✅ **Cloudflare, Tailscale, ngrok, custom** (trait-based) |
| **Sender Pairing/Auth** | ✅ **DM pairing + doctor** | allowFrom whitelist | allowFrom whitelist | ✅ Pairing code | Trigger word | ✅ **6-digit pairing code** + bearer token + allowlists |
| **Group isolation** | ✅ (session isolation) | ❌ | ❌ | ✅ (per-agent) | ✅ **Per-group container** | ❌ |
| **Daemon / Service mode** | ✅ launchd/systemd | ❌ | ❌ | ✅ tmux | ❌ | ✅ **`zeroclaw daemon`** + `service install/start/stop` |
| **System diagnostics** | ✅ `openclaw doctor` | ❌ | ❌ | ❌ | ❌ | ✅ **`zeroclaw doctor`** + `channel doctor` |
| **Composio (1000+ OAuth apps)** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (opt-in) |
| **Encrypted secrets** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **Local key file encryption** |
| **50+ integrations** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **Registry across 9 categories** |

### 3.6. Bảo mật (Security)

| Tiêu chí | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **Isolation model** | Docker sandbox (non-main) | `restrictToWorkspace` | `restrict_to_workspace` (ON) | Isolated workspace per agent | ✅ **OS-level container** per group | ✅ **Multi-layer**: workspace scoping + Docker sandbox + forbidden paths + symlink detection |
| **DM policy** | ✅ **Pairing** + `doctor` | allowFrom whitelist | allowFrom whitelist | Pairing code | Trigger word | ✅ **6-digit pairing** + bearer token + empty allowlist = deny all |
| **Dangerous command blocking** | ✅ (sandbox denylist) | Không rõ | ✅ (block rm -rf...) | Không rõ | ✅ Bash trong container | ✅ **14 system dirs + 4 dotfiles blocked**, null byte injection blocked, symlink escape detection |
| **Security docs** | ✅ **Comprehensive** | ✅ (v0.1.3.post7) | ⚠️ Early dev | Cơ bản | ✅ `SECURITY.md` | ✅ **Security checklist** (4 items, tất cả pass) + `SECURITY.md` |
| **Tunnel integration** | ✅ **Tailscale** | ❌ | ❌ | ❌ | ❌ | ✅ **Cloudflare, Tailscale, ngrok, custom** (trait-based) |
| **Health check tool** | ✅ `openclaw doctor` | ❌ | ❌ | ❌ | ❌ | ✅ **`zeroclaw doctor`** + `channel doctor` |
| **Auditability** | ❌ (52+ modules) | ✅ (~4K dòng) | ✅ (Go binary nhỏ) | ❌ | ✅ **~8 files** | ✅ 1,017 tests, clippy 0 warnings |
| **Gateway exposure** | ⚠️ Có thể public | Không rõ | Không rõ | Không rõ | Không rõ | ✅ **127.0.0.1 mặc định**, từ chối 0.0.0.0 khi không có tunnel |
| **Encrypted secrets** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **API keys encrypted với local key file** |

> **Nhận xét:** **ZeroClaw có hệ thống bảo mật toàn diện nhất** — multi-layer (pairing + allowlists + workspace scoping + Docker sandbox + tunnel-only exposure + encrypted secrets + symlink detection). NanoClaw mạnh về container isolation per group. OpenClaw mạnh về DM pairing + Tailscale.

### 3.7. Hiệu năng & Tài nguyên

| Tiêu chí | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|---|---|---|---|---|---|
| **RAM** | **>1GB** (Node.js) | >100MB | <10MB | >100MB (Node.js) | Nhẹ (Node.js + containers) | **<5MB** (99% nhỏ hơn OpenClaw) |
| **Startup time** | >500s (0.8GHz) | >30s (Python) | <1s | Vài giây | Vài giây | **<10ms** (400x nhanh hơn OpenClaw) |
| **Binary/Package size** | ~28MB (dist) | Python package | ~8MB Go binary | Node.js project | ~8 source files | **3.4MB** single binary |
| **Min hardware cost** | Mac Mini ~$599 | ~$50 (Linux SBC) | **$10** | Mac/Linux machine | Mac/Linux machine | **$10** (ARM, x86, RISC-V) |
| **Daemon mode** | ✅ launchd/systemd | ❌ | ❌ | ✅ tmux | ❌ | ✅ **`zeroclaw daemon`** + `service install/start/stop/status` |
| **Cross-platform binary** | ❌ (cần Node.js) | ❌ (cần Python) | ✅ Go binary | ❌ (cần Node.js) | ❌ (cần Node.js) | ✅ **ARM + x86 + RISC-V** single binary |

---

## 4. Phân tích SWOT cho từng giải pháp

### 🦞 OpenClaw — "The Original"

| | |
|---|---|
| **Strengths** | Full-featured nhất, production-ready, nhiều channel phương Tây nhất, browser control, Canvas/A2UI, Voice Wake, companion apps (macOS/iOS/Android), ClawHub skills, Tailscale remote access, bảo mật toàn diện, cộng đồng lớn nhất (145K+ stars), stable/beta/dev release channels |
| **Weaknesses** | Nặng nhất (>1GB RAM, >500s startup), codebase lớn khó customize, Windows chỉ qua WSL2, chỉ hỗ trợ Anthropic + OpenAI (cần subscription), không có MCP, thiếu channels châu Á |
| **Opportunities** | Đã là standard de facto, ClawHub ecosystem đang phát triển, companion apps tạo lợi thế mobile |
| **Threats** | Quá nặng cho nhiều use case, các bản lightweight (nanobot, PicoClaw) đang thu hút developer muốn đơn giản hơn |

### 🐈 nanobot — "The Researcher's Choice"

| | |
|---|---|
| **Strengths** | Nhiều LLM provider nhất (13+), nhiều channel châu Á nhất, MCP support, research-ready, dễ extend, Windows-friendly nhất, cộng đồng tốt (HKU backing) |
| **Weaknesses** | Single-agent only, Python startup chậm, RAM cao hơn PicoClaw, thiếu browser control/Canvas/Voice |
| **Opportunities** | MCP ecosystem đang phát triển, phù hợp làm nền tảng nghiên cứu AI agent, thị trường châu Á |
| **Threats** | Codebase nhỏ = ít tính năng enterprise, cạnh tranh từ OpenClaw gốc |

### 🦐 PicoClaw — "The Edge Runner"

| | |
|---|---|
| **Strengths** | Siêu nhẹ (<10MB), siêu nhanh (<1s boot), chạy trên hardware $10, Go binary portable, security sandbox tốt |
| **Weaknesses** | Early development, nhiều provider chưa test, ít channel, không có MCP/browser/Canvas, cộng đồng mới |
| **Opportunities** | IoT/Edge computing, home automation, server monitoring trên hardware rẻ |
| **Threats** | Chưa ổn định cho production, thiếu tính năng so với nanobot và OpenClaw |

### 🦞 TinyClaw — "The Team Orchestrator"

| | |
|---|---|
| **Strengths** | **Multi-agent + multi-team** (duy nhất có team chain/fan-out), parallel processing, live TUI dashboard, pairing system |
| **Weaknesses** | **Không hỗ trợ Windows native**, phụ thuộc Claude Code/Codex CLI (cần subscription), ít provider (2), ít channel (4) |
| **Opportunities** | Team workflow automation, complex multi-step tasks |
| **Threats** | Phụ thuộc vào CLI tools bên thứ 3, experimental stability |

### 🔬 NanoClaw — "The Security Purist"

| | |
|---|---|
| **Strengths** | **Codebase nhỏ nhất** (~8 files, đọc hiểu 8 phút), **OS-level container isolation** (không phải application-level), Agent Swarms (first to support), AI-native workflow (Claude Code làm mọi thứ), triết lý "skills over features", per-group memory isolation, auditability cao nhất |
| **Weaknesses** | **Chỉ hỗ trợ Claude** (1 provider duy nhất, cần subscription), **chỉ có WhatsApp** mặc định, không Windows native, không browser control/Canvas/Voice, phụ thuộc Claude Code, cộng đồng nhỏ |
| **Opportunities** | Security-first use cases, developer muốn hiểu toàn bộ code mình chạy, Agent Swarms là tính năng mới của Claude Code |
| **Threats** | Quá opinionated (chỉ Claude, chỉ WhatsApp), cộng đồng nhỏ, phụ thuộc hoàn toàn vào Anthropic ecosystem |

### 🦀 ZeroClaw — "The Rust Powerhouse"

| | |
|---|---|
| **Strengths** | **Rust binary 3.4MB, <5MB RAM, <10ms startup**, **22+ LLM providers** (nhiều nhất), **Windows native**, 8 channels built-in, trait-based architecture (swap mọi thứ), bảo mật multi-layer (pairing + sandbox + allowlists + tunnel + encrypted secrets), **3 browser backends**, daemon/service mode, `zeroclaw doctor`, Composio (1000+ OAuth apps), AIEOS identity, 1,017 tests, 50+ integrations |
| **Weaknesses** | Cần Rust toolchain để build (không có prebuilt binary), không có Canvas/A2UI/Voice Wake, không có companion apps, không có MCP, không multi-agent/swarms, thiếu channels châu Á (Feishu, DingTalk, QQ), cộng đồng nhỏ hơn OpenClaw/nanobot, Apache 2.0 (không phải MIT) |
| **Opportunities** | **Windows + Edge/IoT market** (thay thế cả nanobot lẫn PicoClaw), trait-based extensibility thu hút contributors, Composio mở rộng 1000+ integrations, AIEOS portable identity |
| **Threats** | Cạnh tranh trực tiếp với nanobot (provider flexibility) và PicoClaw (edge/lightweight), Rust learning curve cho contributors, chưa có prebuilt binaries |

---

## 5. Ma trận quyết định cho Software Developer / Tech Lead (Windows)

### Điểm số (1-5, 5 = tốt nhất)

| Tiêu chí (Trọng số) | 🦞 OpenClaw | 🐈 nanobot | 🦐 PicoClaw | 🦞 TinyClaw | 🔬 NanoClaw | 🦀 ZeroClaw |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Windows compatibility** (×2) | ⭐️3 | ⭐️5 | ⭐️3 | ⭐️1 | ⭐️1 | ⭐️5 |
| **Ease of setup** (×1.5) | ⭐️4 | ⭐️5 | ⭐️3 | ⭐️2 | ⭐️4 | ⭐️3 |
| **LLM provider flexibility** (×1.5) | ⭐️2 | ⭐️5 | ⭐️2 | ⭐️2 | ⭐️1 | ⭐️5 |
| **Channel integration** (×1) | ⭐️5 | ⭐️5 | ⭐️3 | ⭐️3 | ⭐️2 | ⭐️4 |
| **Multi-agent / Swarms** (×1.5) | ⭐️4 | ⭐️2 | ⭐️2 | ⭐️5 | ⭐️4 | ⭐️1 |
| **Security & Isolation** (×1) | ⭐️5 | ⭐️4 | ⭐️5 | ⭐️3 | ⭐️5 | ⭐️5 |
| **Performance/Resource** (×0.5) | ⭐️1 | ⭐️3 | ⭐️5 | ⭐️3 | ⭐️4 | ⭐️5 |
| **Feature richness** (×1.5) | ⭐️5 | ⭐️3 | ⭐️2 | ⭐️3 | ⭐️2 | ⭐️4 |
| **Extensibility (skills, plugins)** (×1.5) | ⭐️5 | ⭐️5 | ⭐️2 | ⭐️2 | ⭐️4 | ⭐️5 |
| **Auditability / Code clarity** (×1) | ⭐️2 | ⭐️4 | ⭐️4 | ⭐️3 | ⭐️5 | ⭐️4 |
| **Community & Stability** (×1) | ⭐️5 | ⭐️4 | ⭐️3 | ⭐️2 | ⭐️2 | ⭐️3 |
| **Documentation** (×0.5) | ⭐️5 | ⭐️4 | ⭐️4 | ⭐️4 | ⭐️3 | ⭐️4 |
| | | | | | | |
| **Tổng điểm (có trọng số)** | **47.5** | **52.0** | **35.5** | **30.0** | **35.0** | **53.0** |

> **Ghi chú:** **ZeroClaw vươn lên #1 (53.0 điểm)** nhờ Windows native, 22+ providers, bảo mật multi-layer, hiệu năng vượt trội, và extensibility trait-based. Điểm trừ chủ yếu: cần Rust toolchain để build (ease of setup), không có multi-agent/swarms, cộng đồng nhỏ hơn OpenClaw. nanobot vẫn là #2 nhờ ease of setup (pip install) và MCP support.

---

## 6. Khuyến nghị

### 🏆 Lựa chọn #1: **ZeroClaw** — Best Overall cho Dev/Tech Lead trên Windows

**Lý do:**
- **Windows native** — Rust binary chạy trực tiếp, không cần WSL2/Python/Node.js
- **22+ LLM providers** — nhiều nhất (OpenRouter, Anthropic, OpenAI, Ollama, Groq, DeepSeek, Mistral, xAI, Together, Fireworks, Perplexity, Cohere, Bedrock, Venice...)
- **Hiệu năng vượt trội** — 3.4MB binary, <5MB RAM, <10ms startup
- **Bảo mật multi-layer** — pairing + allowlists + workspace scoping + Docker sandbox + tunnel-only + encrypted secrets
- **Trait-based architecture** — swap mọi subsystem (provider, channel, memory, tool, tunnel...) qua config
- **8 channels built-in** — Telegram, Discord, Slack, WhatsApp, iMessage, Matrix, Webhook, CLI
- **Browser control** — 3 backends (agent-browser, rust-native, computer-use)
- **Daemon/Service mode** — `zeroclaw daemon` + `service install/start/stop`
- **`zeroclaw doctor`** + `channel doctor` cho diagnostics

**Phù hợp khi:**
- Dùng Windows và muốn **native binary** không cần runtime (Python/Node.js)
- Cần **nhiều LLM provider** và muốn swap linh hoạt
- Quan tâm đến **bảo mật** và **hiệu năng**
- Muốn deploy trên **nhiều platform** (Windows, Linux, ARM, RISC-V)
- Sẵn sàng cài Rust toolchain để build

**Hạn chế cần lưu ý:**
- ⚠️ Cần Rust toolchain để build (chưa có prebuilt binary)
- ⚠️ Không có multi-agent/swarms
- ⚠️ Không có Canvas/A2UI, Voice Wake, companion apps
- ⚠️ Thiếu channels châu Á (Feishu, DingTalk, QQ)

### 🥈 Lựa chọn #2: **nanobot** — Best Easy-Setup cho Windows

**Lý do:**
- **Cài đặt đơn giản nhất** — `pip install nanobot-ai` (không cần build)
- **13+ LLM providers** — linh hoạt chọn model phù hợp budget (OpenRouter, DeepSeek, Groq free tier...)
- **MCP support** — tương thích với hệ sinh thái tool server đang phát triển
- **Research-ready** — code sạch ~4,000 dòng, dễ đọc, dễ customize
- **Channels châu Á** — Feishu, DingTalk, QQ, Mochat nếu cần

**Phù hợp khi:**
- Không muốn cài Rust toolchain, chỉ cần `pip install`
- Cần MCP support hoặc channels châu Á
- Budget-conscious (dùng OpenRouter, Groq free tier, DeepSeek...)
- Muốn extend/customize agent behavior cho nhu cầu riêng

### � Lựa chọn #3: **OpenClaw** — Best Feature-Rich cho Power User

**Lý do:**
- **Full-featured nhất** — browser control, Canvas/A2UI, Voice Wake, companion apps
- **Production-ready** — stable release channel, `openclaw doctor`, comprehensive docs
- **Nhiều channel phương Tây nhất** — Signal, iMessage, MS Teams, Google Chat, Matrix, Zalo
- **Bảo mật toàn diện** — Docker sandbox, Tailscale, DM pairing mặc định
- **Remote access** — Tailscale Serve/Funnel cho truy cập từ xa

**Phù hợp khi:**
- Sẵn sàng dùng WSL2 (hoặc có thêm Mac/Linux machine)
- Đã có Anthropic Pro/Max hoặc ChatGPT Plus subscription
- Cần browser automation, voice control, hoặc mobile companion apps
- Cần kết nối Signal, iMessage, MS Teams, Google Chat
- Muốn giải pháp production-grade với community lớn nhất

**Hạn chế cần lưu ý:**
- ⚠️ Windows chỉ qua WSL2
- ⚠️ Nặng (>1GB RAM), cần máy mạnh
- ⚠️ Chỉ hỗ trợ Anthropic + OpenAI (cần subscription, không có free tier)
- ⚠️ Codebase lớn, khó customize

### Lựa chọn #4: **TinyClaw** — Best cho Multi-Agent Team Workflow

**Lý do:**
- **Multi-agent + multi-team** duy nhất — phù hợp workflow phức tạp
- **Team collaboration** — agents tự handoff công việc (chain + fan-out)
- **Live TUI dashboard** — monitoring real-time

**Phù hợp khi:**
- Cần orchestrate nhiều AI agent chuyên biệt (@coder, @writer, @reviewer...)
- Sẵn sàng dùng WSL2 trên Windows
- Đã có Claude Pro/Codex subscription

**Hạn chế cần lưu ý:**
- ❌ Không hỗ trợ Windows native — **bắt buộc WSL2 + tmux + Bash 4.0+**
- ❌ Phụ thuộc Claude Code CLI hoặc Codex CLI (cần subscription)
- ❌ Experimental, chưa ổn định

### Lựa chọn #5: **NanoClaw** — Best cho Security-First Developer

**Lý do:**
- **Codebase nhỏ nhất** — ~8 files, đọc hiểu toàn bộ trong 8 phút
- **OS-level container isolation** — bảo mật thực sự (không phải application-level checks)
- **Agent Swarms** — first personal AI assistant hỗ trợ teams of agents
- **AI-native** — Claude Code làm mọi thứ: setup, debug, customize
- **Skills over features** — fork + customize thay vì config

**Phù hợp khi:**
- Bạn là developer muốn **hiểu toàn bộ code** mình đang chạy
- Cần **container isolation thực sự** (không chỉ workspace restriction)
- Đã có Claude Code subscription và dùng macOS/Linux
- Thích triết lý "fork and customize" hơn là "configure a generic system"

**Hạn chế cần lưu ý:**
- ❌ **Không hỗ trợ Windows** (cần WSL2, skill chưa implement)
- ❌ **Chỉ hỗ trợ Claude** (1 provider duy nhất, cần subscription)
- ❌ **Chỉ có WhatsApp** mặc định (các channel khác qua skills chưa có)
- ❌ Cộng đồng nhỏ, còn mới

### Lựa chọn #6: **PicoClaw** — Best cho Edge/IoT/Home Server

**Lý do:**
- Siêu nhẹ (<10MB RAM), siêu nhanh (<1s boot) — chạy trên hardware $10
- Single Go binary, dễ deploy cross-platform
- Security sandbox mặc định

**Phù hợp khi:**
- Muốn deploy AI assistant trên Raspberry Pi, NAS, hoặc home server
- Cần assistant nhẹ cho server monitoring
- Quan tâm đến resource efficiency

**Hạn chế cần lưu ý:**
- ⚠️ Early development, chưa sẵn sàng production
- ⚠️ Nhiều provider chưa được test
- ⚠️ Ít tính năng hơn nanobot và OpenClaw đáng kể

---

## 7. Chiến lược kết hợp (cho Tech Lead)

Với vai trò Tech Lead, bạn có thể cân nhắc chiến lược kết hợp:

```
┌──────────────────────────────────────────────────────────────┐
│  Development Machine (Windows) — PRIMARY                     │
│  ├── ZeroClaw (main assistant, native Windows)              │
│  │    ├── 22+ providers (OpenRouter, Ollama local...)        │
│  │    ├── Telegram/Discord/Slack/WhatsApp integration       │
│  │    ├── Browser control (3 backends)                      │
│  │    ├── Daemon mode + encrypted secrets                   │
│  │    └── Composio cho 1000+ OAuth integrations             │
│  │                                                            │
│  └── nanobot (backup / MCP / channels châu Á)              │
│       ├── MCP tools cho IDE workflow                         │
│       └── Feishu/DingTalk/QQ nếu team dùng                  │
├──────────────────────────────────────────────────────────────┤
│  Mac/Linux Workstation (nếu có)                              │
│  ├── OpenClaw (full-featured power assistant)                │
│  │    ├── Voice Wake + Talk Mode + Canvas/A2UI              │
│  │    └── Signal/iMessage/MS Teams/iOS/Android               │
│  │                                                            │
│  └── NanoClaw (security-first, auditable)                   │
│       ├── Container isolation per WhatsApp group              │
│       └── Agent Swarms cho complex tasks                     │
├──────────────────────────────────────────────────────────────┤
│  Home Server / NAS / Edge Device (Linux)                     │
│  ├── ZeroClaw (nhẹ nhất, <5MB RAM, daemon mode)            │
│  └── PicoClaw (alternative, Go binary, <10MB RAM)           │
│       └── Heartbeat cho periodic health checks               │
├──────────────────────────────────────────────────────────────┤
│  Team Server (Linux/WSL2) — Khi cần multi-agent              │
│  └── TinyClaw (team workflow orchestration)                  │
│       ├── @coder, @reviewer, @writer agents                  │
│       └── Discord integration cho team                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Tổng kết nhanh — Chọn cái nào?

| Nếu bạn... | Chọn |
|---|---|
| Dùng **Windows**, muốn **native binary + nhiều provider nhất** | 🦀 **ZeroClaw** |
| Dùng **Windows**, muốn **cài đặt đơn giản nhất** (pip install) | 🐈 **nanobot** |
| Dùng **macOS**, muốn **full-featured, production-grade** | 🦞 **OpenClaw** |
| Cần **multi-agent team workflow** | 🦞 **TinyClaw** |
| Cần deploy trên **hardware rẻ / IoT / edge** | � **ZeroClaw** hoặc �🦐 **PicoClaw** |
| Muốn **hiểu toàn bộ code** + **container isolation thực sự** | 🔬 **NanoClaw** |
| Cần **browser automation** (3 backends) | 🦀 **ZeroClaw** |
| Cần **browser + voice control + Canvas** | 🦞 **OpenClaw** |
| **Budget-conscious**, không muốn subscription | 🐈 **nanobot** hoặc 🦀 **ZeroClaw** (OpenRouter/Groq) |
| Cần channels **châu Á** (Feishu, DingTalk, QQ) | 🐈 **nanobot** |
| Cần channels **phương Tây** (Signal, MS Teams, Zalo) | 🦞 **OpenClaw** |
| Muốn **Agent Swarms** + **AI-native workflow** | 🔬 **NanoClaw** |
| Cần **bảo mật multi-layer** + **encrypted secrets** | 🦀 **ZeroClaw** |
| Cần **1000+ OAuth app integrations** (Composio) | 🦀 **ZeroClaw** |
| Cần **daemon/service mode** + **system diagnostics** | 🦀 **ZeroClaw** |

---

## 9. Tham khảo

- [OpenClaw GitHub](https://github.com/openclaw/openclaw) · [Docs](https://docs.openclaw.ai)
- [nanobot GitHub](https://github.com/HKUDS/nanobot)
- [PicoClaw GitHub](https://github.com/sipeed/picoclaw)
- [TinyClaw GitHub](https://github.com/jlia0/tinyclaw)
- [NanoClaw GitHub](https://github.com/gavrielc/nanoclaw)
- [ZeroClaw GitHub](https://github.com/zeroclaw-labs/zeroclaw)
- [Evolution of OpenClaw, PicoClaw & Nanobot Systems — Sterlites](https://sterlites.com/blog/picoclaw-paradigm-edge-intelligence)
- [PicoClaw runs on 10MB RAM — CNX Software](https://www.cnx-software.com/2026/02/10/picoclaw-ultra-lightweight-personal-ai-assistant-run-on-just-10mb-of-ram/)
