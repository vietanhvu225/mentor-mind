# MentorMind V2 — Stitch Design System

> Source of truth for all Stitch AI generation prompts.
> Extracted from DESIGN_BRIEF.md + approved Stitch mockups.

## 1. Brand Identity

- **App Name:** MentorMind V2
- **Logo:** `> MentorMind_` (terminal-style, monospace, blinking cursor)
- **Tagline:** "Your AI Learning Companion"
- **Audience:** Senior developers, tech leads

## 2. Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#1E1E1E` | Page background |
| `--bg-card` | `#252530` | Cards, panels |
| `--bg-sidebar` | `#1A1A2E` | Sidebar background |
| `--accent-primary` | `#6366F1` | Buttons, links, active states (Indigo) |
| `--accent-hover` | `#818CF8` | Hover state |
| `--text-primary` | `#FFFFFF` | Headings |
| `--text-secondary` | `#A0A0B0` | Body text, descriptions |
| `--text-muted` | `#6B7280` | Labels, timestamps |
| `--success` | `#10B981` | Connected, completed, high confidence |
| `--warning` | `#F59E0B` | In progress, medium confidence |
| `--danger` | `#EF4444` | Error, disconnected, danger zone |
| `--confidence-high` | `#10B981` | 8-10 score (green dot) |
| `--confidence-mid` | `#F59E0B` | 5-7 score (amber dot) |
| `--confidence-low` | `#EF4444` | 1-4 score (red dot) |

## 3. Typography

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Headings | Inter | 700 (Bold) | 24-32px |
| Body | Inter | 400 (Regular) | 14-16px |
| Labels | Inter | 500 (Medium) | 12-13px |
| Code / Logo | Fira Code | 600 (SemiBold) | 16-20px |
| Stats | Inter | 700 (Bold) | 28-36px |

## 4. Layout Patterns

### App Shell
```
┌──────┬──────────────────────────────────────┐
│ SIDE │           TOP BAR                     │
│ BAR  │  Search ────── [Analyze] [Avatar]    │
│ 60px ├──────────────────────────────────────┤
│      │                                      │
│ icon │           MAIN CONTENT               │
│ only │                                      │
│      │                                      │
│ ⚙️   │                                      │
└──────┴──────────────────────────────────────┘
```

### Settings Shell
```
┌──────┬──────────┬──────────────────────────┐
│ APP  │ SETTINGS │   SETTINGS CONTENT       │
│ SIDE │ NAV      │                          │
│ BAR  │ 200px    │   Active section         │
│ 60px │          │                          │
└──────┴──────────┴──────────────────────────┘
```

### Modal
- Centered card over dark backdrop overlay
- Max width: 480-600px
- Border-radius: 12px

## 5. Component Tokens

| Component | Style |
|-----------|-------|
| Cards | bg `#252530`, border-radius `12px`, padding `20px`, subtle border `#2A2A3E` |
| Buttons (primary) | bg `#6366F1`, text white, border-radius `8px`, padding `10px 20px` |
| Buttons (secondary) | border `#6366F1`, text `#6366F1`, bg transparent |
| Buttons (danger) | bg `#EF4444`, text white |
| Input fields | bg `#1A1A2E`, border `#2A2A3E`, border-radius `8px`, text white |
| Sidebar icons | 20px, color `#6B7280`, active: `#6366F1` |
| Tags/badges | bg `#2A2A3E`, text `#A0A0B0`, border-radius `4px`, padding `2px 8px` |
| Status dots | 8px circle, color mapped to confidence scale |
| Dividers | `#2A2A3E`, 1px solid |

## 6. Design System Notes for Stitch Generation

**COPY THIS BLOCK INTO EVERY STITCH PROMPT:**

```
DESIGN SYSTEM:
- Dark mode: background #1E1E1E, cards #252530, sidebar #1A1A2E
- Primary accent: Indigo #6366F1 (buttons, links, active states)
- Font: Inter for all UI, Fira Code for logo/code
- Border radius: 12px cards, 8px buttons/inputs
- Collapsed sidebar: 60px width, icons only, active icon in Indigo
- Top bar: search input + "Analyze" Indigo button + user avatar
- Text: white headings, #A0A0B0 body, #6B7280 labels
- Status: green #10B981 connected/high, amber #F59E0B medium, red #EF4444 low/error
- Confidence dots: 🟢 8-10, 🟡 5-7, 🔴 1-4 (integer only)
- Tags: small chips with #2A2A3E background
- Professional, developer-focused aesthetic
```

## 7. Persona Identifiers

| Persona | Emoji | Color | Role |
|---------|-------|-------|------|
| Scout | 🔬 | Green | Summary & key takeaways |
| Builder | 🏗️ | Blue | Action items & implementation |
| Debater | 🤔 | Orange | Critical analysis & counter-arguments |
| Chief | 📝 | Purple | Strategic synthesis & verdict |
