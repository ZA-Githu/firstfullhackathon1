from __future__ import annotations

from dataclasses import dataclass

import cohere
from fastapi import HTTPException

from app.config import get_settings


@dataclass
class GeneratorResult:
    answer: str
    tokens_used: int


async def generate(
    system_prompt: str,
    query: str,
    history: list[dict[str, str]],
) -> GeneratorResult:
    settings = get_settings()
    client = cohere.AsyncClientV2(api_key=settings.cohere_api_key)

    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt}
    ]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": query})

    try:
        response = await client.chat(
            model="command-r-plus-08-2024",
            messages=messages,  # type: ignore[arg-type]
            max_tokens=settings.max_answer_tokens,
        )
    except cohere.BadRequestError as exc:
        raise HTTPException(
            status_code=503, detail="LLM service unavailable"
        ) from exc

    answer = response.message.content[0].text if response.message.content else ""
    tokens = response.usage.tokens.output_tokens if response.usage and response.usage.tokens else 0
    return GeneratorResult(answer=answer, tokens_used=tokens)
