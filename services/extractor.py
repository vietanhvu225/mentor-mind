"""
Smart Content Extractor — extract text, images, and video transcripts from URLs.

Supports:
- Articles/blogs: trafilatura (primary) + Jina Reader (fallback)
- Images: download important images for multimodal Gemini analysis
- YouTube: transcript extraction via youtube-transcript-api
- Reels/Stories: flag for direct viewing
- Short content / "link in comments": detect + follow URLs
- Camofox browser: enhanced extraction for walled gardens (Facebook, LinkedIn)
"""

import base64
import logging
import re
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse, parse_qs

import httpx
import trafilatura
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────
SHORT_CONTENT_THRESHOLD = 200  # words
MAX_IMAGES = 5
MIN_IMAGE_SIZE = 100  # pixels (width or height)
FETCH_TIMEOUT = 15.0  # seconds
JINA_BASE = "https://r.jina.ai"


# ═══════════════════════════════════════════════════════════════════
#  CAMOFOX SNAPSHOT CLEANING
# ═══════════════════════════════════════════════════════════════════

# Lines starting with these prefixes (after stripping indent + "- ") are UI noise
_NOISE_PREFIXES = (
    "button ", "link ", "img ", "img\n", "combobox ", "textbox ",
    "navigation ", "banner", "separator", "slider ", "toolbar ",
    "status ", "listitem", "list:", "table:", "paragraph",
    "dialog:", "group ",
)

# Lines containing these substrings are noise even inside text nodes
_NOISE_SUBSTRINGS = (
    "/url:", "- /url:", "[pressed]", "[disabled]",
)


def clean_camofox_snapshot(raw: str) -> str:
    """
    Clean a Camofox accessibility snapshot by extracting only meaningful text.

    Keeps:
      - `- text: "..."` content lines (post body, comments)
      - `article "Comment by ..."` headers (comment attribution)
      - `heading "..."` lines

    Strips:
      - Navigation bars, buttons, links, images, toolbars, sliders
      - Facebook UI elements (Like, Share, React, Menu, etc.)
      - URL/href lines

    Returns:
        Cleaned text with only meaningful content, ~60-70% smaller.
    """
    if not raw:
        return ""

    cleaned_lines = []
    for line in raw.split("\n"):
        stripped = line.lstrip(" -")

        # Skip empty
        if not stripped:
            continue

        # Keep text content nodes
        if stripped.startswith("text: "):
            # Extract the text value
            text_val = stripped[6:].strip().strip('"')
            if text_val and len(text_val) > 2:
                cleaned_lines.append(text_val)
            continue

        # Keep comment attribution headers
        if stripped.startswith("article ") and "Comment by" in stripped:
            # e.g. article "Comment by Thedigitalkinggg 8 hours ago"
            attr = stripped.replace('article "', "").rstrip('"').rstrip(":")
            cleaned_lines.append(f"\n--- {attr} ---")
            continue

        # Keep headings
        if stripped.startswith("heading ") and "[level=" in stripped:
            heading_text = stripped.split('"')[1] if '"' in stripped else ""
            if heading_text:
                cleaned_lines.append(f"\n## {heading_text}")
            continue

        # Skip known noise patterns
        is_noise = False
        for prefix in _NOISE_PREFIXES:
            if stripped.startswith(prefix):
                is_noise = True
                break
        if is_noise:
            continue

        for substr in _NOISE_SUBSTRINGS:
            if substr in stripped:
                is_noise = True
                break
        if is_noise:
            continue

        # Keep anything else that looks like text (not indented tree structure markers)
        if not stripped.startswith(("'button", "'img", "- button", "- link", "- img")):
            # Only keep if it has some alphabetic content
            if any(c.isalpha() for c in stripped) and len(stripped) > 5:
                cleaned_lines.append(stripped)

    result = "\n".join(cleaned_lines)
    # Collapse multiple blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()

# URL patterns for content type detection
YOUTUBE_PATTERNS = [
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
]
SHORT_VIDEO_PATTERNS = [
    r"instagram\.com/(?:reel|stories)/",
    r"tiktok\.com/",
    r"facebook\.com/(?:reel|stories)/",
    r"fb\.watch/",
]


@dataclass
class ExtractionResult:
    """Result of content extraction."""
    content: str = ""
    images: list[dict] = field(default_factory=list)  # [{url, base64, mime_type}]
    content_type: str = "article"  # article | youtube | short_video
    source: str = "none"  # trafilatura | jina | youtube_transcript | excerpt | followed_url | camofox
    word_count: int = 0
    warnings: list[str] = field(default_factory=list)
    video_id: Optional[str] = None  # YouTube video ID
    github_links: list[str] = field(default_factory=list)  # GitHub repo URLs found in content


