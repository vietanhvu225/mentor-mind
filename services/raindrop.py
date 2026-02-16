"""
Raindrop.io API client — fetch bookmarks and sync to article queue.

Uses test token auth (no OAuth). Scans ALL collections via collectionId=0.
"""

import logging
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from config import RAINDROP_API_TOKEN, DATABASE_PATH
from db.repository import add_article, get_article_by_raindrop_id

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────
BASE_URL = "https://api.raindrop.io/rest/v1"
PER_PAGE = 50          # Raindrop API max per page
MAX_RETRIES = 3
BACKOFF_BASE = 2       # seconds: 2, 4, 8


@dataclass
class SyncResult:
    """Result of a queue sync operation."""
    total_fetched: int = 0
    new_inserted: int = 0
    skipped: int = 0


def _headers() -> dict:
    """Auth headers for Raindrop API."""
    return {
        "Authorization": f"Bearer {RAINDROP_API_TOKEN}",
        "Content-Type": "application/json",
    }


def fetch_raindrops(page: int = 0, perpage: int = PER_PAGE) -> list[dict]:
    """
    Fetch raindrops from ALL collections (collectionId=0).

    Args:
        page: Page number (0-indexed).
        perpage: Items per page (max 50).

    Returns:
        List of raindrop dicts from API response.
    """
    url = f"{BASE_URL}/raindrops/0"
    params = {
        "sort": "-created",   # newest first
        "perpage": perpage,
        "page": page,
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.get(url, headers=_headers(), params=params)

            if response.status_code == 401:
                logger.error("Raindrop API: Token không hợp lệ (401)")
                return []

            if response.status_code == 429:
                logger.warning("Raindrop API: Rate limited (429), retrying...")
                time.sleep(BACKOFF_BASE ** (attempt + 1))
                continue

            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            logger.info(f"Fetched page {page}: {len(items)} raindrops")
            return items

        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as e:
            last_error = e
            wait = BACKOFF_BASE ** (attempt + 1)
            logger.warning(f"Raindrop API: {type(e).__name__}, retry {attempt+1}/{MAX_RETRIES} in {wait}s")
            time.sleep(wait)
        except httpx.HTTPStatusError as e:
            logger.error(f"Raindrop API HTTP error: {e.response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Raindrop API unexpected error: {e}")
            return []

    logger.error(f"Raindrop API: All {MAX_RETRIES} retries failed — {last_error}")
    return []


def fetch_all_new_raindrops(db_path: Optional[str] = None) -> list[dict]:
    """
    Fetch all NEW raindrops (not yet in DB) with pagination.

    Uses stop-at-existing strategy: when a raindrop_id is found in DB,
    stop fetching further pages (older items are already synced).

    Args:
        db_path: Path to SQLite DB. Defaults to config DATABASE_PATH.

    Returns:
        List of new raindrop dicts not yet in DB.
    """
    if db_path is None:
        db_path = str(DATABASE_PATH)

    new_raindrops = []
    page = 0

    while True:
        items = fetch_raindrops(page=page)
        if not items:
            break  # no more items or API error

        found_existing = False
        for item in items:
            raindrop_id = str(item.get("_id", ""))
            if not raindrop_id:
                continue

            existing = get_article_by_raindrop_id(db_path, raindrop_id)
            if existing:
                found_existing = True
                break  # stop — older items already synced
            else:
                new_raindrops.append(item)

        if found_existing:
            break  # don't fetch more pages

        # If we got fewer than PER_PAGE, we've reached the end
        if len(items) < PER_PAGE:
            break

        page += 1

    logger.info(f"Found {len(new_raindrops)} new raindrops across {page+1} pages")
    return new_raindrops


def sync_raindrops_to_db(
    raindrops: list[dict],
    db_path: Optional[str] = None,
) -> SyncResult:
    """
    Insert new raindrops into the articles table (dedup by raindrop_id).

    Args:
        raindrops: List of raindrop dicts from API.
        db_path: Path to SQLite DB. Defaults to config DATABASE_PATH.

    Returns:
        SyncResult with counts.
    """
    if db_path is None:
        db_path = str(DATABASE_PATH)

    result = SyncResult(total_fetched=len(raindrops))

    for item in raindrops:
        raindrop_id = str(item.get("_id", ""))
        title = item.get("title", "Untitled")
        link = item.get("link", "")
        excerpt = item.get("excerpt", "")
        created = item.get("created", "")

        # Extract collection name if available
        collection = item.get("collection", {})
        collection_name = None
        if isinstance(collection, dict):
            collection_name = collection.get("title")

        # Skip if missing essential data
        if not raindrop_id or not link:
            logger.warning(f"Skipping raindrop — missing id or link: {title}")
            result.skipped += 1
            continue

        # Dedup check
        existing = get_article_by_raindrop_id(db_path, raindrop_id)
        if existing:
            result.skipped += 1
            continue

        try:
            add_article(
                db_path=db_path,
                raindrop_id=raindrop_id,
                title=title,
                source_url=link,
                date=created,
                raw_content=excerpt if excerpt else None,
                collection_name=collection_name,
            )
            result.new_inserted += 1
            logger.debug(f"Inserted: {title}")
        except Exception as e:
            logger.error(f"Failed to insert raindrop {raindrop_id}: {e}")
            result.skipped += 1

    logger.info(
        f"Sync complete: {result.new_inserted} new, "
        f"{result.skipped} skipped, {result.total_fetched} total"
    )
    return result


def pick_next_article(db_path: Optional[str] = None) -> Optional[dict]:
    """
    Pick the next article from the queue.

    Order: priority DESC, date DESC (newest article first, high priority first).

    Args:
        db_path: Path to SQLite DB. Defaults to config DATABASE_PATH.

    Returns:
        Article dict or None if queue is empty.
    """
    if db_path is None:
        db_path = str(DATABASE_PATH)

    from db.repository import get_articles_by_status
    articles = get_articles_by_status(db_path, "queued")

    if not articles:
        return None

    # Sort: priority DESC, then date DESC (newest Raindrop article first)
    articles.sort(key=lambda a: (a.get("priority") or 0, a.get("date") or ""), reverse=True)
    return articles[0]
