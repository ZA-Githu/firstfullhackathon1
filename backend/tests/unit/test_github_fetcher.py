from __future__ import annotations

import pytest
import respx
import httpx
from app.services.github_fetcher import _parse_repo, fetch_docs


def test_parse_repo_valid():
    owner, repo = _parse_repo("https://github.com/panaversity/physical-ai-book")
    assert owner == "panaversity"
    assert repo == "physical-ai-book"


def test_parse_repo_invalid():
    with pytest.raises(ValueError):
        _parse_repo("https://notgithub.com/owner/repo")


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
async def test_fetch_docs_filters_md_files():
    tree_response = {
        "tree": [
            {"type": "blob", "path": "docs/week-1/intro.md"},
            {"type": "blob", "path": "docs/week-2/ros2.md"},
            {"type": "blob", "path": "src/index.ts"},
            {"type": "blob", "path": "other/file.md"},
        ]
    }

    with respx.mock:
        respx.get(
            "https://api.github.com/repos/owner/repo/git/trees/HEAD?recursive=1"
        ).mock(return_value=httpx.Response(200, json=tree_response))
        respx.get(
            "https://raw.githubusercontent.com/owner/repo/HEAD/docs/week-1/intro.md"
        ).mock(return_value=httpx.Response(200, text="# Week 1"))
        respx.get(
            "https://raw.githubusercontent.com/owner/repo/HEAD/docs/week-2/ros2.md"
        ).mock(return_value=httpx.Response(200, text="# ROS 2"))

        result = await fetch_docs("https://github.com/owner/repo", "docs")

    assert len(result) == 2
    slugs = [f.metadata.slug for f in result]
    assert "week-1/intro" in slugs
    assert "week-2/ros2" in slugs


@pytest.mark.asyncio
async def test_fetch_docs_404_raises():
    with respx.mock:
        respx.get(
            "https://api.github.com/repos/owner/missing/git/trees/HEAD?recursive=1"
        ).mock(return_value=httpx.Response(404, json={"message": "Not Found"}))

        with pytest.raises(ValueError, match="Repository not found"):
            await fetch_docs("https://github.com/owner/missing", "docs")