# ═══════════════════════════════════════════════════════════════════
#  CONTENT TYPE DETECTION
# ═══════════════════════════════════════════════════════════════════

def detect_content_type(url: str) -> tuple[str, Optional[str]]:
    """
    Detect content type from URL pattern.

    Returns:
        (content_type, video_id) where content_type is
        "youtube", "short_video", or "article".
    """
    for pattern in YOUTUBE_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return "youtube", match.group(1)

    for pattern in SHORT_VIDEO_PATTERNS:
        if re.search(pattern, url):
            return "short_video", None

    return "article", None


# ═══════════════════════════════════════════════════════════════════
#  ARTICLE TEXT EXTRACTION
# ═══════════════════════════════════════════════════════════════════

def _fetch_html(url: str) -> Optional[str]:
    """Fetch raw HTML from URL with timeout."""
    try:
        downloaded = trafilatura.fetch_url(url)
        return downloaded
    except Exception as e:
        logger.warning(f"Failed to fetch HTML: {e}")
        return None


def extract_with_trafilatura(url: str) -> tuple[Optional[str], Optional[str]]:
    """
    Extract article text using trafilatura.

    Returns:
        (text_content, raw_html) — both may be None on failure.
    """
    try:
        downloaded = _fetch_html(url)
        if not downloaded:
            return None, None

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            favor_precision=True,
        )
        return text, downloaded

    except Exception as e:
        logger.error(f"Trafilatura extraction failed: {e}")
        return None, None


def extract_with_jina(url: str) -> Optional[str]:
    """
    Extract article text using Jina Reader API (fallback).

    Returns:
        Extracted text or None.
    """
    try:
        jina_url = f"{JINA_BASE}/{url}"
        with httpx.Client(timeout=FETCH_TIMEOUT) as client:
            response = client.get(
                jina_url,
                headers={"Accept": "text/plain"},
            )
            response.raise_for_status()
            text = response.text.strip()
            if text and len(text) > 50:
                logger.info(f"Jina Reader extracted {len(text)} chars")
                return text
            return None
    except Exception as e:
        logger.warning(f"Jina Reader failed: {e}")
        return None


def _count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def _find_urls_in_text(text: str) -> list[str]:
    """Extract URLs from text content."""
    url_pattern = r'https?://[^\s<>"\')\]]+[^\s<>"\')\].,;:!?]'
    return re.findall(url_pattern, text)


def _is_walled_garden(url: str) -> bool:
    """Check if URL is from a platform that requires login (Facebook, LinkedIn, etc.)."""
    patterns = ["facebook.com", "fb.com", "linkedin.com", "instagram.com"]
    return any(p in url.lower() for p in patterns)


def extract_facebook_meta(url: str) -> tuple[Optional[str], list[str]]:
    """
    Extract content from Facebook/LinkedIn via OG meta tags.

    These platforms serve post text in og:description and images in og:image
    even without login (for SEO/sharing preview purposes).

    Returns:
        (text_content, image_urls) — text from og:description, images from og:image.
    """
    try:
        with httpx.Client(
            timeout=FETCH_TIMEOUT,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            },
        ) as client:
            resp = client.get(url)
            resp.raise_for_status()
            html = resp.text

        soup = BeautifulSoup(html, "html.parser")

        # Extract text from og:description (Facebook puts full post text here)
        og_desc = soup.find("meta", property="og:description")
        text = og_desc.get("content", "") if og_desc else ""

        # Also check for standard meta description as backup
        if not text:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            text = meta_desc.get("content", "") if meta_desc else ""

        # Decode HTML entities
        if text:
            import html as html_module
            text = html_module.unescape(text)

        # Extract images from og:image AND twitter:image
        og_images = soup.find_all("meta", property="og:image")
        tw_images = soup.find_all("meta", attrs={"name": "twitter:image"})
        image_urls = []
        seen_urls = set()
        for img_tag in og_images + tw_images:
            img_url = img_tag.get("content", "")
            if img_url:
                import html as html_module
                img_url = html_module.unescape(img_url)
            if img_url and img_url not in seen_urls and not any(p in img_url.lower() for p in ["favicon", "logo", "icon"]):
                seen_urls.add(img_url)
                image_urls.append(img_url)

        logger.info(f"Facebook meta: {len(text)} chars, {len(image_urls)} images")
        return text if text else None, image_urls

    except Exception as e:
        logger.warning(f"Facebook meta extraction failed: {e}")
        return None, []


