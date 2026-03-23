from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import get_settings

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        settings = get_settings()
        if settings.qdrant_url == ":memory:":
            _client = QdrantClient(":memory:")
        else:
            _client = QdrantClient(
                url=settings.qdrant_url, api_key=settings.qdrant_api_key
            )
    return _client


def ensure_collection(client: QdrantClient, name: str) -> None:
    """Create the collection if it doesn't exist. Non-fatal on connection errors."""
    try:
        existing = [c.name for c in client.get_collections().collections]
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning(
            "Qdrant not reachable at startup (collection check skipped): %s", exc
        )


def delete_collection(client: QdrantClient, name: str) -> None:
    client.delete_collection(collection_name=name)


def ping_qdrant(client: QdrantClient) -> bool:
    try:
        client.get_collections()
        return True
    except Exception:
        return False
