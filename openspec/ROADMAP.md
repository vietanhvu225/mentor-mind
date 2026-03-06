# OpenSpec Change Roadmap

> Mapped from [Personal AI Learning Assistant.md](file:///g:/Target/1-Personal%20AI%20Learning%20Assistant/Personal%20AI%20Learning%20Assistant.md) Phase Breakdown

## ✅ Completed

| # | Change | Phase | Status |
|---|--------|-------|--------|
| 1 | `select-llm-model` | Pre-1A | ✅ Archived 2026-02-15 |
| 2 | `setup-database` | 1A | ✅ Archived 2026-02-15 |
| 3 | `setup-telegram-bot` | 1A | ✅ Archived 2026-02-15 |
| 4 | `hardcoded-article-test` | 1A | ✅ Archived 2026-02-15 |
| 5 | `raindrop-integration` | 1B | ✅ Archived 2026-02-15 |
| 6 | `article-extractor` | 1B | ✅ Archived 2026-02-15 |
| 7 | `scheduler-and-commands` | 1B | ✅ Archived 2026-02-16 |
| 8 | `reflection-system` | 2 | ✅ Archived 2026-02-16 |
| 9 | `batch-digest` | 2 | ✅ Archived 2026-02-16 |
| 10 | `weekly-synthesis` | 3 | ✅ Archived 2026-02-16 |
| 11 | `i18n-support` | Enhancement | ✅ Archived 2026-02-17 |

## 📋 Phase 2 — AI Assistant Exploration

> Exploring AI Assistant frameworks to learn architecture patterns and enhance MentorMind.
> See [COMPARISON.md](file:///g:/Target/1-Personal%20AI%20Learning%20Assistant/COMPARISON.md) for full analysis.
> See [docs/research/ai-assistant-explore.md](file:///g:/Target/1-Personal%20AI%20Learning%20Assistant/docs/research/ai-assistant-explore.md) for explore notes.

### 2A: Study (Research — separate workspace `g:\Target\2-nanobot-study\`)
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 12 | `study-nanobot` | Install, use, read source. **Focus: multi-channel abstraction pattern** | 📋 Planned |
| 13 | `study-zeroclaw` | Study Rust/trait-based architecture concepts (optional) | 📋 Planned |

### 2B: Borrow Patterns (Apply to MentorMind)
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 14 | `channel-abstraction` | 🔥 Decouple from Telegram, create Channel ABC interface | 📋 Planned |
| 15 | `discord-integration` | 🔥 Add Discord channel (Pycord), run parallel with Telegram | 📋 Planned |
| 16 | `semantic-memory` | Semantic search across articles & insights | 📋 Planned |
| 17 | `proactive-reminders` | Spaced repetition, review nudges | 📋 Planned |

### 2C: Rebuild (Decide after 2B)
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 18 | `assistant-rebuild` | Rebuild MentorMind on AI Assistant framework | ❓ Decide after 2B |

### Optional — Enhancements
| # | Change | Scope |
|---|--------|-------|
| — | `web-search-grounding` | LLM verify factual claims via web search. Giải quyết knowledge cutoff. API: Google Search / SerpAPI / Tavily |

## 📋 Phase 3 — Web Platform (V2)

> Hybrid approach: Telegram (habit layer) + Web App (knowledge layer).
> See [MentorMind V2 — Web Platform.md](../MentorMind%20V2%20—%20Web%20Platform.md) for full vision + rationale.
> See [DESIGN_BRIEF.md](../DESIGN_BRIEF.md) for UI/UX design system.
> See [design-system/mentormind-v2/MASTER.md](../design-system/mentormind-v2/MASTER.md) for UUPM source of truth.

### 3A: Core Dashboard (MVP)
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 19 | `ui-design-stitch` | 🎨 Stitch mockups (11 screens): Dashboard, Articles List, Split-view Reader, Analyze Modal (2 states), Reflection Modal, Login (Hybrid Auth), Settings (Main + Notifications + Data & Export + Integrations). All Party Mode reviewed. Stitch Project: `16121599394031746314` | ✅ Done 2026-03-06 |

| 20 | `web-app-foundation` | Next.js 15 setup, Supabase DB + pgvector, auth, Tailwind + shadcn, CI/CD | 📋 Planned |
| 21 | `db-migration` | SQLite → PostgreSQL, migrate existing data, schema update | 📋 Planned |
| 22 | `article-dashboard` | Article grid/list view, filter by status/tags, learning stats, streak | 📋 Planned |
| 23 | `split-view-reader` | Article content + AI analysis tabs (Scout/Builder/Debater/Chief) side-by-side | 📋 Planned |
| 24 | `web-analyze-flow` | One-click analyze, reflection form (voice-enabled), **Raindrop sync** (hybrid whitelist/blacklist collection picker, sync schedule, new collection behavior) | 📋 Planned |
| 25 | `telegram-refactor` | Refactor bot to use shared cloud DB | 📋 Planned |

### 3B: Rich Experience
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 26 | `learning-analytics` | Heatmap, confidence chart, knowledge radar + **Temporal Truth** (confidence history, [Kronos](https://github.com/Ja1Denis/Kronos) pattern) + **Shadow Accounting** (token dashboard) | 📋 Planned |
| 27 | `search-and-tags` | Full-text search + pgvector semantic, auto-tag, faceted filter + **Auto-categorization** (topic tree, [memU](https://github.com/NevaMind-AI/memU) pattern) | 📋 Planned |
| 28 | `quiz-system` | Auto-generate quiz (4 types), grading, SRS feedback | 📋 Planned |
| 29 | `voice-interaction` | 🎤 Web Speech API: voice quiz answers, voice reflection input, voice chat | 📋 Planned |
| 30 | `weekly-visual` | Weekly synthesis rich page + batch overview + **Learning Drift Detection** (auto-alerts, [myBrAIn](https://github.com/lilium360/myBrAIn) pattern) | 📋 Planned |

### 3C: Knowledge Engine
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 31 | `knowledge-graph` | Visual topic connections (react-force-graph), related articles via pgvector | 📋 Planned |
| 32 | `persona-chat` | 💬 Mode A (per-article in split-view) + Mode B (cross-article). **Agentic Pointers** ([Kronos](https://github.com/Ja1Denis/Kronos)) + **Citations** ([SurfSense](https://github.com/MODSetter/SurfSense)) + **Context Budgeter** + **Proactive Context** ([memU](https://github.com/NevaMind-AI/memU)) + **Context-aware Analysis** ([myBrAIn](https://github.com/lilium360/myBrAIn)) | 📋 Planned |
| 33 | `spaced-repetition` | SRS for insights + quiz reschedule | 📋 Planned |
| 34 | `export-share` | PDF/DOCX/Markdown report + public profile + **Report Export** ([SurfSense](https://github.com/MODSetter/SurfSense) pattern) | 📋 Planned |

### 3D: Intelligence Layer (Phase 4+)
| # | Change | Scope | Status |
|---|--------|-------|--------|
| 35 | `configurable-analysis-team` | Default 4 core + on-demand summon 5 extended personas | 📋 Planned |
| 36 | `agent-voice-response` | 🔊 TTS (ElevenLabs/OpenAI), Learning Podcast ([SurfSense](https://github.com/MODSetter/SurfSense) pattern) | 📋 Planned |
| 37 | `strategic-intelligence` | Integration với Strategic Intelligence System | 📋 Planned |
