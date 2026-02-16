"""
Batch Digest — process multiple queued articles into one summary.

Usage:
    from services.digest import create_batch_digest

    result = create_batch_digest(db_path, n=5)
    print(result.output)       # Digest text
    print(result.article_ids)  # IDs processed
"""
import logging
from dataclasses import dataclass, field
from typing import Optional

from db.repository import (
    add_batch_digest,
    get_newest_queued_articles,
    update_article_status,
)
from services.extractor import extract_content
from services.llm_client import call_llm_with_fallback, load_prompt

logger = logging.getLogger(__name__)

MAX_ARTICLE_CHARS = 2000  # Truncate each article to keep total prompt manageable


@dataclass
class DigestResult:
    """Result of batch digest processing."""

    output: Optional[str] = None
    article_ids: list[int] = field(default_factory=list)
    article_titles: dict[int, str] = field(default_factory=dict)
    articles_processed: int = 0
    articles_skipped: int = 0
    skipped_titles: list[str] = field(default_factory=list)
    success: bool = False
    error: Optional[str] = None


def create_batch_digest(db_path: str, n: int = 5) -> DigestResult:
    """
    Create a batch digest from the oldest N queued articles.

    Steps:
        1. Get N oldest queued articles
        2. Extract content for each
        3. Combine into single LLM prompt
        4. Generate digest
        5. Save to DB + update article statuses

    Args:
        db_path: Path to SQLite database
        n: Number of articles to include (default 5, max 10)

    Returns:
        DigestResult with output and metadata
    """
    result = DigestResult()
    n = max(2, min(n, 10))  # Clamp to 2-10

    # 1. Get queued articles
    articles = get_newest_queued_articles(db_path, n)
    if not articles:
        result.error = "Không có bài nào trong queue."
        return result

    # 2. Extract content for each article
    article_texts = []
    for article in articles:
        article_id = article["id"]
        title = article.get("title", "Untitled")
        url = article.get("source_url", "")
        raw_content = article.get("raw_content", "")

        # Use existing raw_content if available, otherwise extract
        if raw_content and len(raw_content) > 100:
            content = raw_content
        elif url:
            try:
                logger.info(f"Extracting article #{article_id}: {title[:50]}")
                extraction = extract_content(url)
                content = extraction.content if extraction.content else ""
            except Exception as e:
                logger.warning(f"Extraction failed for #{article_id}: {e}")
                result.articles_skipped += 1
                result.skipped_titles.append(f"#{article_id}: {title}")
                continue
        else:
            result.articles_skipped += 1
            result.skipped_titles.append(f"#{article_id}: {title} (no URL)")
            continue

        if not content:
            result.articles_skipped += 1
            result.skipped_titles.append(f"#{article_id}: {title} (empty)")
            continue

        # Truncate long articles
        if len(content) > MAX_ARTICLE_CHARS:
            content = content[:MAX_ARTICLE_CHARS] + "\n\n[... truncated ...]"

        article_texts.append({
            "id": article_id,
            "title": title,
            "url": url,
            "content": content,
        })
        result.article_ids.append(article_id)
        result.article_titles[article_id] = title

    if not article_texts:
        result.error = "Không extract được bài nào."
        return result

    result.articles_processed = len(article_texts)

    # 3. Build combined prompt
    combined_text = _build_combined_text(article_texts)

    # 4. Call LLM
    try:
        logger.info(f"Generating digest for {len(article_texts)} articles...")
        system_prompt = load_prompt("digest.md").format(
            n_articles=len(article_texts)
        )
        digest_output = call_llm_with_fallback(
            task_type="batch_digest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": combined_text},
            ],
        )
        result.output = digest_output
        result.success = True
        logger.info("Digest generation complete ✓")
    except Exception as e:
        logger.error(f"Digest LLM call failed: {e}")
        result.error = f"LLM digest failed: {e}"
        return result

    # 5. Save to DB + update statuses
    try:
        add_batch_digest(
            db_path,
            article_ids=result.article_ids,
            digest_output=digest_output,
        )
        for aid in result.article_ids:
            update_article_status(db_path, aid, "digest_reviewed")
        logger.info(f"Digest saved, {len(result.article_ids)} articles → digest_reviewed")
    except Exception as e:
        logger.error(f"Error saving digest to DB: {e}")
        # Don't fail the result — LLM output is still valid
        result.error = f"Digest generated but DB save failed: {e}"

    return result


def _build_combined_text(article_texts: list[dict]) -> str:
    """Build combined text from extracted articles."""
    sections = []
    for art in article_texts:
        sections.append(
            f"## Article #{art['id']}: {art['title']}\n"
            f"🔗 {art['url']}\n\n"
            f"{art['content']}"
        )
    return "\n\n---\n\n".join(sections)
