from __future__ import annotations

import asyncio

import cohere

from app.config import get_settings

EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIMS = 1024
BATCH_SIZE = 96  # Cohere max batch size


async def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    settings = get_settings()
    client = cohere.AsyncClientV2(api_key=settings.cohere_api_key)
    results: list[list[float]] = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        vectors = await _embed_batch_with_retry(client, batch)
        results.extend(vectors)

    return results


async def _embed_batch_with_retry(
    client: cohere.AsyncClientV2, texts: list[str]
) -> list[list[float]]:
    for attempt in range(3):
        try:
            response = await client.embed(
                texts=texts,
                model=EMBEDDING_MODEL,
                input_type="search_query",
                embedding_types=["float"],
            )
            vectors = [list(e) for e in response.embeddings.float_]
            for vec in vectors:
                if len(vec) != EMBEDDING_DIMS:
                    raise ValueError(
                        f"Expected {EMBEDDING_DIMS}-dim vector, got {len(vec)}"
                    )
            return vectors
        except cohere.TooManyRequestsError:
            if attempt == 2:
                raise
            await asyncio.sleep(2**attempt)
    raise RuntimeError("Embedding failed after retries")
