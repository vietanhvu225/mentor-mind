## 1. Config
- [x] 1.1 Thêm `LANGUAGE` env var vào `config.py`
- [x] 1.2 Thêm `LANGUAGE=vi` vào `.env.example`

## 2. String Map
- [x] 2.1 Tạo `strings.py` với function `t(key, **kwargs)`
- [x] 2.2 Extract strings từ `telegram_handler.py` → string map (vi + en) — ALL commands done
- [x] 2.3 Extract strings từ services (scheduler) → string map — done

## 3. Prompt Locale
- [x] 3.1 Move existing prompts → `prompts/vi/`
- [x] 3.2 Translate prompts → `prompts/en/`
- [x] 3.3 Sửa `load_prompt()` trong `llm_client.py` thêm locale folder + fallback

## 4. Integration
- [x] 4.1 Replace hardcoded strings trong `telegram_handler.py` → `t()` calls (ALL)
- [x] 4.2 Replace hardcoded strings trong `scheduler.py` → `t()` calls (ALL)

## 5. Testing
- [x] 5.1 Compile check all modified files — OK
- [x] 5.2 Test `LANGUAGE=vi` — verified output correct
- [x] 5.3 Test `LANGUAGE=en` — verified output correct
