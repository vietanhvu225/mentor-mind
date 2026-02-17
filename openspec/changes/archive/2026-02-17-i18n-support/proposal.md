## Why

Bot hiện chỉ output tiếng Việt (cả UI lẫn AI analysis). Muốn share cho người dùng quốc tế hoặc đơn giản chuyển sang tiếng Anh cần sửa hardcode nhiều chỗ. Cần hệ thống i18n để switch ngôn ngữ qua 1 env var.

## What Changes

- Thêm `LANGUAGE` env var (`vi` | `en`, default: `vi`)
- Tạo `strings.py` chứa string map cho UI messages (2 locales)
- Tổ chức lại prompts: `prompts/vi/` + `prompts/en/`
- Sửa `load_prompt()` chọn prompt theo locale
- Extract hardcoded Vietnamese strings từ `telegram_handler.py` và services ra string map

## Capabilities

### New Capabilities
- `i18n`: Hệ thống chuyển đổi ngôn ngữ (EN/VI) cho cả UI strings và AI prompts

### Modified Capabilities
- `telegram-bot`: Commands output theo ngôn ngữ đã chọn thay vì hardcode tiếng Việt

## Impact

- `config.py`: thêm `LANGUAGE`
- `services/llm_client.py`: sửa `load_prompt()` path
- `bot/telegram_handler.py`: thay hardcoded strings → `t()` calls
- `services/*.py`: thay Vietnamese strings → `t()` calls
- `prompts/`: restructure thành `vi/` + `en/` subfolders
- `.env.example`: thêm `LANGUAGE`

## Không làm

- Không hỗ trợ runtime language switching (chỉ config-time)
- Không dùng gettext/babel (overkill cho bot cá nhân)
- Không tự động detect ngôn ngữ bài viết
