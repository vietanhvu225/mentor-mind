"""
Camofox Browser REST client.

Provides Python interface to the Camofox browser server for enhanced
content extraction from walled-garden sites (Facebook, LinkedIn, Instagram).

Camofox is a headless Firefox fork with C++ anti-detection that bypasses
bot detection on major platforms. It runs as a separate Node.js server
on localhost:9377.

Usage:
    client = CamofoxClient()
    if client.is_available():
        result = client.extract_page("https://facebook.com/some-post")
        # result = {text, screenshot_b64, links, title}
"""
import base64
import logging
import os
import time
from pathlib import Path
from typing import Optional

import httpx

from config import CAMOFOX_URL, CAMOFOX_USER_ID

# API key for cookie import (optional)
CAMOFOX_API_KEY = os.getenv("CAMOFOX_API_KEY", "")

# Default cookies directory
CAMOFOX_COOKIES_DIR = Path(os.getenv(
    "CAMOFOX_COOKIES_DIR",
    os.path.expanduser("~/.camofox/cookies")
))

logger = logging.getLogger(__name__)

# Timeouts
HEALTH_TIMEOUT = 3       # Quick check if server is up
PAGE_LOAD_TIMEOUT = 30   # Wait for page to render
API_TIMEOUT = 15         # General API calls


