from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

import httpx

from app.config import get_settings
from app.models.requests import ChunkMetadata


@dataclass
class FetchedFile:
    content: str
    path: str
    metadata: ChunkMetadata


def _parse_repo(url: str) -> tuple[str, str]:
    match = re.match(
        r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url
    )
    if not match:
        raise ValueError(f"Invalid GitHub repo URL: {url}")
    return match.group(1), match.group(2)


def _path_to_metadata(path: str) -> ChunkMetadata:
    p = PurePosixPath(path)
    parts = list(p.parts[1:])  # strip leading dir (e.g. 'docs')
    parts[-1] = p.stem  # remove extension
    slug = "/".join(parts)
    chapter = parts[0] if parts else "unknown"
    section = parts[-1] if len(parts) > 1 else chapter
    return ChunkMetadata(chapter=chapter, section=section, slug=slug)


async def fetch_docs(
    repo_url: str,
    docs_path: str = "docs",
    token: str | None = None,
) -> list[FetchedFile]:
    owner, repo = _parse_repo(repo_url)
    settings = get_settings()
    auth_token = token or settings.github_token or None

    headers: dict[str, str] = {"Accept": "application/vnd.github+json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    async with httpx.AsyncClient(headers=headers, timeout=30) as client:
        tree_url = (
            f"https://api.github.com/repos/{owner}/{repo}"
            "/git/trees/HEAD?recursive=1"
        )
        resp = await client.get(tree_url)
        if resp.status_code == 404:
            raise ValueError("Repository not found")
        resp.raise_for_status()

        tree = resp.json().get("tree", [])
        md_files = [
            item["path"]
            for item in tree
            if item["type"] == "blob"
            and item["path"].startswith(docs_path + "/")
            and item["path"].endswith((".md", ".mdx"))
        ]

        files: list[FetchedFile] = []
        for path in md_files:
            raw_url = (
                f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"
            )
            raw_resp = await client.get(raw_url)
            raw_resp.raise_for_status()
            metadata = _path_to_metadata(path)
            files.append(
                FetchedFile(
                    content=raw_resp.text, path=path, metadata=metadata
                )
            )

    return files
