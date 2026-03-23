"""IngestionSkill — chunk Markdown → embed → upsert to Qdrant + record hash in Postgres.

Thin wrapper around the existing chunker, embedder, and qdrant services so the
master agent can trigger ingestion programmatically without going through the HTTP route.
"""
from __future__ import annotations

import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.config import get_settings
from app.db import postgres
from app.db.qdrant import ensure_collection
from app.models.requests import IngestSource
from app.services import chunker, embedder


async def run_ingestion_skill(
    sources: list[dict],
    pool=None,
    qdrant_client: QdrantClient | None = None,
    clear_collection: bool = False,
) -> dict:
    """Ingest Markdown sources into Qdrant + Postgres.

    Args:
        sources: List of dicts with keys: text (str), metadata (dict with
                 chapter, section, slug, source_url).
        pool: asyncpg pool.
        qdrant_client: Qdrant client.
        clear_collection: If True, wipe and recreate the collection first.

    Returns:
        dict with keys: status, chunks_stored, skipped_duplicates
    """
    settings = get_settings()
    collection = settings.qdrant_collection

    if clear_collection and qdrant_client:
        from app.db.qdrant import delete_collection
        delete_collection(qdrant_client, collection)
        ensure_collection(qdrant_client, collection)
        if pool:
            await postgres.clear_chunk_hashes(pool)

    ingest_sources = [
        IngestSource(text=s["text"], metadata=s.get("metadata", {}))
        for s in sources
    ]

    chunks_stored = 0
    skipped = 0

    for source in ingest_sources:
        chunks = chunker.chunk_document(source.text, source.metadata)
        new_chunks = []
        for chunk in chunks:
            if pool and await postgres.chunk_hash_exists(pool, chunk.content_hash):
                skipped += 1
            else:
                new_chunks.append(chunk)

        if new_chunks and qdrant_client:
            texts = [c.text for c in new_chunks]
            vectors = await embedder.embed_texts(texts)
            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vec,
                    payload={
                        "text": c.text,
                        "chapter": c.metadata.chapter,
                        "section": c.metadata.section,
                        "slug": c.metadata.slug,
                        "source_url": c.metadata.source_url,
                        "content_hash": c.content_hash,
                    },
                )
                for c, vec in zip(new_chunks, vectors)
            ]
            qdrant_client.upsert(collection_name=collection, points=points)
            if pool:
                for c in new_chunks:
                    await postgres.record_chunk_hash(
                        pool, c.content_hash, c.metadata.slug
                    )
            chunks_stored += len(new_chunks)

    return {
        "status": "ok",
        "chunks_stored": chunks_stored,
        "skipped_duplicates": skipped,
    }
