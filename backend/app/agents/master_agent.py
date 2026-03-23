"""TextbookMasterAgent — orchestrates all textbook intelligence via Claude tool-use.

The agent receives a high-level task, decides which skill(s) to call, executes them,
and returns a structured result. It uses the Claude API agentic loop (tool_use).

Callable from FastAPI routes or programmatically:

    result = await TextbookMasterAgent(pool=pool, qdrant_client=qdrant).run(
        task="generate chapter",
        module="Module 2: ROS 2 Fundamentals",
    )

    result = await TextbookMasterAgent(pool=pool, qdrant_client=qdrant).run(
        task="answer query",
        query="What is Nav2?",
        mode="general",
    )
"""
from __future__ import annotations

import json
import logging
from typing import Any

import anthropic
from qdrant_client import QdrantClient

from app.agents.skills.chapter_generation_skill import run_chapter_generation_skill
from app.agents.skills.ingestion_skill import run_ingestion_skill
from app.agents.skills.personalization_skill import run_personalization_skill
from app.agents.skills.rag_query_skill import run_rag_query_skill
from app.agents.skills.translation_skill import run_translation_skill
from app.config import get_settings

logger = logging.getLogger(__name__)

_AGENT_SYSTEM = """\
You are TextbookMasterAgent — the intelligence layer of the Physical AI & \
Humanoid Robotics interactive textbook.

Your capabilities:
1. **rag_query** — Answer user questions using the textbook's vector store (RAG).
   Use mode="general" for free-form questions; mode="selected" when the user \
has highlighted specific text.
2. **generate_chapter** — Write or expand a Markdown chapter/section for a given module.
3. **personalize_content** — Adapt existing Markdown content to a user's background \
and experience level.
4. **translate_to_urdu** — Translate any Markdown content to Urdu while preserving \
structure and technical terms.
5. **ingest_content** — Chunk and embed new Markdown content into the vector store.

Rules:
- Only use knowledge from this textbook. Never answer general AI questions unrelated \
to Physical AI, robotics, or the course modules.
- Always call the most appropriate skill. Do not attempt to answer from memory alone.
- If the task is ambiguous, infer the most likely intent from context.
- Return concise, structured results.
"""

# ── Tool definitions ────────────────────────────────────────────────────────

_TOOLS: list[dict] = [
    {
        "name": "rag_query",
        "description": (
            "Answer a user question by searching the textbook vector store. "
            "Use mode='selected' if the user has highlighted specific text."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The user question."},
                "mode": {
                    "type": "string",
                    "enum": ["general", "selected"],
                    "description": "general = vector retrieval; selected = grounded in selected_text only.",
                },
                "selected_text": {
                    "type": "string",
                    "description": "Required when mode='selected'. The highlighted passage.",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of chunks to retrieve (general mode). Default 5.",
                },
                "session_id": {
                    "type": "string",
                    "description": "Optional session UUID for conversation history.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "generate_chapter",
        "description": (
            "Generate or expand a full Markdown chapter for a given module/section "
            "of the Physical AI & Humanoid Robotics textbook."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "description": "Module name, e.g. 'Module 2: ROS 2 Fundamentals'.",
                },
                "section": {
                    "type": "string",
                    "description": "Optional specific section within the module.",
                },
                "expand_existing": {
                    "type": "string",
                    "description": "Existing Markdown draft to expand rather than generate fresh.",
                },
                "word_target": {
                    "type": "integer",
                    "description": "Approximate word count. Default 800.",
                },
            },
            "required": ["module"],
        },
    },
    {
        "name": "personalize_content",
        "description": (
            "Adapt a Markdown chapter excerpt to a specific learner's background "
            "and experience level. Preserves all technical accuracy."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Original Markdown content to personalise.",
                },
                "user_background": {
                    "type": "string",
                    "description": "Short description of the user's background, e.g. '3 years Python, no robotics'.",
                },
                "experience_level": {
                    "type": "string",
                    "enum": ["beginner", "intermediate", "advanced"],
                    "description": "Learner's experience level.",
                },
            },
            "required": ["content", "user_background"],
        },
    },
    {
        "name": "translate_to_urdu",
        "description": (
            "Translate a Markdown chapter or section to Urdu. "
            "Preserves code blocks, Markdown structure, and technical English terms."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Markdown content to translate.",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "ingest_content",
        "description": (
            "Chunk and embed new Markdown content into the Qdrant vector store "
            "with deduplication. Use when adding new textbook chapters."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sources": {
                    "type": "array",
                    "description": (
                        "List of content sources. Each item: "
                        "{text: str, metadata: {chapter, section, slug, source_url}}"
                    ),
                    "items": {"type": "object"},
                },
                "clear_collection": {
                    "type": "boolean",
                    "description": "If true, wipe the collection before ingesting.",
                },
            },
            "required": ["sources"],
        },
    },
]


