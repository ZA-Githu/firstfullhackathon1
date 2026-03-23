from __future__ import annotations

import re
import uuid

import asyncpg
from qdrant_client import QdrantClient

from app.config import get_settings
from app.db import postgres
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse, SourceReference
from app.services import embedder, generator, retriever

_SYSTEM = (
    "You are a concise teaching assistant for the Physical AI & Humanoid Robotics textbook.\n"
    "Answer ONLY based on the provided context below.\n"
    "Keep answers SHORT — 2 to 4 sentences maximum. No bullet lists unless specifically asked.\n"
    "If the context does not contain enough information, say so in one sentence.\n"
    "Do not use outside knowledge.\n\n"
    "Context:\n{context}"
)

_GREETING_PATTERNS = re.compile(
    r"^\s*(hi|hello|hey|howdy|greetings|good\s+(morning|afternoon|evening|day)|"
    r"what'?s up|sup|hiya|yo)\s*[!?.]*\s*$",
    re.IGNORECASE,
)

_IDENTITY_PATTERNS = re.compile(
    r"^\s*(who are you|what are you|tell me about yourself|what can you do|"
    r"what do you do|how can you help|help me|what is this|introduce yourself)\s*[!?.]*\s*$",
    re.IGNORECASE,
)

_GREETING_RESPONSE = (
    "Hello! 👋 I'm the AI assistant for the **Physical AI & Humanoid Robotics** textbook. "
    "I can help you with questions about:\n\n"
    "- 🤖 ROS 2 & Navigation (Nav2)\n"
    "- 🌐 NVIDIA Isaac Sim, Isaac ROS, Isaac Lab\n"
    "- ⚡ VLA Models (RT-2, OpenVLA, π0)\n"
    "- 📋 Gazebo & Unity Robotics simulation\n"
    "- 🚀 Physical AI hardware (Jetson Orin, Unitree G1/H1)\n\n"
    "Ask me anything from the textbook!"
)

_IDENTITY_RESPONSE = (
    "I'm the **Physical AI & Humanoid Robotics Textbook Assistant** — a RAG-powered chatbot "
    "built on top of the course material. 🤖\n\n"
    "I can answer questions about ROS 2, NVIDIA Isaac, VLA models, humanoid robots, "
    "simulation environments, and AI-Native development as covered in this textbook.\n\n"
    "What would you like to learn about?"
)


async def run_rag(
    request: ChatRequest,
    pool: asyncpg.Pool,
    qdrant_client: QdrantClient,
) -> ChatResponse:
    settings = get_settings()
    session_id = str(request.session_id) if request.session_id else str(uuid.uuid4())

    if request.language == "ur":
        return ChatResponse(
            answer="Urdu translation coming soon.",
            sources=[],
            session_id=uuid.UUID(session_id),
            tokens_used=0,
        )

    # Handle greetings and identity questions without hitting the vector store
    if _GREETING_PATTERNS.match(request.query):
        return ChatResponse(
            answer=_GREETING_RESPONSE,
            sources=[],
            session_id=uuid.UUID(session_id),
            tokens_used=0,
        )

    if _IDENTITY_PATTERNS.match(request.query):
        return ChatResponse(
            answer=_IDENTITY_RESPONSE,
            sources=[],
            session_id=uuid.UUID(session_id),
            tokens_used=0,
        )

    vectors = await embedder.embed_texts([request.query])
    query_vector = vectors[0]

    chunks = await retriever.retrieve(
        query_vector, request.top_k, settings.qdrant_collection, qdrant_client
    )

    if chunks:
        context = "\n\n---\n\n".join(
            f"[{c.chapter} / {c.section}]\n{c.text}" for c in chunks
        )
    else:
        context = "No relevant content found in the textbook."

    system_prompt = _SYSTEM.format(context=context)
    history = await postgres.get_session_history(pool, session_id) if pool else []
    result = await generator.generate(system_prompt, request.query, history)

    if pool:
        await postgres.save_session_messages(
            pool, session_id, request.query, result.answer
        )

    # Filter out index/intro chunks from displayed sources
    meaningful_chunks = [
        c for c in chunks
        if c.section and c.section.lower() not in ("index", "intro", "", "introduction")
        and c.slug and c.slug.lower() != "index"
    ]
    display_chunks = meaningful_chunks if meaningful_chunks else chunks

    sources = sorted(
        [
            SourceReference(
                chapter=c.chapter,
                section=c.section,
                slug=c.slug,
                relevance_score=c.relevance_score,
            )
            for c in display_chunks
        ],
        key=lambda s: s.relevance_score,
        reverse=True,
    )

    return ChatResponse(
        answer=result.answer,
        sources=sources,
        session_id=uuid.UUID(session_id),
        tokens_used=result.tokens_used,
    )
