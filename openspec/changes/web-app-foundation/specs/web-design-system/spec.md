# Web Design System

## Purpose
Tailwind CSS tokens, shadcn/ui components, CSS variables, and typography matching Stitch mockups.

## Requirements

### Requirement: Tailwind Config
- Custom colors matching `.stitch/DESIGN.md`:
  - `bg-primary`: #1E1E1E, `bg-card`: #252530, `bg-sidebar`: #1A1A2E
  - `accent`: #6366F1 (Indigo), `accent-hover`: #818CF8
  - `success`: #10B981, `warning`: #F59E0B, `danger`: #EF4444
- Custom border-radius: `card` (12px), `button` (8px)
- Font families: `inter` (sans), `fira-code` (mono)

### Requirement: CSS Variables
- Dark mode as default (no toggle in MVP)
- Variables in `globals.css` using HSL format (shadcn convention)
- Map to shadcn component tokens: `--background`, `--foreground`, `--card`, `--primary`, etc.

### Requirement: Typography
- Google Fonts: Inter (400, 500, 600, 700) + Fira Code (600)
- Self-hosted via `next/font/google` (optimized loading)
- Heading: Inter Bold (24-32px)
- Body: Inter Regular (14-16px)
- Labels: Inter Medium (12-13px)
- Code/Logo: Fira Code SemiBold (16-20px)

### Requirement: shadcn/ui Components
Install and configure these components:
- **Layout**: Card, Separator
- **Forms**: Button, Input, Textarea, Checkbox, Slider, Toggle, Select, Label
- **Overlay**: Dialog, Dropdown Menu, Tooltip
- **Data**: Table, Tabs, Badge, Avatar
- **Feedback**: Skeleton (loading states)

All components styled to match dark theme via CSS variable overrides.

### Requirement: Custom Components
Beyond shadcn, build these project-specific components:
- `ConfidenceDot`: 8px circle, color based on 1-10 score (red/amber/green)
- `StatCard`: icon + label + value, card background
- `PersonaTab`: emoji + name + badge count, colored indicator per persona
- `Heatmap`: GitHub-style contribution grid (CSS Grid, no external lib)

### Requirement: Icon System
- Lucide React for all icons
- Consistent 20px size in sidebar
- Icon map: Dashboard (LayoutDashboard), Articles (FileText), Search (Search), Settings (Settings), Analyze (Sparkles), etc.
