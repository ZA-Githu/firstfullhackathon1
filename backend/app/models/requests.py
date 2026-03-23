from __future__ import annotations

import re
from typing import Any, Literal
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator, model_validator

_HTML_PATTERN = re.compile(r"<(script|img|iframe|object|embed)", re.IGNORECASE)


def _reject_html(v: str) -> str:
    if _HTML_PATTERN.search(v):
        raise ValueError("HTML tags not permitted in input fields")
    return v.strip()


class ChunkMetadata(BaseModel):
    chapter: str
    section: str
    slug: str
    source_url: str | None = None


class IngestSource(BaseModel):
    text: str = Field(min_length=10)
    metadata: ChunkMetadata


class IngestRequest(BaseModel):
    github_repo_url: AnyHttpUrl | None = None
    docs_path: str = "docs"
    sources: list[IngestSource] | None = None
    clear_collection: bool = False

    @model_validator(mode="after")
    def require_source_or_url(self) -> "IngestRequest":
        if not self.github_repo_url and not self.sources:
            raise ValueError("Provide either github_repo_url or sources")
        return self


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    session_id: UUID | None = None
    top_k: int = Field(default=5, ge=1, le=20)
    user_background: str | None = None
    language: Literal["en", "ur"] = "en"

    @field_validator("query")
    @classmethod
    def clean_query(cls, v: str) -> str:
        return _reject_html(v)


class ChatSelectedRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    selected_text: str = Field(min_length=10, max_length=5000)
    session_id: UUID | None = None
    language: Literal["en", "ur"] = "en"

    @field_validator("query", "selected_text")
    @classmethod
    def clean_fields(cls, v: str) -> str:
        return _reject_html(v)
