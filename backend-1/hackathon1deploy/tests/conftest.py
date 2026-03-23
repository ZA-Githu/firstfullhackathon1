from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_pool():
    pool = MagicMock()
    pool.acquire = MagicMock()
    pool.close = AsyncMock()
    return pool


@pytest.fixture
def mock_qdrant():
    return MagicMock()
