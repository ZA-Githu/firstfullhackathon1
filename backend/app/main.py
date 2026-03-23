from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.db.postgres import create_pool, init_schema, purge_old_logs
from app.db.qdrant import ensure_collection, get_qdrant_client
from app.dependencies import limiter
from app.routes import agent, chat, chat_selected, health, ingest

settings = get_settings()

app = FastAPI(
    title="AI-Native Book RAG Chatbot",
    version=settings.app_version,
    description="RAG backend for Physical AI & Humanoid Robotics textbook",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
    max_age=86400,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(ingest.router, prefix="/api")
app.include_router(agent.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(chat_selected.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.on_event("startup")
async def startup() -> None:
    app.state.start_time = time.time()

    # Postgres — non-fatal if unreachable
    try:
        app.state.db_pool = await create_pool()
        await init_schema(app.state.db_pool)
        await purge_old_logs(app.state.db_pool, settings.log_retention_days)
    except Exception as exc:
        logger.warning("Postgres not reachable at startup (continuing): %s", exc)
        app.state.db_pool = None

    # Qdrant — non-fatal if unreachable
    try:
        app.state.qdrant_client = get_qdrant_client()
        ensure_collection(app.state.qdrant_client, settings.qdrant_collection)
    except Exception as exc:
        logger.warning("Qdrant not reachable at startup (continuing): %s", exc)
        app.state.qdrant_client = None


@app.on_event("shutdown")
async def shutdown() -> None:
    await app.state.db_pool.close()


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR"},
    )
