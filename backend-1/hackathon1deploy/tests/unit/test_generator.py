from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "test")
    monkeypatch.setenv("DATABASE_URL", "postgresql://t:t@localhost/t")
    monkeypatch.setenv("INGEST_API_KEY", "test")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000")
    from app.config import get_settings

    get_settings.cache_clear()


def _mock_response(answer: str, tokens: int = 50):
    resp = MagicMock()
    resp.choices = [MagicMock()]
    resp.choices[0].message.content = answer
    resp.usage.total_tokens = tokens
    return resp


@pytest.mark.asyncio
async def test_generate_returns_result():
    with patch("app.services.generator.AsyncOpenAI") as mock_class:
        mock_c = MagicMock()
        mock_c.chat.completions.create = AsyncMock(
            return_value=_mock_response("ROS 2 answer")
        )
        mock_class.return_value = mock_c

        from app.services.generator import generate

        result = await generate("system", "what is ROS 2?", [])

    assert result.answer == "ROS 2 answer"
    assert result.tokens_used == 50


@pytest.mark.asyncio
async def test_history_truncated_to_10():
    history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
    captured: dict = {}

    async def capture(**kwargs):
        captured["messages"] = kwargs["messages"]
        return _mock_response("ok")

    with patch("app.services.generator.AsyncOpenAI") as mock_class:
        mock_c = MagicMock()
        mock_c.chat.completions.create = capture
        mock_class.return_value = mock_c

        from app.services.generator import generate

        await generate("system", "query", history)

    assert len(captured["messages"]) == 12  # system + 10 history + user


@pytest.mark.asyncio
async def test_empty_history():
    captured: dict = {}

    async def capture(**kwargs):
        captured["messages"] = kwargs["messages"]
        return _mock_response("ok")

    with patch("app.services.generator.AsyncOpenAI") as mock_class:
        mock_c = MagicMock()
        mock_c.chat.completions.create = capture
        mock_class.return_value = mock_c

        from app.services.generator import generate

        await generate("system", "query", [])

    assert len(captured["messages"]) == 2  # system + user
