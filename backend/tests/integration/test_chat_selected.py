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


def _build_client(answer: str = "Answer from selection."):
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
        "app.services.selected_pipeline.generator.generate",
        new_callable=AsyncMock,
        return_value=GeneratorResult(answer=answer, tokens_used=20),
    ), patch(
        "app.services.selected_pipeline.postgres.get_session_history",
        new_callable=AsyncMock,
        return_value=[],
    ), patch(
        "app.services.selected_pipeline.postgres.save_session_messages",
        new_callable=AsyncMock,
    ), patch(
        "app.db.postgres.log_request", new_callable=AsyncMock
    ), patch(
        "app.services.retriever.retrieve", new_callable=AsyncMock
    ) as mock_retrieve:
        from app.main import app

        client = TestClient(app, raise_server_exceptions=False)
        return client, mock_retrieve


def test_chat_selected_returns_answer():
    client, mock_retrieve = _build_client(answer="RealSense cameras are supported.")
    resp = client.post(
        "/api/chat-selected",
        json={
            "query": "What sensors does it support?",
            "selected_text": (
                "The Jetson Orin Nano supports Intel RealSense depth cameras "
                "and USB cameras for vision tasks."
            ),
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "session_id" in data
    assert "sources" not in data


def test_chat_selected_retriever_never_called():
    client, mock_retrieve = _build_client()
    client.post(
        "/api/chat-selected",
        json={
            "query": "What is this about?",
            "selected_text": "This paragraph explains the importance of ROS 2 middleware.",
        },
    )
    mock_retrieve.assert_not_called()


def test_chat_selected_text_too_long_returns_422():
    client, _ = _build_client()
    resp = client.post(
        "/api/chat-selected",
        json={"query": "What is this?", "selected_text": "x" * 5001},
    )
    assert resp.status_code == 422


def test_chat_selected_html_returns_422():
    client, _ = _build_client()
    resp = client.post(
        "/api/chat-selected",
        json={
            "query": "What is this?",
            "selected_text": "<script>alert(1)</script> long enough text here for the validator",
        },
    )
    assert resp.status_code == 422


def test_chat_selected_query_too_long_returns_422():
    client, _ = _build_client()
    resp = client.post(
        "/api/chat-selected",
        json={
            "query": "q" * 1001,
            "selected_text": "Valid selected text long enough for the validator to pass here.",
        },
    )
    assert resp.status_code == 422
