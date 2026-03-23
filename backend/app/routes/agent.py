"""POST /api/agent — TextbookMasterAgent HTTP endpoint.

Accepts a task and task-specific parameters; runs the master agent;
returns the skill result.

Example requests:

    # RAG query (general)
    POST /api/agent
    {"task": "answer query", "query": "What is Nav2?"}

    # RAG query (selected text)
    POST /api/agent
    {"task": "answer query", "query": "Explain this", "mode": "selected",
     "selected_text": "Nav2 is the navigation stack for ROS 2..."}

    # Chapter generation
    POST /api/agent
    {"task": "generate chapter", "module": "Module 2: ROS 2 Fundamentals",
     "section": "DDS Middleware", "word_target": 1000}

    # Personalisation
    POST /api/agent
    {"task": "personalize", "content": "...", "user_background": "5y Python, no robotics",
     "experience_level": "beginner"}

    # Translation
    POST /api/agent
    {"task": "translate", "content": "## Introduction\\nROS 2 is ..."}

    # Ingestion
    POST /api/agent
    {"task": "ingest", "sources": [{"text": "...", "metadata": {...}}]}
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.agents.master_agent import TextbookMasterAgent
from app.dependencies import get_db_pool, get_qdrant, limiter

router = APIRouter(tags=["agent"])


class AgentRequest(BaseModel):
    task: str
    # RAG
    query: str | None = None
    mode: str | None = "general"
    selected_text: str | None = None
    top_k: int = 5
    session_id: str | None = None
    # Chapter generation
    module: str | None = None
    section: str | None = None
    expand_existing: str | None = None
    word_target: int = 800
    # Personalisation
    content: str | None = None
    user_background: str | None = None
    experience_level: str = "intermediate"
    # Ingestion
    sources: list[dict[str, Any]] | None = None
    clear_collection: bool = False


class AgentResponse(BaseModel):
    task: str
    result: Any
    direct: bool = False


@router.post("/agent", response_model=AgentResponse)
@limiter.limit("5/minute")
async def run_agent(
    request: Request,
    body: AgentRequest,
    pool=Depends(get_db_pool),
    qdrant=Depends(get_qdrant),
) -> AgentResponse:
    """Run TextbookMasterAgent for any textbook intelligence task."""
    # Build kwargs from request body, skipping None/default-only fields
    kwargs: dict[str, Any] = {}

    if body.query:
        kwargs["query"] = body.query
    if body.mode:
        kwargs["mode"] = body.mode
    if body.selected_text:
        kwargs["selected_text"] = body.selected_text
    if body.top_k != 5:
        kwargs["top_k"] = body.top_k
    if body.session_id:
        kwargs["session_id"] = body.session_id
    if body.module:
        kwargs["module"] = body.module
    if body.section:
        kwargs["section"] = body.section
    if body.expand_existing:
        kwargs["expand_existing"] = body.expand_existing
    if body.word_target != 800:
        kwargs["word_target"] = body.word_target
    if body.content:
        kwargs["content"] = body.content
    if body.user_background:
        kwargs["user_background"] = body.user_background
    if body.experience_level != "intermediate":
        kwargs["experience_level"] = body.experience_level
    if body.sources is not None:
        kwargs["sources"] = body.sources
    if body.clear_collection:
        kwargs["clear_collection"] = body.clear_collection

    try:
        agent = TextbookMasterAgent(pool=pool, qdrant_client=qdrant)
        result = await agent.run(task=body.task, **kwargs)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AgentResponse(
        task=result["task"],
        result=result["result"],
        direct=result.get("direct", False),
    )
