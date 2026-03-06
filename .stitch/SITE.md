# MentorMind V2 — Site Map & Roadmap

> Vision: A personal AI learning companion for senior developers.
> Stitch Project ID: `16121599394031746314`

## 1. Vision

MentorMind V2 transforms passive article reading into active learning through multi-persona AI analysis, structured reflection, and knowledge graph visualization. The web platform provides rich visualizations and deep reading experiences alongside the existing Telegram bot for quick capture.

## 2. Tech Stack

- **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** Supabase (PostgreSQL + pgvector + Auth + Realtime)
- **AI:** Gemini 2.5 Pro (multi-persona analysis)
- **Integrations:** Raindrop.io, Telegram Bot

## 3. Auth Strategy

| Mode | Method | When |
|------|--------|------|
| `supabase` | Google SSO + email/password | Cloud deploy (default) |
| `totp` | 6-digit TOTP OTP | Self-hosted, internal |
| `both` | All above combined | Hybrid |

Config via `AUTH_PROVIDER` env var.

## 4. Sitemap (Designed Screens)

- [x] Dashboard — article grid, learning stats, streak, heatmap
- [x] Articles List — table view, filter tabs, bulk actions, sort
- [x] Split-view Reader — article content + AI analysis tabs
- [x] Analyze Modal (Input) — URL input, persona info
- [x] Analyze Modal (Progress) — pipeline visualization
- [x] Reflection Modal — insight, action, confidence, voice, tags
- [x] Login — hybrid auth (Google + OTP + email)
- [x] Settings (Main) — Profile + Raindrop Sync + Analysis Team
- [x] Settings (Notifications) — Telegram, Email, Browser Push, Quiet Hours
- [x] Settings (Data & Export) — Storage, Export, Backup, Danger Zone
- [x] Settings (Integrations) — Connected services, Available, API Access

## 5. Roadmap (Future Screens)

| Screen | Phase | Priority |
|--------|-------|----------|
| Learning Analytics (heatmap, radar, charts) | 3B | P1 |
| Quiz / Assessment results | 3B | P1 |
| Weekly Synthesis report | 3B | P1 |
| Knowledge Graph visualization | 3C | P2 |
| Persona Chat (full-screen) | 3C | P2 |
| Timeline view | 3C | P2 |
| Onboarding wizard | 3B | P2 |
| V1 Migration wizard | 3A | P1 |

## 6. Creative Freedom

Ideas for unique screens not yet in roadmap:
- **Learning Podcast** — TTS-generated audio summary of weekly learnings
- **Debate Arena** — Side-by-side comparison of Debater vs Builder perspectives
- **Knowledge Gaps** — AI-identified topics user should learn next
- **Study Plan** — Generated weekly reading plan based on goals
- **Achievement Badges** — Gamification: streaks, milestones, skill levels
