from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


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


def _build_client(qdrant_ok: bool = True, db_ok: bool = True):
    from unittest.mock import patch, AsyncMock, MagicMock

    pool_mock = MagicMock()
    pool_mock.close = AsyncMock()
    conn_mock = AsyncMock()
    if not db_ok:
        conn_mock.execute.side_effect = Exception("db down")
    pool_mock.acquire.return_value.__aenter__ = AsyncMock(return_value=conn_mock)
    pool_mock.acquire.return_value.__aexit__ = AsyncMock(return_value=False)

    qdrant_mock = MagicMock()
    if not qdrant_ok:
        qdrant_mock.get_collections.side_effect = Exception("qdrant down")
    else:
        qdrant_mock.get_collections.return_value = MagicMock(collections=[])

    with patch(
        "app.main.create_pool", new_callable=AsyncMock, return_value=pool_mock
    ), patch("app.main.init_schema", new_callable=AsyncMock), patch(
        "app.main.purge_old_logs", new_callable=AsyncMock
    ), patch(
        "app.main.get_qdrant_client", return_value=qdrant_mock
    ), patch(
        "app.main.ensure_collection"
    ):
        from app.main import app
        from fastapi.testclient import TestClient

        return TestClient(app, raise_server_exceptions=False)


def test_health_all_ok():
    client = _build_client()
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["qdrant"] == "ok"
    assert data["db"] == "ok"


def test_health_qdrant_down():
    client = _build_client(qdrant_ok=False)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "degraded"
    assert data["qdrant"] == "error"


def test_health_no_auth_required():
    client = _build_client()
    resp = client.get("/api/health")
    assert resp.status_code == 200
