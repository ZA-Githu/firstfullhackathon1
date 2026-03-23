from __future__ import annotations

from fastapi import HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings

limiter = Limiter(key_func=get_remote_address)

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_ingest_key(
    api_key: str | None = Security(_api_key_header),
) -> None:
    settings = get_settings()
    if not api_key or api_key != settings.ingest_api_key:
        raise HTTPException(
            status_code=401, detail="Invalid or missing X-API-Key"
        )


def get_db_pool(request: Request):  # type: ignore[return]
    return request.app.state.db_pool


def get_qdrant(request: Request):  # type: ignore[return]
    return request.app.state.qdrant_client