# ═══════════════════════════════════════════════════════════════════
#  IMAGE EXTRACTION
# ═══════════════════════════════════════════════════════════════════

def extract_image_urls(html: str, base_url: str) -> list[str]:
    """
    Extract important image URLs from HTML.

    Filters: skip small images (icons/avatars), ads, tracking pixels.
    Returns up to MAX_IMAGES URLs sorted by likely importance.
    """
    if not html:
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
        img_urls = []

        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or ""
            if not src or src.startswith("data:"):
                continue

            # Make absolute URL
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                parsed = urlparse(base_url)
                src = f"{parsed.scheme}://{parsed.netloc}{src}"

            # Filter out tiny images (icons, tracking pixels)
            width = img.get("width", "")
            height = img.get("height", "")
            try:
                if width and int(str(width).replace("px", "")) < MIN_IMAGE_SIZE:
                    continue
                if height and int(str(height).replace("px", "")) < MIN_IMAGE_SIZE:
                    continue
            except (ValueError, TypeError):
                pass

            # Skip common ad/tracking patterns
            skip_patterns = [
                "pixel", "tracking", "analytics", "ad-", "advertisement",
                "favicon", "logo", "icon", "avatar", "emoji", "badge",
                "spacer", "1x1", "blank.gif",
            ]
            src_lower = src.lower()
            if any(p in src_lower for p in skip_patterns):
                continue

            img_urls.append(src)

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for u in img_urls:
            if u not in seen:
                seen.add(u)
                unique.append(u)

        result = unique[:MAX_IMAGES]
        logger.info(f"Found {len(unique)} images, using top {len(result)}")
        return result

    except Exception as e:
        logger.warning(f"Image extraction failed: {e}")
        return []


def download_images(urls: list[str]) -> list[dict]:
    """
    Download images and encode as base64 for Gemini multimodal.

    Returns:
        List of {url, base64, mime_type} dicts.
    """
    images = []
    for url in urls:
        try:
            with httpx.Client(
                timeout=10.0,
                follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0"},
            ) as client:
                resp = client.get(url)
                resp.raise_for_status()

                content_type = resp.headers.get("content-type", "")
                if not content_type.startswith("image/"):
                    continue

                # Skip tiny images (< 5KB likely icons)
                if len(resp.content) < 5000:
                    continue

                b64 = base64.b64encode(resp.content).decode("utf-8")
                mime = content_type.split(";")[0].strip()

                images.append({
                    "url": url,
                    "base64": b64,
                    "mime_type": mime,
                })
                logger.debug(f"Downloaded image: {url} ({len(resp.content)} bytes)")

        except Exception as e:
            logger.debug(f"Failed to download image {url}: {e}")
            continue

    logger.info(f"Downloaded {len(images)}/{len(urls)} images")
    return images


# ═══════════════════════════════════════════════════════════════════
#  YOUTUBE TRANSCRIPT EXTRACTION
# ═══════════════════════════════════════════════════════════════════

