from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException
from qdrant_client import QdrantClient


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
        results = client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail="Vector store unavailable"
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
