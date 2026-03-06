# Tasks: web-app-foundation

## 1. Project Setup
- [x] Init Next.js 15 with App Router (`pnpm create next-app@latest web --ts --app --eslint --tailwind --src-dir --import-alias "@/*" --use-pnpm`)
- [x] Configure strict TypeScript (`strict: true` in tsconfig)
- [x] Install core deps: `@supabase/supabase-js @supabase/ssr @tanstack/react-query zustand otpauth lucide-react`
- [ ] Install dev deps: `prettier eslint-config-prettier husky lint-staged vitest @testing-library/react`
- [ ] Setup Husky pre-commit hooks + lint-staged
- [x] Create `.env.local` from `.env.example` (Supabase credentials)

## 2. Design System (Tailwind + shadcn)
- [x] Init shadcn/ui (`pnpm dlx shadcn@latest init` — dark mode, CSS variables)
- [x] Configure Tailwind v4 with custom tokens from `.stitch/DESIGN.md`
- [x] Setup `globals.css` CSS variables (dark mode default, hex colors)
- [x] Setup fonts: Inter + Fira Code via `next/font/google`
- [x] Install shadcn components: Button, Card, Dialog, Table, Tabs, Input, Textarea, Checkbox, Slider, Toggle, Select, Badge, Avatar, Separator, Dropdown Menu, Tooltip, Skeleton, Label
- [x] Build `ConfidenceDot` component (8px circle, red/amber/green)
- [x] Build `StatCard` component (icon + label + value)
- [x] Build `PersonaTab` component (emoji + name + badge)
- [x] Build `Heatmap` component (CSS Grid contribution chart)

## 3. App Shell Layout
- [x] Build `AppSidebar` — collapsed 60px, Lucide icons, active state Indigo, tooltip hover
- [x] Build `TopBar` — search input + Analyze button + Avatar dropdown
- [x] Build `AppShell` — compose sidebar + topbar + main content area
- [x] Build `SettingsSidebar` — 9-item nav, active Indigo border
- [x] Create `(app)/layout.tsx` — wraps all authenticated pages with AppShell
- [x] Create `(auth)/login/page.tsx` — placeholder login page

## 4. Routing & Page Shells
- [x] `/` → redirect to `/dashboard`
- [x] `/dashboard/page.tsx` — stat cards + heatmap + recent articles (mock data)
- [x] `/articles/page.tsx` — filter tabs + article table with confidence dots
- [x] `/articles/[id]/page.tsx` — split-view reader with persona tabs
- [x] `/search/page.tsx` — search input + empty state
- [x] `/settings/page.tsx` → redirect to `/settings/profile`
- [x] `/settings/profile/page.tsx` — avatar + name + email form
- [x] `/settings/auth/page.tsx` — connected accounts + password change
- [x] `/settings/ai-config/page.tsx` — model selection dropdowns
- [x] `/settings/raindrop/page.tsx` — connection status + sync mode
- [x] `/settings/analysis-team/page.tsx` — 4 persona cards with toggles
- [x] `/settings/notifications/page.tsx` — channels + quiet hours
- [x] `/settings/data-export/page.tsx` — storage + export + backup + danger zone
- [x] `/settings/integrations/page.tsx` — connected/available services + API access
- [x] `/settings/advanced/page.tsx` — system info

## 5. Modals
- [x] Build `AnalyzeModal` — URL input + pipeline info + loading state (Dialog)
- [x] Build `ReflectionModal` — insight + action + confidence slider + tags (Dialog)
- [x] Wire Analyze button in TopBar → opens AnalyzeModal
- [x] Wire Reflect button in reader → opens ReflectionModal

## 6. Supabase Database
- [ ] Install Supabase CLI (`pnpm add -D supabase`)
- [ ] Init Supabase local: `npx supabase init`
- [ ] Write `supabase/migrations/001_initial_schema.sql` (7 tables + pgvector + RLS)
- [ ] Run migration against cloud Supabase (via Dashboard SQL Editor or CLI)
- [ ] Enable pgvector extension in Supabase Dashboard
- [ ] Generate TypeScript types: `npx supabase gen types typescript --project-id <id> > src/lib/supabase/types.ts`

## 7. Supabase Client
- [ ] Create `src/lib/supabase/client.ts` — browser client (`createBrowserClient()`)
- [ ] Create `src/lib/supabase/server.ts` — server client for RSC (`createServerClient()`)
- [ ] Create `src/lib/supabase/middleware.ts` — session refresh helper

## 8. Authentication
- [ ] Create `src/lib/auth/config.ts` — read AUTH_PROVIDER, export auth mode
- [ ] Create `src/lib/auth/provider.tsx` — AuthProvider context + useAuth hook
- [ ] Create `src/lib/auth/totp.ts` — TOTP verify function using `otpauth`
- [ ] Create `middleware.ts` (project root) — auth guard for `(app)` routes
- [ ] Build Login page (`/login/page.tsx`) matching Stitch S6 mockup
- [ ] Implement Google SSO flow (Supabase Auth)
- [ ] Implement email/password flow (collapsed section)
- [ ] Implement TOTP OTP flow (6-digit input)
- [ ] Implement "Trust device" cookie (30-day)
- [ ] Test: login → dashboard redirect, logout → login redirect

## 9. Data Layer
- [ ] Setup TanStack Query provider in root layout
- [ ] Create `src/hooks/use-articles.ts` — useArticles, useArticle(id)
- [ ] Create `src/hooks/use-analyses.ts` — useAnalyses(articleId)
- [ ] Create `src/hooks/use-reflections.ts` — useReflections(articleId)
- [ ] Create `src/hooks/use-auth.ts` — wrapper around AuthProvider
- [ ] Create `src/lib/stores/ui-store.ts` — Zustand: sidebar, modals, filters
- [ ] Create `src/lib/stores/settings-store.ts` — Zustand: user preferences

## 10. Seed Data
- [ ] Write `supabase/seed/export-v1.py` — read V1 SQLite, export articles/tags/analyses as JSON
- [ ] Run export script → save to `supabase/seed/data.json`
- [ ] Write `supabase/seed/seed.sql` — insert JSON data into Supabase tables
- [ ] Run seed against Supabase → verify data appears in dashboard

## 11. CI/CD & Deploy
- [ ] Create `vercel.json` (if needed, or use zero-config)
- [ ] Connect repo to Vercel
- [ ] Configure environment variables in Vercel Dashboard
- [ ] Deploy → verify production build works
- [ ] Verify preview deployments on PRs

## 12. Verify & Polish
- [ ] All pages render without errors
- [ ] Auth flow works end-to-end (login → dashboard → logout)
- [ ] Seed data visible in dashboard + articles list
- [ ] Settings pages render all sections
- [ ] Modals open/close correctly
- [ ] Dark theme consistent across all pages
- [ ] No TypeScript errors (`pnpm tsc --noEmit`)
- [ ] No lint errors (`pnpm lint`)
- [ ] Update README.md + README.vi.md with V2 web features
