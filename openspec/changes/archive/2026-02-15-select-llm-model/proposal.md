## Why

Hệ thống cần chọn LLM model cụ thể để implement. Hiện tại config ghi "TBD". User đã có license **Google AI Ultra** ($249.99/tháng) với quota đầy đủ — tận dụng tài nguyên có sẵn, **$0 chi phí thêm**.

## What Changes

- Chốt LLM model theo **2-stage pipeline** (phân tích → planning)
- Xác định API endpoints và integration method
- Cập nhật `config.py` và `.env` với model configuration
- Design `services/analyzer.py` với 2-stage routing logic + fallback chain

## Quota hiện có (Google AI Ultra — $0 chi phí thêm)

| Model | Quota | Reset |
|-------|-------|-------|
| **Gemini 3 Pro** (High/Low) | 100% | ~5h |
| **Gemini 3 Flash** | 100% | ~5h |
| **Claude Opus 4.5/4.6** (Thinking) | 100% | ~5h |
| Claude Sonnet 4.5 | 100% | ~5h |
| GPT-OSS 120B | 100% | ~5h |

> Opus và Sonnet cùng quota → dùng Opus (model mạnh nhất).

## 2-Stage Pipeline Design

### Tại sao 2-stage thay vì 1-call?

Mỗi model có điểm mạnh khác nhau:
- **Gemini 3 Pro**: MMMU 81%, tiếng Việt hàng đầu, multimodal → **hiểu bài tốt nhất**
- **Claude Opus 4.6**: ARC-AGI 37.6%, SWE-Bench 80.9% → **reasoning + planning tốt nhất**

Tách 2 stage để mỗi model chơi đúng sở trường, tránh "vừa đánh trống vừa thổi còi".

### Stage 1: PHÂN TÍCH (Gemini 3 Pro — 1 call)

Gửi bài viết → Gemini trả 3 persona cùng lúc:

```
📥 Input: Bài viết "RAG Pipeline Best Practices 2026"

📤 Output (Gemini 3 Pro):

🔬 RESEARCHER:
- Tóm tắt: Bài viết trình bày best practices cho RAG pipeline...
- Key insights:
  • Chunking strategy ảnh hưởng 80% chất lượng
  • Hybrid search (keyword + semantic) outperform pure vector
- Concept: Giải thích "late chunking"...

🏗️ ARCHITECT:
- System design impact: CMS cần tách indexing thành async pipeline...
- Ứng dụng: eCommerce search có thể dùng hybrid search...
- Risk: Vector DB scaling khi >1M documents...

🔍 SKEPTIC:
- Hype: "80%" là số liệu từ 1 benchmark cụ thể, không phổ quát
- Giới hạn: RAG vẫn struggle với multi-hop reasoning
- Alternative: Fine-tuning on domain data có thể tốt hơn RAG
```

→ 3 góc nhìn, cùng 1 model → style nhất quán, không mâu thuẫn.

### Stage 2: TỔNG HỢP & KẾ HOẠCH (Claude Opus 4.6 — 1 call)

Gửi output Stage 1 → Opus tổng hợp + lên plan:

```
📥 Input: Output Stage 1 (Researcher + Architect + Skeptic)

📤 Output (Claude Opus 4.6):

📊 SYNTHESIZER:
1. Chunking strategy là bottleneck #1 — đầu tư thời gian ở đây
2. Hybrid search là safe bet cho production
3. RAG không phải silver bullet — evaluate vs fine-tuning
4. Async indexing pipeline nên là pattern mặc định
5. Cần benchmark trên data thật, không tin số liệu paper

🎯 ACTION PLAN:
- Tuần này: Build mini POC so sánh 3 chunking strategies
- Đọc thêm: "Late Chunking" paper
- Áp dụng: Thử hybrid search cho project hiện tại
```

→ Opus dùng reasoning mạnh để ra plan cụ thể, actionable hơn Gemini.

### So sánh 1-call vs 2-stage

| | 1-call (cũ) | 2-stage (mới) |
|---|------------|--------------|
| Gemini làm gì | Cả 4 persona | 3 persona (phân tích) |
| Opus làm gì | Không dùng | Synthesizer + Action Plan |
| Tổng calls | 1 | 2 |
| Latency | ~10s | ~20s |
| Action quality | OK | **Mạnh hơn nhiều** |
| Coherence | Cao | Cao (mỗi stage 1 model) |

### Model Config

```python
MODEL_CONFIG = {
    # Stage 1: Phân tích (Gemini 3 Pro)
    "stage_1_analysis": "gemini-3-pro",    # Researcher + Architect + Skeptic

    # Stage 2: Tổng hợp & Plan (Claude Opus 4.6)
    "stage_2_planning": "claude-opus-4.6",  # Synthesizer + Action Planning

    # Các task khác
    "batch_digest":     "gemini-3-pro",     # Tóm tắt backlog
    "weekly_synthesis": "gemini-3-pro",     # Cross-article analysis

    # Fallback chain (khi primary lỗi/rate limit)
    "fallback_chain": [
        "gemini-3-flash",    # 95% quality của Pro, 3x nhanh
        "claude-opus-4.5",   # Backup reasoning
        "gpt-oss-120b",      # Last resort
    ]
}
```

## Capabilities

### New Capabilities
- `llm-config`: Cấu hình 2-stage model pipeline, API keys, fallback chain, parameters

### Modified Capabilities
_Không có — chưa có spec nào existing_

## Impact

- `config.py`: 2-stage model config + fallback chain
- `.env` / `.env.example`: `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`
- `services/analyzer.py`: 2-stage pipeline logic + fallback
- `requirements.txt`: `google-generativeai`, `anthropic`

## Không làm

- ❌ Không dùng model khác nhau cho từng persona trong cùng 1 stage
- ❌ Không implement model switching UI/command
- ❌ Không benchmark models
- ❌ Không setup OpenRouter/external proxy
