
import uuid

from fastapi import APIRouter, Depends, Request
from qdrant_client.models import PointStruct

from app.config import get_settings
from app.db import postgres
from app.db.qdrant import delete_collection, ensure_collection
from app.dependencies import get_db_pool, get_qdrant, verify_ingest_key
from app.models.requests import IngestRequest, IngestSource
from app.models.responses import IngestResponse
from app.services import chunker, embedder, github_fetcher

router = APIRouter(tags=["ingest"])


@router.post(
    "/ingest",
    response_model=IngestResponse,
    dependencies=[Depends(verify_ingest_key)],
)
async def ingest(
    request: Request,
    body: IngestRequest,
    pool=Depends(get_db_pool),
    qdrant=Depends(get_qdrant),
) -> IngestResponse:
    settings = get_settings()
    collection = settings.qdrant_collection

    if body.clear_collection:
        delete_collection(qdrant, collection)
        ensure_collection(qdrant, collection)
        if pool is not None:
            await postgres.clear_chunk_hashes(pool)

    sources: list[IngestSource] = list(body.sources or [])
    if body.github_repo_url:
        fetched = await github_fetcher.fetch_docs(
            str(body.github_repo_url), body.docs_path
        )
        sources.extend(
            IngestSource(text=f.content, metadata=f.metadata) for f in fetched
        )

    chunks_stored = 0
    skipped = 0

    for source in sources:
        chunks = chunker.chunk_document(source.text, source.metadata)
        new_chunks = []
        for chunk in chunks:
            if pool is not None and await postgres.chunk_hash_exists(pool, chunk.content_hash):
                skipped += 1
            else:
                new_chunks.append(chunk)

        if new_chunks:
            texts = [c.text for c in new_chunks]
            vectors = await embedder.embed_texts(texts, input_type="search_document")
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
            qdrant.upsert(collection_name=collection, points=points)
            if pool is not None:
                for c in new_chunks:
                    await postgres.record_chunk_hash(pool, c.content_hash, c.metadata.slug)
            chunks_stored += len(new_chunks)

    return IngestResponse(
        status="ok",
        chunks_stored=chunks_stored,
        skipped_duplicates=skipped,
        collection=collection,
    )
