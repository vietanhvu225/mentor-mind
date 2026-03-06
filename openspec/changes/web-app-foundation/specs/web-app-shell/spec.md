# Web App Shell

## Purpose
App layout, routing, and navigation components matching Stitch mockups.

## Requirements

### Requirement: App Sidebar
- Collapsed sidebar (60px width, icon-only)
- Icons: Dashboard, Articles, Search, Settings (bottom)
- Active state: Indigo highlight (#6366F1)
- Hover: tooltip showing page name
- Lucide React icons

### Requirement: Top Bar
- Search input (placeholder: "Search articles...")
- "Analyze" primary button (Indigo)
- User avatar (dropdown: profile, settings, logout)
- Sticky top

### Requirement: App Shell Layout
- Route group `(app)` wraps all authenticated pages
- Layout: sidebar left + topbar top + main content scrollable
- Responsive: sidebar hidden on mobile, hamburger toggle

### Requirement: Settings Layout
- Settings-specific sidebar nav (200px, left of content)
- 9 nav items: Profile, Auth, AI Config, Raindrop Sync, Analysis Team, Notifications, Data & Export, Integrations, Advanced
- Active item: Indigo text + left border
- Nested under `(app)/settings/`

### Requirement: Route Structure
- `/` → redirect to `/dashboard`
- `/dashboard` — S1 Dashboard page
- `/articles` — S2 Articles List page
- `/articles/[id]` — S3 Split-view Reader page
- `/settings` → redirect to `/settings/profile`
- `/settings/profile|auth|ai-config|raindrop|analysis-team|notifications|data-export|integrations|advanced`
- `/login` — S6 Login page (outside auth guard)

### Requirement: Page Shells
- Each page renders basic structure matching Stitch mockup layout
- Dashboard: stat cards row + heatmap + article grid
- Articles List: filter tabs + table
- Split-view Reader: resizable left/right panels
- Settings pages: form sections with cards
- Content is static/placeholder initially — wired to data in later changes

### Requirement: Modals
- Analyze Modal (Dialog): URL input + persona info + progress state
- Reflection Modal (Dialog): insight + action + confidence + voice + tags
- Triggered from TopBar ("Analyze" button) and article reader
- Uses shadcn/ui Dialog component
