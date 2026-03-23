from __future__ import annotations

import asyncio
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException


def test_retrieve_returns_chunks():
    mock_hit = MagicMock()
    mock_hit.payload = {
        "text": "ROS content",
        "chapter": "Week 3",
        "section": "Nodes",
        "slug": "week-3/nodes",
    }
    mock_hit.score = 0.92

    mock_client = MagicMock()
    mock_client.search.return_value = [mock_hit]

    from app.services.retriever import retrieve

    result = asyncio.get_event_loop().run_until_complete(
        retrieve([0.1] * 1536, 3, "ai-native-book", mock_client)
    )
    assert len(result) == 1
    assert result[0].chapter == "Week 3"
    assert result[0].relevance_score == 0.92


def test_retrieve_empty_results():
    mock_client = MagicMock()
    mock_client.search.return_value = []

    from app.services.retriever import retrieve

    result = asyncio.get_event_loop().run_until_complete(
        retrieve([0.1] * 1536, 5, "ai-native-book", mock_client)
    )
    assert result == []


def test_retrieve_qdrant_error_raises_503():
    mock_client = MagicMock()
    mock_client.search.side_effect = Exception("connection refused")

    from app.services.retriever import retrieve

    with pytest.raises(HTTPException) as exc_info:
        asyncio.get_event_loop().run_until_complete(
            retrieve([0.1] * 1536, 5, "ai-native-book", mock_client)
        )
    assert exc_info.value.status_code == 503
