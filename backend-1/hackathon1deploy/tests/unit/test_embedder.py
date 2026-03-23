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


@pytest.mark.asyncio
async def test_embed_returns_vectors():
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]

    with patch("app.services.embedder.AsyncOpenAI") as mock_class:
        mock_c = MagicMock()
        mock_c.embeddings.create = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_c

        from app.services.embedder import embed_texts

        result = await embed_texts(["hello world"])

    assert len(result) == 1
    assert len(result[0]) == 1536


@pytest.mark.asyncio
async def test_embed_empty_returns_empty():
    from app.services.embedder import embed_texts

    result = await embed_texts([])
    assert result == []


@pytest.mark.asyncio
async def test_embed_batches_150_texts():
    call_count = 0

    async def mock_create(**kwargs):
        nonlocal call_count
        call_count += 1
        n = len(kwargs["input"])
        r = MagicMock()
        r.data = [MagicMock(embedding=[0.1] * 1536) for _ in range(n)]
        return r

    with patch("app.services.embedder.AsyncOpenAI") as mock_class:
        mock_c = MagicMock()
        mock_c.embeddings.create = mock_create
        mock_class.return_value = mock_c

        from app.services import embedder

        result = await embedder.embed_texts(["text"] * 150)

    assert len(result) == 150
    assert call_count == 2


@pytest.mark.asyncio
async def test_embed_retries_on_rate_limit():
    from openai import RateLimitError

    call_count = 0

    async def flaky(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise RateLimitError(
                "rate limited",
                response=MagicMock(status_code=429),
                body={},
            )
        r = MagicMock()
        r.data = [MagicMock(embedding=[0.1] * 1536)]
        return r

    with patch("app.services.embedder.AsyncOpenAI") as mock_class:
        with patch("app.services.embedder.asyncio.sleep", new_callable=AsyncMock):
            mock_c = MagicMock()
            mock_c.embeddings.create = flaky
            mock_class.return_value = mock_c

            from app.services import embedder

            result = await embedder.embed_texts(["text"])

    assert call_count == 3
    assert len(result[0]) == 1536
