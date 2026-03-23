"""TranslationSkill — translate chapter/section Markdown to Urdu.

Preserves:
  - Markdown structure (headings, code blocks, lists, bold/italic)
  - Technical terms in English (e.g. ROS 2, Qdrant, VLA, Nav2)
  - Code blocks verbatim — never translated
"""
from __future__ import annotations

import anthropic

from app.config import get_settings

_SYSTEM = (
    "You are a professional technical translator specialising in robotics and AI content.\n"
    "Translate the following Markdown text from English to Urdu.\n\n"
    "Rules:\n"
    "1. Keep ALL Markdown syntax intact: ##, ###, **, *, -, ```, etc.\n"
    "2. NEVER translate content inside ``` code blocks — leave them verbatim.\n"
    "3. Keep English technical terms as-is (e.g. ROS 2, Nav2, Qdrant, VLA, Isaac Sim, "
    "   Jetson Orin Nano, Python, CUDA). You may add Urdu explanation in parentheses the first time.\n"
    "4. URLs, filenames, variable names — never translate.\n"
    "5. Return ONLY the translated Markdown — no preamble or explanation."
)


async def run_translation_skill(
    content: str,
    target_language: str = "ur",
) -> dict:
    """Translate Markdown content to the target language.

    Args:
        content: Markdown text to translate.
        target_language: ISO code — currently only "ur" (Urdu) is supported.

    Returns:
        dict with keys: translated_content, target_language, original_length, translated_length
    """
    if target_language != "ur":
        return {
            "error": f"Language '{target_language}' is not yet supported. Only 'ur' (Urdu) is available."
        }

    settings = get_settings()
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    stream = client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=8192,
        system=_SYSTEM,
        messages=[{"role": "user", "content": content}],
    )

    final = await stream.get_final_message()
    translated = next(
        (b.text for b in final.content if b.type == "text"), ""
    )

    return {
        "translated_content": translated,
        "target_language": target_language,
        "original_length": len(content),
        "translated_length": len(translated),
    }
