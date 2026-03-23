from __future__ import annotations

import uuid

import asyncpg

from app.db import postgres
from app.models.requests import ChatSelectedRequest
from app.models.responses import ChatSelectedResponse
from app.services import generator

_CANNOT_ANSWER = "This question cannot be answered from the selected text alone."

_SYSTEM = (
    "You are a teaching assistant. Answer ONLY based on the following text excerpt.\n"
    "If the question cannot be answered from this excerpt, respond with exactly:\n"
    f'"{_CANNOT_ANSWER}"\n\n'
    "Excerpt:\n{selected_text}"
)


async def run_selected(
    request: ChatSelectedRequest,
    pool: asyncpg.Pool,
) -> ChatSelectedResponse:
    session_id = (
        str(request.session_id) if request.session_id else str(uuid.uuid4())
    )

    if request.language == "ur":
        return ChatSelectedResponse(
            answer="Urdu translation coming soon.",
            session_id=uuid.UUID(session_id),
            tokens_used=0,
        )

    system_prompt = _SYSTEM.format(selected_text=request.selected_text)
    history = await postgres.get_session_history(pool, session_id) if pool else []
    result = await generator.generate(system_prompt, request.query, history)

    if pool:
        await postgres.save_session_messages(
            pool, session_id, request.query, result.answer
        )

    return ChatSelectedResponse(
        answer=result.answer,
        session_id=uuid.UUID(session_id),
        tokens_used=result.tokens_used,
    )
