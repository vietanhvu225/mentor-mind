## Why

MentorMind V1 chạy hoàn toàn qua Telegram — hiệu quả cho quick capture nhưng giới hạn về visualization, deep reading, và knowledge management. Phase 3A cần web platform để:

- **Rich UI**: Split-view reader, heatmaps, knowledge graph — không thể trên Telegram
- **Self-serve**: User truy cập dashboard bất kỳ lúc nào, không phụ thuộc bot commands
- **Scalable**: Web app cho phép thêm features (quiz, analytics, export) dễ dàng hơn
- **Hybrid**: Telegram (habit layer) + Web (knowledge layer) chạy song song

11 Stitch mockups đã approved (`#19 ui-design-stitch`). Cần foundation để bắt đầu implement.

## What

Setup full-stack web application foundation cho MentorMind V2, bao gồm:

### 1. Next.js 15 Project
- App Router + TypeScript + strict mode
- pnpm package manager
- Project structure: `src/app/`, `src/components/`, `src/lib/`, `src/hooks/`

### 2. Design System (Tailwind + shadcn/ui)
- Custom Tailwind config với tokens từ `.stitch/DESIGN.md`
- shadcn/ui components: Button, Card, Dialog, Table, Tabs, Input, Slider, Toggle, Badge, Avatar
- CSS variables cho dark mode (primary theme)
- Google Fonts: Inter + Fira Code

### 3. App Shell (match Stitch mockups)
- Collapsed sidebar (60px, icon-only, Lucide icons)
- Top bar (search input + "Analyze" button + user avatar)
- Settings layout (sidebar nav + content area)
- Responsive: Desktop-first, basic tablet/mobile breakpoints
- Route structure: `/dashboard`, `/articles`, `/articles/[id]`, `/settings/*`, `/login`

### 4. Supabase Backend
- Supabase project setup + environment config
- PostgreSQL schema (empty tables): users_profile, articles, article_analyses, reflections, tags, article_tags, user_settings, raindrop_collections
- pgvector extension enabled (article_embeddings table)
- Supabase client + TypeScript types generation
- Row Level Security (RLS) policies

### 5. Authentication
- Supabase Auth: Google SSO + email/password
- TOTP OTP (via `otpauth` library) — toggled via `AUTH_PROVIDER` env var
- Auth middleware (protected routes)
- Login page matching Stitch mockup (hybrid 3-mode)
- Session management + "Trust device" cookie

### 6. Data Layer
- TanStack Query (React Query) for server state (caching, fetching)
- Zustand for UI state (sidebar, modals, filters)
- Supabase Realtime subscription setup (future use)

### 7. CI/CD
- Vercel deployment (auto-deploy on push)
- Environment variables config (Supabase, auth, TOTP)
- Preview deployments for PRs

### 8. Seed Data (Real articles from V1)
- Export existing V1 articles (Raindrop-synced) → `seed/articles.json`
- Python export script using V1 SQLite DB
- Supabase seed script: insert articles, tags, sample analyses into empty tables
- Result: Dashboard shows real 128+ articles ngay sau setup
- No Raindrop API integration needed — one-time export only

### 9. Developer Experience
- ESLint + Prettier (strict config)
- Vitest + Testing Library (setup, no tests yet)
- Husky + lint-staged (pre-commit hooks)
- Zod schemas for runtime validation

## Không làm

- ❌ Business logic (article analysis, AI personas, reflection processing)
- ❌ Raindrop.io sync integration
- ❌ Data migration từ V1 SQLite → PostgreSQL (→ `#21 db-migration`)
- ❌ AI/LLM integration (Gemini API calls)
- ❌ Quiz system, knowledge graph, analytics charts
- ❌ Telegram bot refactor
- ❌ Full test coverage (chỉ setup framework)
- ❌ Mobile-optimized responsive (chỉ basic breakpoints)

## New Capabilities

- `web-app-shell`: App layout, routing, navigation components
- `web-auth`: Authentication flow (SSO + email + TOTP), middleware, session
- `web-database`: Supabase schema, client, TypeScript types, RLS policies
- `web-design-system`: Tailwind tokens, shadcn components, CSS variables

## Modified Capabilities

- `database-layer`: Add PostgreSQL/Supabase schema alongside existing SQLite (coexist, not replace)

## Impact

- **New dependency**: Next.js 15, Supabase, TanStack Query, Zustand, shadcn/ui
- **New infrastructure**: Vercel hosting, Supabase cloud project
- **Existing code**: No changes to V1 Python/Telegram code — fully independent
- **File structure**: New `src/` directory for web app code
