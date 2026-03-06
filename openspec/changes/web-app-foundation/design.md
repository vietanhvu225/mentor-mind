# Design: web-app-foundation

## Goals

- Scaffold production-ready Next.js 15 app matching Stitch mockups
- Establish design system, auth, database, and data layer patterns
- Seed with real V1 data for immediate testing
- Zero V1 code changes — fully independent web app

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Vercel                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Next.js 15 (App Router)              │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │  │
│  │  │  Pages   │  │   API    │  │  Middleware     │  │  │
│  │  │ (React)  │  │  Routes  │  │  (Auth guard)  │  │  │
│  │  └────┬─────┘  └────┬─────┘  └────────────────┘  │  │
│  │       │              │                             │  │
│  │  ┌────▼──────────────▼──────────────────────────┐ │  │
│  │  │            Client Libraries                   │ │  │
│  │  │  Supabase Client │ TanStack Query │ Zustand  │ │  │
│  │  └────┬─────────────┴───────────────────────────┘ │  │
│  └───────┼───────────────────────────────────────────┘  │
└──────────┼──────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│                    Supabase Cloud                        │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐│
│  │PostgreSQL│  │   Auth   │  │      pgvector          ││
│  │  + RLS   │  │(Google+  │  │  (article_embeddings)  ││
│  │          │  │email+OTP)│  │                        ││
│  └──────────┘  └──────────┘  └────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
mentor-mind/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── (auth)/                   # Auth layout group
│   │   │   └── login/page.tsx        # Login (hybrid: Google + OTP + email)
│   │   ├── (app)/                    # Authenticated layout group
│   │   │   ├── layout.tsx            # App Shell (sidebar + topbar)
│   │   │   ├── dashboard/page.tsx    # S1: Dashboard
│   │   │   ├── articles/
│   │   │   │   ├── page.tsx          # S2: Articles List
│   │   │   │   └── [id]/page.tsx     # S3: Split-view Reader
│   │   │   └── settings/
│   │   │       ├── page.tsx          # S7: Settings Main (redirect → profile)
│   │   │       ├── profile/page.tsx
│   │   │       ├── auth/page.tsx
│   │   │       ├── ai-config/page.tsx
│   │   │       ├── raindrop/page.tsx
│   │   │       ├── analysis-team/page.tsx
│   │   │       ├── notifications/page.tsx    # S7a
│   │   │       ├── data-export/page.tsx      # S7b
│   │   │       ├── integrations/page.tsx     # S7c
│   │   │       └── advanced/page.tsx
│   │   ├── layout.tsx                # Root layout (providers, fonts)
│   │   └── globals.css               # CSS variables + base styles
│   │
│   ├── components/
│   │   ├── ui/                       # shadcn/ui components (auto-generated)
│   │   ├── layout/
│   │   │   ├── app-sidebar.tsx       # Collapsed sidebar (60px)
│   │   │   ├── top-bar.tsx           # Search + Analyze + Avatar
│   │   │   ├── settings-sidebar.tsx  # Settings nav (9 items)
│   │   │   └── app-shell.tsx         # Composed layout wrapper
│   │   ├── articles/
│   │   │   ├── article-card.tsx      # Dashboard article card
│   │   │   ├── article-table.tsx     # Articles list table
│   │   │   └── article-reader.tsx    # Split-view reader shell
│   │   ├── modals/
│   │   │   ├── analyze-modal.tsx     # S4: Analyze (input + progress)
│   │   │   └── reflection-modal.tsx  # S5: Reflection form
│   │   └── shared/
│   │       ├── confidence-dot.tsx    # 🔴🟡🟢 status indicator
│   │       ├── heatmap.tsx           # Learning activity grid
│   │       ├── stat-card.tsx         # Dashboard stat cards
│   │       └── persona-tab.tsx       # AI persona tab component
│   │
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts             # Browser client
│   │   │   ├── server.ts             # Server client (RSC)
│   │   │   ├── middleware.ts          # Auth middleware helper
│   │   │   └── types.ts              # Generated DB types
│   │   ├── auth/
│   │   │   ├── provider.tsx           # Auth context provider
│   │   │   ├── totp.ts               # TOTP verification logic
│   │   │   └── config.ts             # AUTH_PROVIDER env routing
│   │   ├── stores/
│   │   │   ├── ui-store.ts           # Zustand: sidebar, modals, filters
│   │   │   └── settings-store.ts     # Zustand: user preferences
│   │   └── utils.ts                  # Shared utilities (cn, formatDate, etc.)
│   │
│   ├── hooks/
│   │   ├── use-articles.ts           # TanStack Query: articles CRUD
│   │   ├── use-analyses.ts           # TanStack Query: analyses
│   │   ├── use-reflections.ts        # TanStack Query: reflections
│   │   └── use-auth.ts              # Auth state hook
│   │
│   └── types/
│       ├── article.ts                # Article, Analysis, Reflection types
│       ├── persona.ts                # Persona enum + config
│       └── settings.ts               # Settings types
│
├── supabase/
│   ├── migrations/
│   │   └── 001_initial_schema.sql    # Full schema + pgvector + RLS
│   └── seed/
│       ├── export-v1.py              # Python: SQLite → JSON export
│       └── seed.sql                  # Insert seed data
│
├── public/
│   └── fonts/                        # Inter + Fira Code (self-hosted)
│
├── tailwind.config.ts                # Custom theme tokens
├── components.json                   # shadcn/ui config
├── .env.example                      # Environment template
├── .env.local                        # Local secrets (gitignored)
└── vercel.json                       # Vercel config
```

## Data Flow

### Auth Flow
```
User → /login
  ├─ AUTH_PROVIDER=supabase → [Google SSO] or [Email/Password]
  │   └─ Supabase Auth → session cookie → redirect /dashboard
  ├─ AUTH_PROVIDER=totp → [6-digit OTP input]
  │   └─ Verify via otpauth library → custom session → redirect /dashboard
  └─ AUTH_PROVIDER=both → Show all 3 options

