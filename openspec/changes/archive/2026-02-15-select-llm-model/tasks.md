## 1. Config & Environment Setup

- [x] 1.1 Thêm `openai` vào `requirements.txt`
- [x] 1.2 Thêm env variables vào `.env.example`: `ANTIGRAVITY_API_KEY`, `ANTIGRAVITY_BASE_URL`, `MODEL_STAGE_1`, `MODEL_STAGE_2`, `MODEL_DIGEST`, `MODEL_WEEKLY`, `FALLBACK_CHAIN`
- [x] 1.3 Cập nhật `config.py` với `MODEL_CONFIG` dict (4 task types) và `FALLBACK_CHAIN` list
- [x] 1.4 Cập nhật `config.py` với `ANTIGRAVITY_BASE_URL` và `ANTIGRAVITY_API_KEY`

> **Done khi:** `config.py` load được tất cả model config từ env, có default values hợp lý.

## 2. LLM Client Service

- [x] 2.1 Tạo `services/llm_client.py` với OpenAI client kết nối Antigravity proxy (`base_url`, `api_key` từ config)
- [x] 2.2 Implement hàm `call_llm(model, messages, **kwargs)` — wrapper gọi `client.chat.completions.create()`
- [x] 2.3 Implement model-level fallback logic trong `call_llm_with_fallback(task_type, messages)` — thử primary model → fallback chain
- [x] 2.4 Implement proxy health check: `check_proxy_health()` gọi `GET /health` endpoint
- [x] 2.5 Implement retry logic cho ConnectionError (retry 2x, backoff 5s)

> **Done khi:** `call_llm("gemini-3-pro", [...])` gọi được qua proxy và trả response. Fallback chain hoạt động khi model fail.

## 3. Prompt Files

- [x] 3.1 Tạo `prompts/daily_analysis.md` — Stage 1 system prompt (include 3 personas)
- [x] 3.2 Tạo `prompts/action_planning.md` — Stage 2 system prompt (synthesizer + action plan)
- [x] 3.3 Tạo `prompts/personas/researcher.md`
- [x] 3.4 Tạo `prompts/personas/architect.md`
- [x] 3.5 Tạo `prompts/personas/skeptic.md`
- [x] 3.6 Tạo `prompts/personas/synthesizer.md`
- [x] 3.7 Implement `load_prompt(filename)` trong `services/llm_client.py` — đọc .md file, raise FileNotFoundError nếu missing

> **Done khi:** Tất cả 6 prompt files tồn tại, `load_prompt()` đọc và return nội dung đúng.

## 4. 2-Stage Pipeline trong Analyzer

- [x] 4.1 Implement `analyze_article(article_text)` trong `services/analyzer.py` — orchestrate 2-stage pipeline
- [x] 4.2 Stage 1: Gọi `call_llm_with_fallback("stage_1_analysis", ...)` với daily_analysis prompt + article text
- [x] 4.3 Stage 2: Gọi `call_llm_with_fallback("stage_2_planning", ...)` với action_planning prompt + Stage 1 output
- [x] 4.4 Implement graceful degradation: nếu Stage 2 fail → return Stage 1 output + warning flag
- [x] 4.5 Implement full failure: nếu Stage 1 fail → return error object với article link

> **Done khi:** `analyze_article("...")` trả kết quả 2-stage hoặc graceful degradation. Không crash khi proxy down.

## 5. Testing & Verification

- [x] 5.1 Test kết nối proxy: chạy `call_llm("gemini-3-flash", [{"role":"user","content":"hello"}])` thành công
- [x] 5.2 Test 2-stage pipeline với 1 article thật → chạy `python test_llm.py`
- [x] 5.3 Test fallback: set `MODEL_STAGE_1=nonexistent-model` → verify fallback chain kicks in
- [x] 5.4 Test graceful degradation: disconnect Stage 2 model → verify Stage 1 output vẫn được trả
- [x] 5.5 Test config override: set env `MODEL_STAGE_1=gemini-3-flash` → verify đúng model được sử dụng

> **Requires:** Python + pip in PATH, `pip install -r requirements.txt`, Antigravity Tools proxy running at localhost:8045
