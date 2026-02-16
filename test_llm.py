"""Integration tests for LLM pipeline — tests all configured models."""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

def log(msg):
    with open("test_results.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)

# Clear previous results
with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write("=== LLM Integration Test Results ===\n\n")

# ── Test 1: Proxy Health Check ─────────────────────────────────────
log("TEST 1: Proxy health check...")
try:
    from services.llm_client import call_llm, call_llm_with_fallback, check_proxy_health
    health = check_proxy_health()
    log(f"  Health: {'OK' if health else 'FAIL'}")
    log(f"  RESULT: {'PASS ✓' if health else 'FAIL ✗'}\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 2: Individual Model Connectivity ──────────────────────────
MODELS_TO_TEST = [
    ("gemini-3-pro",            "Stage 1 primary"),
    ("claude-opus-4-6-thinking","Stage 2 primary"),
    ("gemini-3-flash",          "Fallback #1"),
    ("claude-sonnet-4-5",       "Fallback #2"),
]

log("TEST 2: Individual model connectivity...")
for model, role in MODELS_TO_TEST:
    try:
        start = time.time()
        r = call_llm(model, [{"role": "user", "content": "Reply with just: OK"}])
        elapsed = time.time() - start
        ok = "OK" in r.strip().upper()
        log(f"  {model} ({role}): {r.strip()[:50]} [{elapsed:.1f}s] {'✓' if ok else '⚠️'}")
    except Exception as e:
        log(f"  {model} ({role}): FAIL ✗ — {e}")
log("")

# ── Test 3: Config Override ────────────────────────────────────────
log("TEST 3: Config override...")
try:
    import config
    original = config.MODEL_CONFIG["stage_1_analysis"]
    log(f"  Default stage_1: {original}")
    config.MODEL_CONFIG["stage_1_analysis"] = "gemini-3-flash"
    log(f"  After override: {config.MODEL_CONFIG['stage_1_analysis']}")
    config.MODEL_CONFIG["stage_1_analysis"] = original  # restore
    log("  RESULT: PASS ✓\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 4: 2-Stage Pipeline (REAL models) ─────────────────────────
log("TEST 4: 2-stage pipeline with REAL models...")
log(f"  Stage 1 model: {config.MODEL_CONFIG['stage_1_analysis']}")
log(f"  Stage 2 model: {config.MODEL_CONFIG['stage_2_planning']}")
try:
    from services.analyzer import analyze_article
    start = time.time()
    result = analyze_article(
        "RAG (Retrieval-Augmented Generation) combines LLMs with external knowledge bases. "
        "Key insight: chunking strategy affects 80% of retrieval quality. "
        "Hybrid search (keyword + semantic) consistently outperforms pure vector search. "
        "Late chunking is a new technique that preserves context across chunk boundaries.",
        article_link="https://example.com/rag-best-practices"
    )
    elapsed = time.time() - start
    log(f"  Stage 1 success: {result.stage_1_success}")
    log(f"  Stage 2 success: {result.stage_2_success}")
    log(f"  Total time: {elapsed:.1f}s")
    log(f"  Stage 1 output: {len(result.stage_1_output or '')} chars")
    log(f"  Stage 2 output: {len(result.stage_2_output or '')} chars")
    if result.stage_1_output:
        log(f"  Stage 1 preview: {result.stage_1_output[:200]}...")
    if result.stage_2_output:
        log(f"  Stage 2 preview: {result.stage_2_output[:200]}...")
    log(f"  RESULT: {'PASS ✓' if result.full_success else 'PARTIAL' if result.success else 'FAIL ✗'}\n")
except Exception as e:
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 5: Fallback Chain ─────────────────────────────────────────
log("TEST 5: Fallback chain (bad primary → fallback model)...")
try:
    import config
    config.MODEL_CONFIG["stage_1_analysis"] = "nonexistent-model-xyz"
    start = time.time()
    r = call_llm_with_fallback("stage_1_analysis", [{"role": "user", "content": "Reply OK"}])
    elapsed = time.time() - start
    log(f"  Response: {r.strip()[:50]} [{elapsed:.1f}s]")
    log(f"  Fallback chain used: {config.FALLBACK_CHAIN}")
    config.MODEL_CONFIG["stage_1_analysis"] = "gemini-3-pro"  # restore
    log("  RESULT: PASS ✓\n")
except Exception as e:
    config.MODEL_CONFIG["stage_1_analysis"] = "gemini-3-pro"  # restore
    log(f"  RESULT: FAIL ✗ — {e}\n")

# ── Test 6: Graceful Degradation ───────────────────────────────────
log("TEST 6: Graceful degradation (Stage 2 fail)...")
try:
    config.MODEL_CONFIG["stage_2_planning"] = "nonexistent-model-xyz"
    old_chain = config.FALLBACK_CHAIN[:]
    config.FALLBACK_CHAIN.clear()  # no fallbacks

    result = analyze_article("Test article for degradation.", article_link="https://example.com")
    log(f"  Stage 1 success: {result.stage_1_success}")
    log(f"  Stage 2 success: {result.stage_2_success}")
    log(f"  Warning: {result.warning}")
    has_warning = result.stage_1_success and not result.stage_2_success and result.warning
    config.MODEL_CONFIG["stage_2_planning"] = "claude-opus-4-6-thinking"  # restore
    config.FALLBACK_CHAIN.extend(old_chain)  # restore
    log(f"  RESULT: {'PASS ✓' if has_warning else 'FAIL ✗'}\n")
except Exception as e:
    config.MODEL_CONFIG["stage_2_planning"] = "claude-opus-4-6-thinking"
    log(f"  RESULT: FAIL ✗ — {e}\n")

log("=== All tests done ===")
