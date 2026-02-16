"""
MentorMind — Personal AI Learning Assistant.

Initializes database, scheduler, and starts Telegram bot polling.
"""
import logging
import sys
from pathlib import Path

import config
from db.models import init_db
from bot.telegram_handler import build_application

# ── Logging ────────────────────────────────────────────────────────
log_file = Path(__file__).parent / "data" / "bot.log"
log_file.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(log_file), mode="w", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Initialize DB and start the Telegram bot."""

    # Validate token
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Add it to .env file.")
        sys.exit(1)

    if not config.TELEGRAM_CHAT_ID:
        logger.warning("TELEGRAM_CHAT_ID is not set. Bot won't send proactive messages.")

    # Initialize database
    db_path = str(config.DATABASE_PATH)
    logger.info(f"Initializing database at {db_path}")
    init_db(db_path)

    # Build and run bot (scheduler starts via post_init inside build_application)
    logger.info("Starting Telegram bot...")
    app = build_application(config.TELEGRAM_BOT_TOKEN)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