class CamofoxClient:
    """REST client for Camofox browser server."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        self.base_url = (base_url or CAMOFOX_URL).rstrip("/")
        self.user_id = user_id or CAMOFOX_USER_ID
        self._available: Optional[bool] = None  # cached health check
        self._cookies_imported: bool = False     # track cookie import

    # ── Health ────────────────────────────────────────────────────

    def is_available(self) -> bool:
        """
        Check if Camofox server is running.
        Result is cached for the lifetime of this client instance.
        """
        if self._available is not None:
            return self._available

        try:
            resp = httpx.get(
                f"{self.base_url}/health",
                timeout=HEALTH_TIMEOUT,
            )
            self._available = resp.status_code == 200
        except Exception:
            self._available = False

        if self._available:
            logger.info("Camofox server available")
        else:
            logger.debug("Camofox server not available — using fallback extraction")

        return self._available

    # ── Cookie Import ─────────────────────────────────────────────

    def import_cookies(self, cookie_filename: str = "facebook.txt") -> bool:
        """
        Import cookies from Netscape-format file into Camofox session.
        Called once per client instance before first extraction.

        Args:
            cookie_filename: Name of cookie file in ~/.camofox/cookies/

        Returns:
            True if cookies were successfully imported.
        """
        if self._cookies_imported:
            return True

        if not CAMOFOX_API_KEY:
            logger.debug("CAMOFOX_API_KEY not set — skipping cookie import")
            return False

        cookie_file = CAMOFOX_COOKIES_DIR / cookie_filename
        if not cookie_file.exists():
            logger.debug(f"Cookie file not found: {cookie_file}")
            return False

        # Parse Netscape cookie file
        cookies = []
        try:
            with open(cookie_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or not line:
                        continue
                    parts = line.split("\t")
                    if len(parts) >= 7:
                        cookies.append({
                            "domain": parts[0],
                            "path": parts[2],
                            "secure": parts[3].upper() == "TRUE",
                            "expires": int(float(parts[4])) if parts[4] != "0" else -1,
                            "name": parts[5],
                            "value": parts[6],
                        })
        except Exception as e:
            logger.warning(f"Failed to parse cookie file: {e}")
            return False

        if not cookies:
            logger.debug("No cookies parsed from file")
            return False

        # POST cookies to Camofox server
        try:
            resp = httpx.post(
                f"{self.base_url}/sessions/{self.user_id}/cookies",
                json={"cookies": cookies},
                headers={
                    "Authorization": f"Bearer {CAMOFOX_API_KEY}",
                    "Content-Type": "application/json",
                },
                timeout=API_TIMEOUT,
            )
            if resp.status_code == 200:
                self._cookies_imported = True
                logger.info(f"Imported {len(cookies)} cookies into Camofox session")
                return True
            else:
                logger.warning(f"Cookie import failed: {resp.status_code} — {resp.text[:200]}")
                return False
        except Exception as e:
            logger.warning(f"Cookie import request failed: {e}")
            return False

    # ── Tab Management ────────────────────────────────────────────

    def create_tab(self, url: str, session_key: str = "extract") -> Optional[str]:
        """
        Open a new tab and navigate to URL.

        Returns:
            Tab ID string, or None on failure.
        """
        try:
            resp = httpx.post(
                f"{self.base_url}/tabs",
                json={
                    "userId": self.user_id,
                    "sessionKey": session_key,
                    "url": url,
                },
                timeout=PAGE_LOAD_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            tab_id = data.get("id") or data.get("tabId")
            logger.info(f"Camofox tab created: {tab_id} → {url}")
            return tab_id
        except Exception as e:
            logger.warning(f"Camofox create_tab failed: {e}")
            return None

    def close_tab(self, tab_id: str) -> None:
        """Close a tab by ID."""
        try:
            httpx.delete(
                f"{self.base_url}/tabs/{tab_id}",
                params={"userId": self.user_id},
                timeout=API_TIMEOUT,
            )
        except Exception as e:
            logger.debug(f"Camofox close_tab: {e}")

    # ── Content Extraction ────────────────────────────────────────

    def get_snapshot(self, tab_id: str) -> Optional[str]:
        """
        Get accessibility snapshot — token-efficient text representation.
        ~90% smaller than raw HTML.
        """
        try:
            resp = httpx.get(
                f"{self.base_url}/tabs/{tab_id}/snapshot",
                params={"userId": self.user_id},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("snapshot", "")
        except Exception as e:
            logger.warning(f"Camofox snapshot failed: {e}")
            return None

    def get_screenshot(self, tab_id: str) -> Optional[bytes]:
        """Get page screenshot as PNG bytes."""
        try:
            resp = httpx.get(
                f"{self.base_url}/tabs/{tab_id}/screenshot",
                params={"userId": self.user_id},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            if "image" in content_type:
                return resp.content
            # Some servers return base64 JSON
            data = resp.json()
            if data.get("screenshot"):
                return base64.b64decode(data["screenshot"])
            return resp.content
        except Exception as e:
            logger.warning(f"Camofox screenshot failed: {e}")
            return None

    def get_links(self, tab_id: str) -> list[str]:
        """Get all links on the rendered page."""
        try:
            resp = httpx.get(
                f"{self.base_url}/tabs/{tab_id}/links",
                params={"userId": self.user_id},
                timeout=API_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("links", [])
        except Exception as e:
            logger.warning(f"Camofox get_links failed: {e}")
            return []

    # ── High-Level Extraction ─────────────────────────────────────

    def extract_page(self, url: str, wait_seconds: float = 3.0) -> Optional[dict]:
        """
        Full extraction pipeline for a single URL.

        Steps: create tab → wait for render → snapshot + screenshot + links → close.

        Args:
            url: Page URL to extract.
            wait_seconds: Extra wait after page load for JS rendering.

        Returns:
            Dict with keys: text, screenshot_b64, links, title.
            None if extraction fails.
        """
        if not self.is_available():
            return None

        # Auto-import cookies on first extraction
        self.import_cookies()

        tab_id = self.create_tab(url)
        if not tab_id:
            return None

        try:
            # Wait for dynamic content to render
            time.sleep(wait_seconds)

            # Get text content (accessibility snapshot)
            snapshot = self.get_snapshot(tab_id)

            # Get screenshot for multimodal analysis
            screenshot_bytes = self.get_screenshot(tab_id)
            screenshot_b64 = None
            if screenshot_bytes and len(screenshot_bytes) > 1000:
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            # Get all links (for "link in comments" detection)
            links = self.get_links(tab_id)

            result = {
                "text": snapshot or "",
                "screenshot_b64": screenshot_b64,
                "links": links,
                "url": url,
            }

            text_len = len(result["text"])
            logger.info(
                f"Camofox extracted: {text_len} chars, "
                f"screenshot={'yes' if screenshot_b64 else 'no'}, "
                f"{len(links)} links"
            )

            return result

        except Exception as e:
            logger.error(f"Camofox extract_page failed: {e}")
            return None

        finally:
            self.close_tab(tab_id)
