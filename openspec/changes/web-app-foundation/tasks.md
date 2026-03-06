# Tasks: web-app-foundation

## 1. Project Setup
- [ ] Init Next.js 15 with App Router (`pnpm create next-app@latest ./ --ts --app --eslint --tailwind --src-dir --import-alias "@/*"`)
- [ ] Configure strict TypeScript (`strict: true` in tsconfig)
- [ ] Install core deps: `@supabase/supabase-js @supabase/ssr @tanstack/react-query zustand otpauth lucide-react`
- [ ] Install dev deps: `prettier eslint-config-prettier husky lint-staged vitest @testing-library/react`
- [ ] Setup Husky pre-commit hooks + lint-staged
- [ ] Create `.env.local` from `.env.example` (Supabase credentials)

## 2. Design System (Tailwind + shadcn)
- [ ] Init shadcn/ui (`pnpm dlx shadcn@latest init` — dark mode, CSS variables)
- [ ] Configure `tailwind.config.ts` with custom tokens from `.stitch/DESIGN.md`
- [ ] Setup `globals.css` CSS variables (dark mode default, HSL colors)
- [ ] Setup fonts: Inter + Fira Code via `next/font/google`
- [ ] Install shadcn components: Button, Card, Dialog, Table, Tabs, Input, Textarea, Checkbox, Slider, Toggle, Select, Badge, Avatar, Separator, Dropdown Menu, Tooltip, Skeleton, Label
- [ ] Build `ConfidenceDot` component (8px circle, red/amber/green)
- [ ] Build `StatCard` component (icon + label + value)
- [ ] Build `PersonaTab` component (emoji + name + badge)
- [ ] Build `Heatmap` component (CSS Grid contribution chart)

## 3. App Shell Layout
- [ ] Build `AppSidebar` — collapsed 60px, Lucide icons, active state Indigo, tooltip hover
- [ ] Build `TopBar` — search input + Analyze button + Avatar dropdown
- [ ] Build `AppShell` — compose sidebar + topbar + main content area
- [ ] Build `SettingsSidebar` — 9-item nav, active Indigo border
- [ ] Create `(app)/layout.tsx` — wraps all authenticated pages with AppShell
- [ ] Create `(auth)/layout.tsx` — minimal layout for login page

## 4. Routing & Page Shells
- [ ] `/` → redirect to `/dashboard`
- [ ] `/dashboard/page.tsx` — stat cards + heatmap + article card grid (static/placeholder data)
- [ ] `/articles/page.tsx` — filter tabs + article table (empty state)
- [ ] `/articles/[id]/page.tsx` — split-view reader shell (resizable panels)
- [ ] `/settings/page.tsx` → redirect to `/settings/profile`
- [ ] `/settings/profile/page.tsx` — avatar + name + email form
- [ ] `/settings/auth/page.tsx` — password change + 2FA config
- [ ] `/settings/ai-config/page.tsx` — model selection placeholder
- [ ] `/settings/raindrop/page.tsx` — whitelist/blacklist + sync schedule
- [ ] `/settings/analysis-team/page.tsx` — 4 persona cards with toggles
- [ ] `/settings/notifications/page.tsx` — S7a: Telegram, Email, Browser Push, Quiet Hours
- [ ] `/settings/data-export/page.tsx` — S7b: Storage, Export buttons, Backup, Danger Zone
- [ ] `/settings/integrations/page.tsx` — S7c: Connected/Available services, API Access
- [ ] `/settings/advanced/page.tsx` — debug info, logs

## 5. Modals
- [ ] Build `AnalyzeModal` — URL input + persona info text + progress state (Dialog)
- [ ] Build `ReflectionModal` — insight + action + confidence slider + tags (Dialog)
- [ ] Wire Analyze button in TopBar → opens AnalyzeModal
- [ ] Wire Reflect button in reader → opens ReflectionModal

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
