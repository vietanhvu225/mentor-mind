"""
Article Analyzer — 2-stage pipeline for daily article analysis.

Stage 1 (Gemini 3 Pro): Multi-persona analysis (Researcher + Architect + Skeptic)
Stage 2 (Claude Opus 4.6): Synthesis + Action Planning

Usage:
    from services.analyzer import analyze_article

    result = analyze_article("Full article text here...")
    print(result.stage_1_output)  # 3-persona analysis
    print(result.stage_2_output)  # Synthesizer + Action Plan
"""
import logging
from dataclasses import dataclass, field
from typing import Optional

from services.llm_client import call_llm_with_fallback, load_prompt

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Result of the 2-stage analysis pipeline."""

    stage_1_output: Optional[str] = None
    stage_2_output: Optional[str] = None
    article_link: Optional[str] = None
    stage_1_success: bool = False
    stage_2_success: bool = False
    warning: Optional[str] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """True if at least Stage 1 succeeded."""
        return self.stage_1_success

    @property
    def full_success(self) -> bool:
        """True if both stages succeeded."""
        return self.stage_1_success and self.stage_2_success


def _build_stage_1_prompt() -> str:
    """Build Stage 1 system prompt with embedded persona prompts."""
    from datetime import date
    template = load_prompt("daily_analysis.md")
    researcher = load_prompt("personas/researcher.md")
    architect = load_prompt("personas/architect.md")
    skeptic = load_prompt("personas/skeptic.md")

    return template.format(
        today_date=date.today().isoformat(),
        researcher_prompt=researcher,
        architect_prompt=architect,
        skeptic_prompt=skeptic,
    )


def _build_stage_2_prompt() -> str:
    """Build Stage 2 system prompt with embedded synthesizer prompt."""
    template = load_prompt("action_planning.md")
    synthesizer = load_prompt("personas/synthesizer.md")

    return template.format(
        synthesizer_prompt=synthesizer,
    )


def analyze_article(
    article_text: str,
    article_link: Optional[str] = None,
    images: Optional[list[dict]] = None,
) -> AnalysisResult:
    """
    Run the 2-stage analysis pipeline on an article.

    Stage 1 (analysis): Gemini 3 Pro — 3 personas (supports multimodal)
    Stage 2 (planning): Claude Opus 4.6 — synthesizer + action plan

    Graceful degradation:
    - Stage 1 fails → return error with article link
    - Stage 2 fails → return Stage 1 output with warning

    Args:
        article_text: Full text of the article to analyze.
        article_link: Optional URL of the original article.
        images: Optional list of image dicts with {base64, mime_type} for multimodal.

    Returns:
        AnalysisResult with outputs from both stages (or partial).
    """
    result = AnalysisResult(article_link=article_link)

    # ── Stage 1: Multi-persona analysis ────────────────────────────
    try:
        logger.info("Stage 1: Starting multi-persona analysis...")
        system_prompt = _build_stage_1_prompt()

        # Build user message — multimodal if images available
        if images:
            # OpenAI-compatible multimodal format
            user_content = [{"type": "text", "text": article_text}]
            for img in images:
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{img['mime_type']};base64,{img['base64']}",
                    },
                })
            logger.info(f"Multimodal input: text + {len(images)} images")
        else:
            user_content = article_text

        stage_1_output = call_llm_with_fallback(
            task_type="stage_1_analysis",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        result.stage_1_output = stage_1_output
        result.stage_1_success = True
        logger.info("Stage 1: Complete ✓")

    except Exception as e:
        logger.error("Stage 1 FAILED: %s", e)
        result.error = f"Stage 1 failed: {e}"
        # Do NOT call Stage 2 if Stage 1 failed
        return result

    # ── Stage 2: Synthesis + Action Planning ───────────────────────
    try:
        logger.info("Stage 2: Starting synthesis & action planning...")
        system_prompt = _build_stage_2_prompt()
        stage_2_output = call_llm_with_fallback(
            task_type="stage_2_planning",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": stage_1_output},
            ],
        )
        result.stage_2_output = stage_2_output
        result.stage_2_success = True
        logger.info("Stage 2: Complete ✓")

    except Exception as e:
        logger.warning("Stage 2 FAILED (Stage 1 OK, degrading gracefully): %s", e)
        result.warning = (
            "⚠️ Phần tổng hợp và action plan không khả dụng. "
            "Chỉ hiển thị phân tích từ 3 personas."
        )

    return result