def extract_youtube_transcript(video_id: str) -> Optional[str]:
    """
    Extract transcript from YouTube video.

    Tries Vietnamese first, then English, then auto-generated.

    Returns:
        Transcript text or None.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        # Try different language preferences
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        transcript = None
        # Priority: Vietnamese manual → English manual → any manual → any generated
        for lang in ["vi", "en"]:
            try:
                transcript = transcript_list.find_transcript([lang])
                break
            except Exception:
                continue

        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(["vi", "en"])
            except Exception:
                pass

        if transcript is None:
            # Try any available transcript
            for t in transcript_list:
                transcript = t
                break

        if transcript is None:
            return None

        # Fetch and join transcript snippets
        snippets = transcript.fetch()
        text_parts = [s.text for s in snippets]
        full_text = " ".join(text_parts)

        logger.info(f"YouTube transcript: {len(full_text)} chars, {_count_words(full_text)} words")
        return full_text

    except Exception as e:
        logger.warning(f"YouTube transcript extraction failed: {e}")
        return None


def _get_youtube_info(video_id: str) -> tuple[str, str]:
    """Get YouTube video title and description via oEmbed."""
    try:
        url = f"https://www.youtube.com/oembed?url=https://youtube.com/watch?v={video_id}&format=json"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json()
            return data.get("title", ""), data.get("author_name", "")
    except Exception:
        return "", ""


# ═══════════════════════════════════════════════════════════════════
#  GITHUB README ENRICHMENT
# ═══════════════════════════════════════════════════════════════════

MAX_README_CHARS = 3000  # Truncate README to this length


def fetch_github_readme(github_url: str) -> Optional[str]:
    """
    Fetch README.md from a GitHub repo for content enrichment.

    Tries raw.githubusercontent.com with main/master branches.

    Args:
        github_url: GitHub repo URL (e.g. https://github.com/owner/repo)

    Returns:
        README content (truncated to MAX_README_CHARS) or None on failure.
    """
    # Extract owner/repo from URL
    match = re.search(r'github\.com/([\w.-]+)/([\w.-]+)', github_url)
    if not match:
        return None

    owner, repo = match.group(1), match.group(2)

    # Try main, then master branch
    for branch in ("main", "master"):
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
        try:
            resp = httpx.get(raw_url, timeout=10.0, follow_redirects=True)
            if resp.status_code == 200 and len(resp.text) > 50:
                readme = resp.text
                if len(readme) > MAX_README_CHARS:
                    readme = readme[:MAX_README_CHARS] + "\n\n[... truncated ...]"
                logger.info(
                    f"Fetched README from {owner}/{repo} ({branch}): "
                    f"{len(readme)} chars"
                )
                return readme
        except Exception as e:
            logger.debug(f"README fetch failed ({branch}): {e}")

    logger.info(f"No README found for {owner}/{repo}")
    return None


# ═══════════════════════════════════════════════════════════════════
#  ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════

def extract_content(url: str, excerpt: Optional[str] = None) -> ExtractionResult:
    """
    Smart content extraction — detect type and extract accordingly.

    Args:
        url: The URL to extract content from.
        excerpt: Raindrop excerpt as ultimate fallback.

    Returns:
        ExtractionResult with content, images, type, warnings.
    """
    result = ExtractionResult()
    content_type, video_id = detect_content_type(url)
    result.content_type = content_type
    result.video_id = video_id

    # ── Short Video (Reel/Story/TikTok) ───────────────────────────
    if content_type == "short_video":
        result.warnings.append(f"📱 Short video — xem trực tiếp: {url}")
        result.content = excerpt or ""
        result.source = "excerpt"
        result.word_count = _count_words(result.content)
        return result

    # ── YouTube ───────────────────────────────────────────────────
    if content_type == "youtube" and video_id:
        title, author = _get_youtube_info(video_id)
        transcript = extract_youtube_transcript(video_id)

        if transcript:
            header = f"[YouTube Video] {title}\nBy: {author}\n\n" if title else ""
            result.content = header + transcript
            result.source = "youtube_transcript"
            result.word_count = _count_words(result.content)
            return result
        else:
            result.warnings.append(
                f"🎬 Video không có transcript — xem trực tiếp: {url}"
            )
            result.content = f"[YouTube Video] {title}\nBy: {author}" if title else ""
            result.source = "excerpt"
            result.word_count = _count_words(result.content)
            return result

    # ── Article / Blog / Social Post ──────────────────────────────
    og_image_urls = []  # images from OG tags (Facebook, LinkedIn)

    # For walled gardens (Facebook, LinkedIn), try Camofox first, then OG meta
    if _is_walled_garden(url):
        # Strategy 1: Camofox browser (full render, anti-detection)
        try:
            from services.camofox_client import CamofoxClient
            camofox = CamofoxClient()
            if camofox.is_available():
                page_data = camofox.extract_page(url)
                if page_data and page_data.get("text") and len(page_data["text"]) > 50:
                    raw_text = page_data["text"]
                    cleaned = clean_camofox_snapshot(raw_text)
                    result.content = cleaned
                    result.source = "camofox"
                    result.word_count = _count_words(result.content)
                    logger.info(
                        f"Camofox: {len(raw_text)} raw → {len(cleaned)} cleaned chars "
                        f"({result.word_count} words) from walled garden"
                    )
                    # Use screenshot as multimodal image
                    if page_data.get("screenshot_b64"):
                        result.images.append({
                            "base64": page_data["screenshot_b64"],
                            "mime_type": "image/png",
                            "url": "camofox_screenshot",
                        })
                    # Save page links for "link in comments" detection
                    if page_data.get("links"):
                        result.warnings.append(
                            f"🔗 Camofox found {len(page_data['links'])} links on page"
                        )
        except Exception as e:
            logger.debug(f"Camofox not available: {e}")

        # Strategy 2: OG meta tags fallback
        if not result.content:
            fb_text, og_image_urls = extract_facebook_meta(url)
            if fb_text and _count_words(fb_text) > 0:
                result.content = fb_text
                result.source = "og_meta"
                result.word_count = _count_words(result.content)
                logger.info(
                    f"Walled garden: extracted {result.word_count} words via OG meta"
                )

        # Don't try trafilatura for walled gardens (will fail)
        text, raw_html = None, None
    else:
        text, raw_html = extract_with_trafilatura(url)

    if not result.content and text and _count_words(text) >= SHORT_CONTENT_THRESHOLD:
        result.content = text
        result.source = "trafilatura"
    elif not result.content:
        # Try Jina Reader as fallback
        jina_text = extract_with_jina(url)
        if jina_text and _count_words(jina_text) >= SHORT_CONTENT_THRESHOLD:
            result.content = jina_text
            result.source = "jina"
            if not raw_html:
                raw_html = _fetch_html(url)
        elif not result.content and text and _count_words(text) > 0:
            result.content = text
            result.source = "trafilatura"
        elif not result.content and jina_text and _count_words(jina_text) > 0:
            result.content = jina_text
            result.source = "jina"

    if not result.word_count:
        result.word_count = _count_words(result.content)

    # ── Short content detection + URL follow ──────────────────────
    if result.word_count < SHORT_CONTENT_THRESHOLD and result.content:
        # Combine URLs from content text + excerpt
        all_text_for_urls = result.content
        if excerpt:
            all_text_for_urls += " " + excerpt
        urls_in_text = _find_urls_in_text(all_text_for_urls)
        # Filter out the original URL and common non-article URLs
        candidate_urls = [
            u for u in urls_in_text
            if u != url
            and not any(p in u for p in ["t.co/", "bit.ly/", "#", "javascript:", "facebook.com", "fb.com"])
        ]

        if candidate_urls:
            best_url = max(candidate_urls, key=len)
            logger.info(f"Short content detected, following URL: {best_url}")
            result.warnings.append(
                f"🔗 Bài gốc ngắn — đang follow link: {best_url}"
            )

            followed_text, followed_html = extract_with_trafilatura(best_url)
            if followed_text and _count_words(followed_text) > result.word_count:
                result.content = followed_text
                result.source = "followed_url"
                result.word_count = _count_words(result.content)
                raw_html = followed_html
                url = best_url
            else:
                result.warnings.append(
                    f"⚠️ Bài ngắn — có thể là social post. Xem trực tiếp: {url}"
                )
        else:
            result.warnings.append(
                f"⚠️ Bài ngắn ({result.word_count} words) — xem trực tiếp: {url}"
            )

    # ── Ultimate fallback: excerpt ────────────────────────────────
    if not result.content and excerpt:
        result.content = excerpt
        result.source = "excerpt"
        result.word_count = _count_words(result.content)
        result.warnings.append("⚠️ Không extract được content, dùng excerpt")

    # ── Extract images for multimodal ─────────────────────────────
    # Priority: OG images (Facebook) > HTML img tags
    if og_image_urls:
        image_urls_to_download = og_image_urls[:MAX_IMAGES]
        result.images = download_images(image_urls_to_download)
        if len(og_image_urls) > MAX_IMAGES:
            result.warnings.append(
                f"🖼️ Bài có {len(og_image_urls)} ảnh — chỉ phân tích top {MAX_IMAGES}"
            )
    elif raw_html and result.content_type == "article":
        image_urls = extract_image_urls(raw_html, url)
        if image_urls:
            result.images = download_images(image_urls)
            if len(image_urls) > MAX_IMAGES:
                result.warnings.append(
                    f"🖼️ Bài có {len(image_urls)} ảnh — chỉ phân tích top {MAX_IMAGES}"
                )

    # ── Extract GitHub links from content ───────────────────────
    if result.content:
        # Match github.com/owner/repo with or without protocol
        github_pattern = r'(?:https?://)?github\.com/[\w.-]+/[\w.-]+'
        raw_links = re.findall(github_pattern, result.content)
        # Deduplicate, clean, and normalize
        seen = set()
        for link in raw_links:
            # Clean trailing dots, commas, parens
            clean = link.rstrip('.,;:)]\'"')
            # Ensure https:// prefix
            if not clean.startswith('http'):
                clean = f'https://{clean}'
            if clean not in seen:
                seen.add(clean)
                result.github_links.append(clean)
        if result.github_links:
            logger.info(f"Found {len(result.github_links)} GitHub link(s) in content")

    # ── Enrich with GitHub README when content is short ───────────
    if result.github_links and result.word_count < 500:
        for gh_url in result.github_links[:2]:  # Max 2 repos
            readme = fetch_github_readme(gh_url)
            if readme:
                result.content += f"\n\n{'='*40}\n📖 README — {gh_url}\n{'='*40}\n{readme}"
                result.word_count = _count_words(result.content)
                logger.info(
                    f"Enriched with README from {gh_url} "
                    f"(now {result.word_count} words)"
                )

    return result
