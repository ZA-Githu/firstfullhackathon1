from __future__ import annotations

import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID


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


def test_selected_pipeline_does_not_import_retriever():
    import inspect
    import app.services.selected_pipeline as sp

    source = inspect.getsource(sp)
    assert "retriever" not in source, (
        "selected_pipeline must NOT import or reference retriever"
    )


@pytest.mark.asyncio
async def test_retriever_never_called():
    from app.models.requests import ChatSelectedRequest

    mock_pool = MagicMock()
    gen_result = MagicMock()
    gen_result.answer = "RealSense cameras are supported."
    gen_result.tokens_used = 30

    with patch(
        "app.services.selected_pipeline.generator.generate",
        new_callable=AsyncMock,
        return_value=gen_result,
    ):
        with patch(
            "app.services.selected_pipeline.postgres.get_session_history",
            new_callable=AsyncMock,
            return_value=[],
        ):
            with patch(
                "app.services.selected_pipeline.postgres.save_session_messages",
                new_callable=AsyncMock,
            ):
                with patch(
                    "app.services.retriever.retrieve"
                ) as mock_retrieve:
                    from app.services.selected_pipeline import run_selected

                    req = ChatSelectedRequest(
                        query="What sensors does it support?",
                        selected_text=(
                            "The Jetson Orin Nano supports Intel RealSense "
                            "depth cameras and USB cameras for vision tasks."
                        ),
                    )
                    result = await run_selected(req, mock_pool)

    mock_retrieve.assert_not_called()
    assert len(result.answer) > 0


@pytest.mark.asyncio
async def test_new_session_id_generated():
    from app.models.requests import ChatSelectedRequest

    mock_pool = MagicMock()
    gen_result = MagicMock()
    gen_result.answer = "answer"
    gen_result.tokens_used = 10

    with patch(
        "app.services.selected_pipeline.generator.generate",
        new_callable=AsyncMock,
        return_value=gen_result,
    ):
        with patch(
            "app.services.selected_pipeline.postgres.get_session_history",
            new_callable=AsyncMock,
            return_value=[],
        ):
            with patch(
                "app.services.selected_pipeline.postgres.save_session_messages",
                new_callable=AsyncMock,
            ):
                from app.services.selected_pipeline import run_selected

                req = ChatSelectedRequest(
                    query="What is this?",
                    selected_text=(
                        "This is a long enough selected text for the validator."
                    ),
                )
                result = await run_selected(req, mock_pool)

    assert isinstance(result.session_id, UUID)
