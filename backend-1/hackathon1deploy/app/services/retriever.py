from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector


@dataclass
class RetrievedChunk:
    text: str
    chapter: str
    section: str
    slug: str
    relevance_score: float


async def retrieve(
    query_vector: list[float],
    top_k: int,
    collection: str,
    client: QdrantClient,
) -> list[RetrievedChunk]:
    try:
        results = client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        ).points
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"Vector store unavailable: {type(exc).__name__}: {exc}"
        ) from exc

    return [
        RetrievedChunk(
            text=hit.payload.get("text", "") if hit.payload else "",
            chapter=hit.payload.get("chapter", "") if hit.payload else "",
            section=hit.payload.get("section", "") if hit.payload else "",
            slug=hit.payload.get("slug", "") if hit.payload else "",
            relevance_score=round(hit.score, 2),
        )
        for hit in results
    ]