Middleware (every request):
  → Check session → valid? continue : redirect /login
  → "Trust device" cookie → skip OTP for 30 days
```

### Data Fetching (TanStack Query)
```
Page Component
  └─ useArticles() hook
       └─ TanStack Query
            └─ queryFn: supabase.from('articles').select(...)
                 └─ Supabase Client (with RLS)
                      └─ PostgreSQL

Cache strategy:
  - staleTime: 5 minutes (articles don't change often)
  - gcTime: 30 minutes
  - Optimistic updates for reflections
```

### UI State (Zustand)
```
ui-store:
  - sidebarCollapsed: boolean (default: true)
  - activeModal: 'analyze' | 'reflection' | null
  - articleFilters: { status, tags, sort }
  - settingsActiveTab: string
```

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| App Router vs Pages | App Router | Next.js 15 default, RSC, layouts, streaming |
| Supabase vs custom API | Supabase | Auth + DB + Realtime built-in, free tier generous |
| shadcn/ui vs custom | shadcn/ui | Copy-paste = full control, Radix primitives, dark mode |
| pnpm vs npm | pnpm | Faster installs, disk efficient, strict deps |
| Zustand vs Context | Zustand | DevTools, selectors (minimal re-renders), persist middleware |
| TanStack Query vs SWR | TanStack Query | DevTools, mutation support, richer cache control |
| Self-host fonts vs CDN | Self-host | Performance (no external requests), GDPR compliant |

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Supabase free tier limits (500MB DB, 50K auth) | Sufficient for single-user app, upgrade path clear |
| TOTP adds auth complexity | Feature-flagged via `AUTH_PROVIDER`, can disable entirely |
| Seed data schema mismatch with future changes | Schema versioned via Supabase migrations, seed is one-time dev tool |
| shadcn/ui updates may break customizations | Components are copied (not npm dep), full version control |
| pgvector extension availability | Supabase includes pgvector by default on all plans |