class TextbookMasterAgent:
    """Orchestrates textbook intelligence via Claude tool-use.

    Usage:
        agent = TextbookMasterAgent(pool=pool, qdrant_client=qdrant_client)
        result = await agent.run(task="answer query", query="What is Nav2?")
        result = await agent.run(task="generate chapter", module="Module 1")
        result = await agent.run(
            task="personalize",
            content="...",
            user_background="Python developer, no robotics",
            experience_level="beginner",
        )
    """

    def __init__(self, pool=None, qdrant_client: QdrantClient | None = None) -> None:
        settings = get_settings()
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._pool = pool
        self._qdrant = qdrant_client

    async def run(self, task: str, **kwargs: Any) -> dict:
        """Run the agent for a given task.

        Args:
            task: High-level task description. Examples:
                  "answer query", "generate chapter", "personalize", "translate", "ingest".
            **kwargs: Task-specific parameters forwarded to the appropriate skill.

        Returns:
            dict with the skill's result plus metadata.
        """
        user_message = self._build_user_message(task, kwargs)
        messages: list[dict] = [{"role": "user", "content": user_message}]

        max_iterations = 5
        for _ in range(max_iterations):
            response = await self._client.messages.create(
                model="claude-opus-4-6",
                max_tokens=8192,
                thinking={"type": "adaptive"},
                system=_AGENT_SYSTEM,
                tools=_TOOLS,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                # Extract final text answer
                text = next(
                    (b.text for b in response.content if b.type == "text"), ""
                )
                return {"task": task, "result": text, "skill_calls": []}

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []

                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    skill_result = await self._dispatch_skill(
                        block.name, block.input
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(skill_result),
                    })

                messages.append({"role": "user", "content": tool_results})
                continue

            # pause_turn or unexpected — break
            break

        # Return whatever the last assistant turn produced
        last_text = ""
        last_skill_result: dict = {}
        for msg in reversed(messages):
            if msg["role"] == "user" and isinstance(msg["content"], list):
                for item in msg["content"]:
                    if isinstance(item, dict) and item.get("type") == "tool_result":
                        try:
                            last_skill_result = json.loads(item["content"])
                        except (json.JSONDecodeError, KeyError):
                            pass
                        break
                break

        return {
            "task": task,
            "result": last_skill_result or last_text,
            "direct": True,  # agent returned skill output directly
        }

    # ── private helpers ───────────────────────────────────────────────────

    @staticmethod
    def _build_user_message(task: str, kwargs: dict) -> str:
        """Convert task + kwargs into a natural-language prompt."""
        task_lower = task.lower()

        if "query" in task_lower or "answer" in task_lower or "chat" in task_lower:
            query = kwargs.get("query", "")
            mode = kwargs.get("mode", "general")
            selected = kwargs.get("selected_text", "")
            msg = f"Answer this question from the textbook: {query}"
            if mode == "selected" and selected:
                msg += f"\n\nUser has selected this text:\n{selected}"
            return msg

        if "generate" in task_lower or "chapter" in task_lower or "write" in task_lower:
            module = kwargs.get("module", "")
            section = kwargs.get("section", "")
            expand = kwargs.get("expand_existing", "")
            msg = f"Generate a textbook chapter for: {module}"
            if section:
                msg += f", section: {section}"
            if expand:
                msg += f"\n\nExpand this existing draft:\n{expand[:500]}..."
            return msg

        if "personal" in task_lower or "adapt" in task_lower:
            content = kwargs.get("content", "")
            bg = kwargs.get("user_background", "")
            level = kwargs.get("experience_level", "intermediate")
            return (
                f"Personalise this content for a {level} learner "
                f"with background: {bg}\n\nContent:\n{content[:1000]}..."
            )

        if "translat" in task_lower or "urdu" in task_lower:
            content = kwargs.get("content", "")
            return f"Translate this textbook content to Urdu:\n\n{content[:2000]}..."

        if "ingest" in task_lower or "embed" in task_lower:
            sources = kwargs.get("sources", [])
            return f"Ingest {len(sources)} source(s) into the textbook vector store."

        # Generic fallback
        extra = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        return f"Task: {task}. Parameters: {extra}"

    async def _dispatch_skill(self, skill_name: str, inputs: dict) -> dict:
        """Call the appropriate skill function."""
        try:
            if skill_name == "rag_query":
                return await run_rag_query_skill(
                    query=inputs["query"],
                    mode=inputs.get("mode", "general"),
                    selected_text=inputs.get("selected_text"),
                    top_k=inputs.get("top_k", 5),
                    session_id=inputs.get("session_id"),
                    pool=self._pool,
                    qdrant_client=self._qdrant,
                )

            if skill_name == "generate_chapter":
                return await run_chapter_generation_skill(
                    module=inputs["module"],
                    section=inputs.get("section"),
                    expand_existing=inputs.get("expand_existing"),
                    word_target=inputs.get("word_target", 800),
                )

            if skill_name == "personalize_content":
                return await run_personalization_skill(
                    content=inputs["content"],
                    user_background=inputs["user_background"],
                    experience_level=inputs.get("experience_level", "intermediate"),
                )

            if skill_name == "translate_to_urdu":
                return await run_translation_skill(
                    content=inputs["content"],
                    target_language="ur",
                )

            if skill_name == "ingest_content":
                return await run_ingestion_skill(
                    sources=inputs["sources"],
                    pool=self._pool,
                    qdrant_client=self._qdrant,
                    clear_collection=inputs.get("clear_collection", False),
                )

        except Exception as exc:
            logger.exception("Skill '%s' failed: %s", skill_name, exc)
            return {"error": str(exc), "skill": skill_name}

        return {"error": f"Unknown skill: {skill_name}"}
