from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    chapter: str
    section: str
    slug: str
    relevance_score: float = Field(ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
    session_id: UUID
    tokens_used: int


class ChatSelectedResponse(BaseModel):
    answer: str
    session_id: UUID
    tokens_used: int


class IngestResponse(BaseModel):
    status: str
    chunks_stored: int
    skipped_duplicates: int
    collection: str


class HealthResponse(BaseModel):
    status: str
    version: str
    qdrant: str
    db: str
    uptime_seconds: int


class ErrorResponse(BaseModel):
    error: str
    code: str
    detail: str | None = None
