# UI Mockups Spec

## Purpose
Stitch-generated visual mockups cho MentorMind V2 Phase 3A MVP screens.
Output: Approved visual direction → reference khi code.

## Screens

### S1: Dashboard
- **Layout**: Sidebar trái (icon-only, expandable) + main content
- **Stats bar**: 3 cards (streak, total articles, avg confidence) top
- **Article grid**: Cards with title, date, status dot (🔴🟡🟢), confidence badge, tags
- **Filters**: Status, date range, tags — toolbar phía trên grid
- **Empty state**: CTA "Analyze your first article"
- **Dark mode**: `#1E1E1E` bg, `#252530` cards, Indigo accents

### S2: Split-view Reader
- **Left panel (50%)**: Rendered markdown article content, scrollable
- **Right panel (50%)**: Tabs for Scout (blue), Builder (green), Debater (red), Chief (amber)
- **Tab content**: Markdown-rendered AI analysis per persona
- **Bottom of right panel**: Chat input cho persona chat (Mode A)
- **Resizable**: Drag divider between panels
- **Article metadata bar**: Title, source URL, date, confidence, status

### S3: Analyze Modal
- **Trigger**: "+" button hoặc ⌘N
- **Content**: URL input field + "Analyze" button
- **Progress state**: Loading spinner + "Analyzing with 4 personas..."
- **Done state**: Success message + "View Analysis" button
- **Secondary**: "Or sync from Raindrop" link

### S4: Reflection Modal
- **Trigger**: Button trong split-view reader
- **Content**: Article title header + 3 fields:
  - Key insight (textarea)
  - Action item (textarea)
  - Confidence slider (1-10 with labels)
- **Voice input**: Mic icon trên mỗi textarea
- **Submit**: "Save Reflection" button

### S5: Login
- **Minimal**: Logo `> MentorMind_` + email/password + sign in button
- **Dark bg**: Centered card, subtle border
- **No registration**: Single user, pre-configured

## Acceptance Criteria
- [ ] Mỗi screen approved bởi user (max 3 iteration rounds)
- [ ] Screens follow MASTER.md color system
- [ ] Dark mode primary, with consideration for light mode
- [ ] Consistent component patterns across screens
