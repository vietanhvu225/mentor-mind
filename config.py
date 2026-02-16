"""
Application configuration — loads from .env with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "learning.db")))

# ── Language ────────────────────────────────────────────────────────
LANGUAGE = os.getenv("LANGUAGE", "vi")  # "vi" | "en"

# ── Telegram ───────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ── Raindrop ───────────────────────────────────────────────────────
RAINDROP_API_TOKEN = os.getenv("RAINDROP_API_TOKEN", "")

# ── Antigravity Tools Proxy (LLM Gateway) ──────────────────────────
ANTIGRAVITY_API_KEY = os.getenv("ANTIGRAVITY_API_KEY", "sk-antigravity")
ANTIGRAVITY_BASE_URL = os.getenv("ANTIGRAVITY_BASE_URL", "http://127.0.0.1:8045/v1")

# ── Model Configuration ───────────────────────────────────────────
# 2-stage pipeline: Stage 1 (analysis) + Stage 2 (planning)
MODEL_CONFIG = {
    "stage_1_analysis": os.getenv("MODEL_STAGE_1", "gemini-3-pro"),
    "stage_2_planning": os.getenv("MODEL_STAGE_2", "claude-opus-4-6-thinking"),
    "batch_digest":     os.getenv("MODEL_DIGEST", "gemini-3-pro"),
    "weekly_synthesis": os.getenv("MODEL_WEEKLY", "gemini-3-pro"),
}

# Fallback chain — tried in order when primary model fails
# Proxy handles account-level retry/rotation; this is model-level fallback
_fallback_env = os.getenv("FALLBACK_CHAIN", "gemini-3-flash,claude-sonnet-4-5")
FALLBACK_CHAIN = [m.strip() for m in _fallback_env.split(",") if m.strip()]

# ── Timezone ───────────────────────────────────────────────────────
TIMEZONE = os.getenv("TZ", "Asia/Ho_Chi_Minh")

# ── Camofox Browser (optional) ─────────────────────────────────────
# Anti-detection browser server for Facebook/LinkedIn/Instagram extraction
CAMOFOX_URL = os.getenv("CAMOFOX_URL", "http://localhost:9377")
CAMOFOX_USER_ID = os.getenv("CAMOFOX_USER_ID", "learning-bot")

# ── Scheduler ──────────────────────────────────────────────────────
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8"))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))
SCHEDULE_ENABLED = os.getenv("SCHEDULE_ENABLED", "true").lower() == "true"
