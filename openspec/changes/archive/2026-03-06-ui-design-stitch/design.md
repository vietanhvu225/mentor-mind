## Context

UI design phase cho MentorMind V2 web platform. Tạo visual mockups bằng Stitch trước khi code.
Design system đã có: DESIGN_BRIEF.md + design-system/mentormind-v2/MASTER.md.

## Technical Decisions

### Tool: Google Stitch (MCP)
- Generate screens từ text prompts, iterate với user feedback
- Device type: DESKTOP (primary)
- Output: Visual mockups (static images), không phải code

### Design System References
- **Colors**: Dark `#1E1E1E` bg, Indigo `#6366F1` primary, Amber `#F59E0B` secondary
- **Typography**: Inter (body) + Fira Code (code/metadata)
- **Components**: shadcn/ui patterns (cards, tabs, sidebar, modals)
- **Icons**: Its Hover (animated) + Lucide (fallback)

### Screen Architecture

#### S1: Dashboard (landing page after login)
```
┌──────┬──────────────────────────────────┐
│ SIDE │  Stats bar (streak, articles,    │
│ BAR  │  avg confidence)                 │
│      ├──────────────────────────────────┤
│ 📊   │  Article grid/list              │
│ 📖   │  ┌─────┐ ┌─────┐ ┌─────┐       │
│ 🎯   │  │Card │ │Card │ │Card │       │
│ 💬   │  │ 🟢  │ │ 🟡  │ │ 🔴  │       │
│ 📅   │  └─────┘ └─────┘ └─────┘       │
│ ⚙️   │  ┌─────┐ ┌─────┐ ┌─────┐       │
│      │  │Card │ │Card │ │Card │       │
│      │  └─────┘ └─────┘ └─────┘       │
└──────┴──────────────────────────────────┘
```

#### S2: Split-view Reader
```
┌──────┬─────────────────┬────────────────┐
│ SIDE │  Article (50%)  │  Analysis (50%)│
│ BAR  │                 │  ┌────────────┐│
│      │  [Rendered       │  │ 🔬 Scout   ││
│      │   markdown       │  │ 🏗️ Builder ││
│      │   content]       │  │ 🤔 Debater ││
│      │                 │  │ 📝 Chief   ││
│      │                 │  ├────────────┤│
│      │                 │  │ Chat input ││
│      │                 │  └────────────┘│
└──────┴─────────────────┴────────────────┘
```

#### S3: Analyze Modal (overlay)
```
┌────────────────────────────┐
│  Analyze New Article       │
│                            │
│  URL: [________________]   │
│                            │
│  [Analyze]                 │
│                            │
│  ── or ──                  │
│  Auto-sync from Raindrop   │
└────────────────────────────┘
```

#### S4: Reflection Modal (overlay)
```
┌────────────────────────────────┐
│  Reflect on: "Article Title"   │
│                                │
│  Key Insight:                  │
│  [________________________]    │
│                                │
│  Action Item:                  │
│  [________________________]    │
│                                │
│  Confidence: ──●────── 7/10   │
│                                │
│  [Save Reflection]             │
└────────────────────────────────┘
```

#### S5: Login
```
┌────────────────────────────┐
│       > MentorMind_        │
│                            │
│  Email: [______________]   │
│  Pass:  [______________]   │
│                            │
│  [Sign In]                 │
└────────────────────────────┘
```

### Stitch Workflow
1. Tạo project → get project ID
2. Generate mỗi screen với detailed prompt (inject MASTER.md context)
3. User review → feedback → edit_screens → iterate 2-3 rounds
4. Optional: generate_variants cho alternatives
5. Approved → move to code implementation

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Stitch output không match design system | Inject chi tiết colors, fonts, layout vào prompt |
| Static mockup không show interactions | Describe hover states, transitions trong prompt |
| Iterate nhiều lần tốn thời gian | Cap 3 rounds per screen, prioritize P0 screens |
