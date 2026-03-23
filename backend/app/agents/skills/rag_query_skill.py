"""RAGQuerySkill — embed query → retrieve Qdrant → generate grounded answer.

Supports two modes:
  - general: full vector retrieval from the book
  - selected: answer grounded in caller-supplied text only (no retrieval)

Reuses existing services: embedder, retriever, generator.
"""
from __future__ import annotations

import uuid
from typing import Literal

from qdrant_client import QdrantClient

from app.config import get_settings
from app.db import postgres
from app.services import embedder, generator, retriever


async def run_rag_query_skill(
    query: str,
    mode: Literal["general", "selected"] = "general",
    selected_text: str | None = None,
    top_k: int = 5,
    session_id: str | None = None,
    pool=None,
    qdrant_client: QdrantClient | None = None,
) -> dict:
    """Execute a RAG query and return answer + sources.

    Args:
        query: User question.
        mode: "general" uses vector retrieval; "selected" uses only selected_text.
        selected_text: Required when mode=="selected".
        top_k: Number of chunks to retrieve (general mode only).
        session_id: Optional session ID for history tracking.
        pool: asyncpg pool (injected by the route).
        qdrant_client: Qdrant client (injected by the route).

    Returns:
        dict with keys: answer, sources, session_id, tokens_used
    """
    settings = get_settings()
    sid = session_id or str(uuid.uuid4())

    if mode == "selected":
        if not selected_text:
            return {"error": "selected_text is required for selected mode"}
        context = selected_text
        sources: list[dict] = []
    else:
        vectors = await embedder.embed_texts([query])
        chunks = await retriever.retrieve(
            vectors[0], top_k, settings.qdrant_collection, qdrant_client
        )
        context = (
            "\n\n---\n\n".join(
                f"[{c.chapter} / {c.section}]\n{c.text}" for c in chunks
            )
            if chunks
            else "No relevant content found."
        )
        sources = [
            {
                "chapter": c.chapter,
                "section": c.section,
                "slug": c.slug,
                "relevance_score": c.relevance_score,
            }
            for c in sorted(chunks, key=lambda x: x.relevance_score, reverse=True)
        ]

    system_prompt = (
        "You are a teaching assistant for the Physical AI & Humanoid Robotics textbook.\n"
        "Answer ONLY based on the provided context. If the context lacks enough information, say: "
        '"I can only answer questions based on the Physical AI & Humanoid Robotics textbook content."\n'
        "Do not use outside knowledge. Be concise and accurate.\n\n"
        f"Context:\n{context}"
    )

    history = await postgres.get_session_history(pool, sid) if pool else []
    result = await generator.generate(system_prompt, query, history)

    if pool:
        await postgres.save_session_messages(pool, sid, query, result.answer)

    return {
        "answer": result.answer,
        "sources": sources,
        "session_id": sid,
        "tokens_used": result.tokens_used,
    }
