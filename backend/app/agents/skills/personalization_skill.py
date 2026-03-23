"""PersonalizationSkill — adapt chapter content to a user's background.

Uses the user's profile (experience level, domain background from sign-up)
to rewrite or annotate a chapter section for their skill level.
"""
from __future__ import annotations

import anthropic

from app.config import get_settings

_SYSTEM = (
    "You are an adaptive learning assistant for the Physical AI & Humanoid Robotics textbook.\n"
    "Your job is to personalise a given chapter excerpt for a specific learner profile.\n"
    "Rules:\n"
    "1. Keep ALL technical content accurate — never remove facts, only adjust depth.\n"
    "2. Preserve Markdown structure (headings, code blocks, lists).\n"
    "3. For beginners: add analogies, expand jargon explanations, add beginner tips.\n"
    "4. For advanced users: add deeper technical notes, link to advanced topics, trim basics.\n"
    "5. Do NOT hallucinate new technical claims; only annotate or adjust existing content.\n"
    "6. Return ONLY the personalised Markdown — no preamble."
)


async def run_personalization_skill(
    content: str,
    user_background: str,
    experience_level: str = "intermediate",
) -> dict:
    """Personalise chapter content for a user's profile.

    Args:
        content: Original Markdown chapter content.
        user_background: e.g. "5 years Python, no robotics experience".
        experience_level: "beginner" | "intermediate" | "advanced".

    Returns:
        dict with keys: personalised_content, experience_level, original_word_count, new_word_count
    """
    settings = get_settings()
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_msg = (
        f"Learner profile:\n"
        f"- Background: {user_background}\n"
        f"- Experience level: {experience_level}\n\n"
        f"Adapt this textbook content accordingly:\n\n{content}"
    )

    stream = client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )

    final = await stream.get_final_message()
    personalised = next(
        (b.text for b in final.content if b.type == "text"), content
    )

    return {
        "personalised_content": personalised,
        "experience_level": experience_level,
        "original_word_count": len(content.split()),
        "new_word_count": len(personalised.split()),
    }
