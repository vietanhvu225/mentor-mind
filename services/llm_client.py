"""
LLM Client Service — Single OpenAI client for all models via Antigravity Tools proxy.

Usage:
    from services.llm_client import call_llm, call_llm_with_fallback, check_proxy_health

    # Direct call
    response = call_llm("gemini-3-pro", [{"role": "user", "content": "Hello"}])

    # With fallback
    response = call_llm_with_fallback("stage_1_analysis", messages)
"""
import os
import time
import logging
from pathlib import Path
from typing import Optional

import openai
import httpx

import config

logger = logging.getLogger(__name__)


# ── OpenAI Client (singleton) ──────────────────────────────────────
_client: Optional[openai.OpenAI] = None


def _get_client() -> openai.OpenAI:
    """Lazy-init OpenAI client pointing to Antigravity Tools proxy."""
    global _client
    if _client is None:
        _client = openai.OpenAI(
            api_key=config.ANTIGRAVITY_API_KEY,
            base_url=config.ANTIGRAVITY_BASE_URL,
            timeout=120.0,  # 2 min timeout to prevent hanging
        )
        logger.info(
            "LLM client initialized → %s", config.ANTIGRAVITY_BASE_URL
        )
    return _client


# ── Core LLM Call ──────────────────────────────────────────────────
def call_llm(
    model: str,
    messages: list[dict],
    max_retries: int = 2,
    retry_delay: float = 5.0,
    **kwargs,
) -> str:
    """
    Call an LLM model via the Antigravity proxy.

    Handles ConnectionError with retry logic (retry 2x, backoff 5s).
    Proxy handles account-level retry/rotation internally.

    Returns:
        The assistant's response text.

    Raises:
        openai.APIError: If the API returns an error after retries.
        ConnectionError: If proxy is unreachable after retries.
    """
    client = _get_client()
    last_error: Optional[Exception] = None

    for attempt in range(1 + max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs,
            )
            content = response.choices[0].message.content or ""
            logger.info(
                "LLM call OK: model=%s, tokens=%s",
                model,
                getattr(response.usage, "total_tokens", "?"),
            )
            return content

        except (ConnectionError, httpx.ConnectError) as e:
            last_error = e
            if attempt < max_retries:
                wait = retry_delay * (attempt + 1)
                logger.warning(
                    "Proxy connection error (attempt %d/%d), retrying in %.1fs: %s",
                    attempt + 1, max_retries + 1, wait, e,
                )
                time.sleep(wait)
            else:
                logger.error(
                    "Proxy unreachable after %d attempts: %s",
                    max_retries + 1, e,
                )

        except httpx.ReadTimeout as e:
            # Timeout — don't retry same model, fail fast to fallback
            logger.warning(
                "LLM timeout after 120s: model=%s. Skipping retries → fallback.",
                model,
            )
            raise

        except openai.APIError as e:
            # API-level errors (rate limit, server error, etc.)
            # Proxy already handles account rotation for 429s,
            # so if we still get an error, the model is truly failing.
            logger.error("LLM API error: model=%s, error=%s", model, e)
            raise

    raise ConnectionError(
        f"Proxy unreachable after {max_retries + 1} attempts"
    ) from last_error


# ── Fallback-aware Call ────────────────────────────────────────────
def call_llm_with_fallback(
    task_type: str,
    messages: list[dict],
    **kwargs,
) -> str:
    """
    Call LLM with model-level fallback chain.

    1. Try the primary model mapped to task_type in MODEL_CONFIG
    2. On failure, try each model in FALLBACK_CHAIN
    3. If all fail, raise the last error

    Args:
        task_type: Key in MODEL_CONFIG (e.g. "stage_1_analysis")
        messages: Chat messages list
        **kwargs: Extra args passed to chat.completions.create()

    Returns:
        The assistant's response text.

    Raises:
        Exception: If primary + all fallback models fail.
    """
    primary_model = config.MODEL_CONFIG.get(task_type)
    if not primary_model:
        raise ValueError(f"Unknown task_type: {task_type!r}. "
                         f"Valid: {list(config.MODEL_CONFIG.keys())}")

    models_to_try = [primary_model] + config.FALLBACK_CHAIN
    last_error: Optional[Exception] = None

    for model in models_to_try:
        try:
            logger.info("Trying model=%s for task=%s", model, task_type)
            return call_llm(model, messages, **kwargs)
        except Exception as e:
            last_error = e
            logger.warning(
                "Model %s failed for task %s: %s. Trying next fallback...",
                model, task_type, e,
            )

    raise RuntimeError(
        f"All models failed for task {task_type!r}. "
        f"Tried: {models_to_try}"
    ) from last_error


# ── Proxy Health Check ─────────────────────────────────────────────
def check_proxy_health() -> bool:
    """
    Check if Antigravity Tools proxy is reachable.

    Calls GET /health (or /healthz) endpoint.

    Returns:
        True if proxy is healthy, False otherwise.
    """
    # Derive health URL from base_url (strip /v1 suffix)
    base = config.ANTIGRAVITY_BASE_URL.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]

    for endpoint in ("/health", "/healthz"):
        try:
            resp = httpx.get(f"{base}{endpoint}", timeout=5.0)
            if resp.status_code == 200:
                logger.info("Proxy health check OK: %s%s", base, endpoint)
                return True
        except Exception:
            pass

    logger.warning("Proxy health check failed: %s", base)
    return False


# ── Prompt Loader ──────────────────────────────────────────────────
def load_prompt(filename: str) -> str:
    """
    Load a prompt template from the prompts/{LANGUAGE}/ directory.

    Tries prompts/{LANGUAGE}/{filename} first, falls back to prompts/vi/{filename}.

    Args:
        filename: Relative path within prompts/{lang}/ (e.g. "daily_analysis.md"
                  or "personas/researcher.md")

    Returns:
        The prompt text content.

    Raises:
        FileNotFoundError: If the prompt file doesn't exist in any locale.
    """
    # Try current language first
    path = config.PROMPTS_DIR / config.LANGUAGE / filename
    if path.exists():
        return path.read_text(encoding="utf-8")

    # Fallback to Vietnamese
    fallback_path = config.PROMPTS_DIR / "vi" / filename
    if fallback_path.exists():
        logger.warning(
            "Prompt %s not found for locale '%s', falling back to 'vi'",
            filename, config.LANGUAGE,
        )
        return fallback_path.read_text(encoding="utf-8")

    raise FileNotFoundError(
        f"Prompt file not found: {path}. "
        f"Also tried fallback: {fallback_path}"
    )
