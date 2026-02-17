## Context

Bot hiện hardcode ~60+ Vietnamese strings trong `telegram_handler.py` và ~20+ trong services. Prompts cho LLM cũng viết tiếng Việt. Cần i18n system đơn giản, không over-engineer.

## Approach: Simple String Map + Prompt Locale

### 1. Config — `LANGUAGE` env var

```python
# config.py
LANGUAGE = os.getenv("LANGUAGE", "vi")  # "vi" | "en"
```

### 2. String Map — `strings.py` (NEW)

```python
STRINGS = {
    "vi": {
        "help_header": "📋 *Commands*\n\n📖 *Học tập*\n",
        "analyze_start": "🔍 Đang phân tích bài #{id}...",
        "analyze_done": "✅ Phân tích xong bài #{id}",
        # ... ~60 keys
    },
    "en": {
        "help_header": "📋 *Commands*\n\n📖 *Learning*\n",
        "analyze_start": "🔍 Analyzing article #{id}...",
        "analyze_done": "✅ Analysis complete for article #{id}",
        # ... ~60 keys
    }
}

def t(key, **kwargs):
    """Translate string key to current locale."""
    from config import LANGUAGE
    template = STRINGS.get(LANGUAGE, STRINGS["vi"]).get(key, key)
    return template.format(**kwargs) if kwargs else template
```

### 3. Prompt Locale — Folder structure

```
prompts/
├── vi/
│   ├── personas/
│   │   ├── researcher.md
│   │   ├── architect.md
│   │   ├── skeptic.md
│   │   └── synthesizer.md
│   ├── digest.md
│   ├── weekly.md
│   ├── daily_analysis.md
│   └── action_planning.md
└── en/
    ├── personas/
    │   ├── researcher.md
    │   ├── architect.md
    │   ├── skeptic.md
    │   └── synthesizer.md
    ├── digest.md
    ├── weekly.md
    ├── daily_analysis.md
    └── action_planning.md
```

### 4. Sửa `load_prompt()` trong `llm_client.py`

```python
def load_prompt(name):
    path = PROMPTS_DIR / config.LANGUAGE / f"{name}.md"
    if not path.exists():
        # Fallback to Vietnamese if English prompt not available
        path = PROMPTS_DIR / "vi" / f"{name}.md"
    return path.read_text(encoding="utf-8")
```

## Migration Strategy

1. Move existing prompts vào `prompts/vi/`
2. Copy + translate sang `prompts/en/`
3. Extract strings từ `telegram_handler.py` → `strings.py` keys
4. Extract strings từ services → `strings.py` keys
5. Replace hardcoded strings với `t()` calls

## Trade-offs

| Decision | Pro | Con |
|---|---|---|
| Simple dict thay vì gettext | Zero dependencies, dễ hiểu | Không có tooling (po editor) |
| Fallback to Vietnamese | Không crash nếu thiếu key EN | User có thể thấy mixed language |
| Config-time only | Đơn giản, không cần restart logic | Đổi language phải restart bot |
