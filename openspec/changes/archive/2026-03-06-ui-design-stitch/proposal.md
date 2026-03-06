## Why

Phase 3A bắt đầu — cần visual mockups TRƯỚC khi code. Lý do:
- Xác định layout, proportions, component placement trước → code nhanh hơn, ít rework
- MentorMind V2 là web app hoàn toàn mới — cần thiết lập visual direction
- Design system đã có (MASTER.md + DESIGN_BRIEF.md) nhưng chưa được visualize thành screens

Tool: Google Stitch (MCP) — generate screens từ text prompts, iterate với feedback.

## What Changes

- **Tạo Stitch project "MentorMind V2"** với device type DESKTOP
- **Generate P0 screens** (core MVP):
  - Dashboard: article grid + learning stats + streak + heatmap
  - Articles List: all articles + filter tabs + bulk actions + sort
  - Split-view Reader: article content trái + AI analysis tabs (Scout/Builder/Debater/Chief) phải + Summon + Chat
  - Analyze Modal: URL input → progress (2 states)
  - Reflection Modal: insight + action items + confidence slider + voice + tags
  - Settings page: Raindrop sync (hybrid whitelist/blacklist), Analysis Team config, profile
  - Login page: simple auth
- **Iterate each screen** dựa trên user feedback (2-3 rounds mỗi screen)
- **Generate variants** nếu cần explore alternatives
- **Output**: Approved visual direction cho mỗi P0 screen → reference khi code

## Capabilities

### New Capabilities
- `ui-mockups`: Stitch-generated screen mockups cho Phase 3A MVP — Dashboard, Reader, Modals, Login

### Modified Capabilities
- Không modify capabilities hiện tại — chỉ tạo visual reference

## Impact

- **Code**: Không thay đổi code — output là visual mockups
- **Files**: Stitch screens lưu trên Stitch cloud (project ID tracked)
- **Dependencies**: Stitch MCP đã cấu hình
- **Design references**: DESIGN_BRIEF.md + design-system/mentormind-v2/MASTER.md

## Không làm

- ❌ Code implementation (change #20-25)
- ❌ Phase 3B/3C screens (做 sau khi 3A approved)
- ❌ Mobile/tablet mockups (desktop first)
- ❌ Interactive prototypes (Stitch output là static)
