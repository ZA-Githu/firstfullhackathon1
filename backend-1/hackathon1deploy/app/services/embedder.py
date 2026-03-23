from __future__ import annotations

import cohere

from app.config import get_settings

EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIM = 1024
BATCH_SIZE = 96


async def embed_texts(
    texts: list[str],
    input_type: str = "search_query",
) -> list[list[float]]:
    if not texts:
        return []

    settings = get_settings()
    client = cohere.AsyncClientV2(api_key=settings.cohere_api_key)
    results: list[list[float]] = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = await client.embed(
            texts=batch,
            model=EMBEDDING_MODEL,
            input_type=input_type,
            embedding_types=["float"],
        )
        vectors = response.embeddings.float_
        for vec in vectors:
            if len(vec) != EMBEDDING_DIM:
                raise ValueError(f"Expected {EMBEDDING_DIM}-dim vector, got {len(vec)}")
        results.extend(vectors)

    return results
