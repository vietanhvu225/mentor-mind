# UI Mockups Spec

## Purpose
Stitch-generated visual mockups cho MentorMind V2 Phase 3A MVP screens.
Output: Approved visual direction → reference khi code.

**Stitch Project ID**: `16121599394031746314`
**Stitch Infrastructure**: `.stitch/metadata.json`, `.stitch/DESIGN.md`, `.stitch/SITE.md`

## Screens (11 total — all approved)

### S1: Dashboard
- **Layout**: Collapsed sidebar trái (60px, icon-only) + main content
- **Top bar**: Search input + "Analyze" Indigo button + user avatar
- **Stats bar**: 3 cards (streak days, total articles, avg confidence integer)
- **Heatmap**: "Learning Activity" GitHub-style contribution grid
- **Article grid**: 6 cards with title, date, source, status dot (🔴🟡🟢), confidence badge, tags, persona color dots
- **Screen ID**: `fea5396c08874d70ac16f318594a18b9`

### S2: Articles List
- **Layout**: Table view with 10 rows
- **Columns**: Title + source subtitle, Status, Confidence dot, Tags, Date, Actions
- **Filter tabs**: All / New / In Progress / Completed
- **Bulk select**: Checkboxes + "Analyze Selected" Indigo button
- **Sort**: Dropdown sort options
- **Screen ID**: `a8b28fd8226a4f9c9041a2ac31b317f4`

### S3: Split-view Reader
- **Left panel (50%)**: Rendered article markdown, code blocks with syntax highlighting, progress bar top
- **Right panel (50%)**: Tabs for 🔬 Scout / 🏗️ Builder / 🤔 Debater / 📝 Chief with badge counts
- **Chat input**: Sticky bottom, "Summon +" button for extended personas
- **Implications**: Highlighted box section
- **Related articles**: Bottom recommendations
- **Screen ID**: `8b6fd8b015a3412ca2e89003442d2c31`

### S4a: Analyze Modal (Input State)
- **Content**: URL input + "All 4 personas will analyze automatically" text + persona icons
- **Secondary**: "Or sync from Raindrop" link
- **Screen ID**: `20e19ac813f3437099c26f970f4b9e49`

### S4b: Analyze Modal (Progress State)
- **Content**: Pipeline visualization showing 4 persona analysis stages
- **Screen ID**: `08910e3a2dc2417799926a3ccb33837d`

### S5: Reflection Modal
- **Content**: Dark backdrop overlay + centered card
- **Fields**: Key insight textarea + Action item textarea + Confidence slider (1-10)
- **Voice input**: 🎤 Mic icon on each textarea
- **Tags**: Selectable tag chips
- **Screen ID**: `94beaf094db249a9a5bc4463bc39bda7`

### S6: Login (Hybrid Auth)
- **Logo**: `> MentorMind_` + "Your AI Learning Companion"
- **Primary**: [Sign in with Google] button
- **TOTP**: 6-digit OTP input boxes + "Verify Code" button
- **Collapsed**: "▸ More sign-in options" → email/password
- **Trust device**: "☑ Trust this device for 30 days"
- **Config**: `AUTH_PROVIDER` env var controls which modes visible
- **Screen ID**: `d9540c57b8134a728b3ee42364e5491b`

### S7: Settings (Main — Profile + Raindrop + Analysis Team)
- **Layout**: Collapsed app sidebar + Settings nav sidebar (200px) + content
- **Settings nav**: Profile / Auth / AI Config / Raindrop Sync / Analysis Team / Notifications / Data & Export / Integrations / Advanced
- **Profile section**: Avatar, name, email
- **Raindrop Sync**: Whitelist/Blacklist collection picker, sync schedule, stats
- **Analysis Team**: 4 core personas (Scout/Builder/Debater/Chief) with toggle + custom instructions
- **Screen ID**: `291168428aaa49f996a6a80681688ca1`

### S7a: Settings — Notifications
- **Telegram Bot**: Connected status, notification checkboxes
- **Email Digest**: Frequency dropdown, content checkboxes
- **Browser Push**: Enable/disable, type checkboxes
- **Quiet Hours**: Toggle + time range (22:00 → 07:00)
- **Screen ID**: `5dd429e94ed1438a8c89a5dd9781a8c1`

### S7b: Settings — Data & Export
- **Storage Overview**: Progress bars per data type
- **Quick Export**: JSON / CSV / JSON-LD / Markdown buttons
- **Automated Backups**: Toggle, frequency, file path, "Backup Now"
- **Import**: Backup restore + V1 migration
- **Danger Zone**: Red-bordered destructive actions
- **Screen ID**: `457a61a363df473cab31c83856f5ed4b`

### S7c: Settings — Integrations
- **Connected**: Raindrop.io + Telegram Bot (status + Configure/Disconnect)
- **Available**: Notion, Obsidian (vault path), Readwise, GitHub (2x2 grid)
- **API Access**: Masked API key + Copy/Regenerate + rate limit + docs link
- **Screen ID**: `e1f61beff9184e57a3182e5bacd148ee`

## Design System
- **Theme**: Dark mode (#1E1E1E bg, #252530 cards, #6366F1 Indigo accent)
- **Font**: Inter (UI), Fira Code (logo/code)
- **Border radius**: 12px cards, 8px buttons
- **Full design tokens**: `.stitch/DESIGN.md`

## Acceptance Criteria
- [x] All 11 screens approved by user via Party Mode review
- [x] Screens follow DESIGN_BRIEF.md color system
- [x] Dark mode primary throughout
- [x] Consistent component patterns across screens (sidebar, cards, modals)
- [x] Settings sidebar nav consistent (9 items) across all 4 settings sub-screens
