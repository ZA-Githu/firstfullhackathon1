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


SAMPLE = {
    "text": "## ROS 2 Nodes\n\nROS 2 nodes are independent processes. " * 30,
    "metadata": {"chapter": "Week 3", "section": "Nodes", "slug": "week-3/nodes"},
}


def _build_client(hash_exists: bool = False):
    pool_mock = MagicMock()
    pool_mock.close = AsyncMock()
    qdrant_mock = MagicMock()
    qdrant_mock.get_collections.return_value = MagicMock(collections=[])
    qdrant_mock.upsert = MagicMock()

    with patch(
        "app.main.create_pool", new_callable=AsyncMock, return_value=pool_mock
    ), patch("app.main.init_schema", new_callable=AsyncMock), patch(
        "app.main.purge_old_logs", new_callable=AsyncMock
    ), patch(
        "app.main.get_qdrant_client", return_value=qdrant_mock
    ), patch(
        "app.main.ensure_collection"
    ), patch(
        "app.services.embedder.embed_texts",
        new_callable=AsyncMock,
        return_value=[[0.1] * 1536] * 20,
    ), patch(
        "app.db.postgres.chunk_hash_exists",
        new_callable=AsyncMock,
        return_value=hash_exists,
    ), patch(
        "app.db.postgres.record_chunk_hash", new_callable=AsyncMock
    ), patch(
        "app.db.postgres.clear_chunk_hashes", new_callable=AsyncMock
    ):
        from app.main import app

        return TestClient(app, raise_server_exceptions=False)


def test_ingest_valid_payload():
    client = _build_client()
    resp = client.post(
        "/api/ingest",
        json={"sources": [SAMPLE]},
        headers={"X-API-Key": "test-ingest-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["chunks_stored"] >= 0


def test_ingest_no_api_key_returns_401():
    client = _build_client()
    resp = client.post("/api/ingest", json={"sources": [SAMPLE]})
    assert resp.status_code == 401


def test_ingest_wrong_api_key_returns_401():
    client = _build_client()
    resp = client.post(
        "/api/ingest",
        json={"sources": [SAMPLE]},
        headers={"X-API-Key": "wrong-key"},
    )
    assert resp.status_code == 401


def test_ingest_no_sources_returns_422():
    client = _build_client()
    resp = client.post(
        "/api/ingest",
        json={},
        headers={"X-API-Key": "test-ingest-key"},
    )
    assert resp.status_code == 422


def test_ingest_duplicates_skipped():
    client = _build_client(hash_exists=True)
    resp = client.post(
        "/api/ingest",
        json={"sources": [SAMPLE]},
        headers={"X-API-Key": "test-ingest-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["chunks_stored"] == 0
    assert data["skipped_duplicates"] > 0
