from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "test")
    monkeypatch.setenv("DATABASE_URL", "postgresql://t:t@localhost/t")
    monkeypatch.setenv("INGEST_API_KEY", "test-ingest-key")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000")
    from app.config import get_settings

    get_settings.cache_clear()


def _build_client():
    from app.services.retriever import RetrievedChunk
    from app.services.generator import GeneratorResult

    pool_mock = MagicMock()
    pool_mock.close = AsyncMock()
    qdrant_mock = MagicMock()
    qdrant_mock.get_collections.return_value = MagicMock(collections=[])

    with patch(
        "app.main.create_pool", new_callable=AsyncMock, return_value=pool_mock
    ), patch("app.main.init_schema", new_callable=AsyncMock), patch(
        "app.main.purge_old_logs", new_callable=AsyncMock
    ), patch(
        "app.main.get_qdrant_client", return_value=qdrant_mock
    ), patch(
        "app.main.ensure_collection"
    ), patch(
        "app.services.rag_pipeline.embedder.embed_texts",
        new_callable=AsyncMock,
        return_value=[[0.1] * 1536],
    ), patch(
        "app.services.rag_pipeline.retriever.retrieve",
        new_callable=AsyncMock,
        return_value=[
            RetrievedChunk(
                text="ROS 2 nodes are independent processes.",
                chapter="Week 3",
                section="Nodes",
                slug="week-3/nodes",
                relevance_score=0.95,
            )
        ],
    ), patch(
        "app.services.rag_pipeline.generator.generate",
        new_callable=AsyncMock,
        return_value=GeneratorResult(
            answer="ROS 2 nodes communicate via topics.", tokens_used=40
        ),
    ), patch(
        "app.services.rag_pipeline.postgres.get_session_history",
        new_callable=AsyncMock,
        return_value=[],
    ), patch(
        "app.services.rag_pipeline.postgres.save_session_messages",
        new_callable=AsyncMock,
    ), patch(
        "app.db.postgres.log_request", new_callable=AsyncMock
    ):
        from app.main import app

        return TestClient(app, raise_server_exceptions=False)


def test_chat_returns_answer_with_sources():
    client = _build_client()
    resp = client.post("/api/chat", json={"query": "Explain ROS 2 nodes"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "sources" in data
    assert "session_id" in data


def test_chat_query_too_long_returns_422():
    client = _build_client()
    resp = client.post("/api/chat", json={"query": "x" * 1001})
    assert resp.status_code == 422


def test_chat_empty_query_returns_422():
    client = _build_client()
    resp = client.post("/api/chat", json={"query": ""})
    assert resp.status_code == 422


def test_chat_html_in_query_returns_422():
    client = _build_client()
    resp = client.post(
        "/api/chat",
        json={"query": "<script>alert(1)</script> what is ROS?"},
    )
    assert resp.status_code == 422
