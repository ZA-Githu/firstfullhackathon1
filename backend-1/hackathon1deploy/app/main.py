from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.db.postgres import create_pool, init_schema, purge_old_logs
from app.db.qdrant import ensure_collection, get_qdrant_client
from app.dependencies import limiter
from app.routes import chat, chat_selected, health, ingest

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title="AI-Native Book RAG Chatbot",
    version=settings.app_version,
    description="RAG backend for Physical AI & Humanoid Robotics textbook",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
    max_age=86400,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(ingest.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(chat_selected.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root() -> HTMLResponse:
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Physical AI & Humanoid Robotics — RAG API</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #060b18;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      background: rgba(6,182,212,0.06);
      border: 1px solid rgba(6,182,212,0.25);
      border-radius: 20px;
      padding: 3rem 2.5rem;
      max-width: 600px;
      width: 90%;
      text-align: center;
    }
    .badge {
      display: inline-block;
      background: rgba(6,182,212,0.12);
      border: 1px solid rgba(6,182,212,0.35);
      border-radius: 999px;
      padding: 0.35rem 1rem;
      font-size: 0.78rem;
      color: #67e8f9;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 1.5rem;
    }
    h1 {
      font-size: 1.9rem;
      font-weight: 900;
      background: linear-gradient(135deg, #fff 0%, #67e8f9 50%, #fbbf24 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 0.75rem;
      line-height: 1.2;
    }
    p { color: rgba(255,255,255,0.55); line-height: 1.7; margin-bottom: 2rem; }
    .links { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
    a {
      padding: 0.75rem 1.75rem;
      border-radius: 10px;
      font-weight: 700;
      font-size: 0.95rem;
      text-decoration: none;
      transition: all 0.2s;
    }
    .btn-primary {
      background: linear-gradient(135deg, #06b6d4, #0284c7);
      color: #fff;
      box-shadow: 0 4px 20px rgba(6,182,212,0.4);
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(6,182,212,0.55); }
    .btn-ghost {
      border: 1px solid rgba(6,182,212,0.35);
      color: #67e8f9;
    }
    .btn-ghost:hover { background: rgba(6,182,212,0.1); }
    .status {
      margin-top: 2rem;
      padding: 0.6rem 1rem;
      background: rgba(16,185,129,0.1);
      border: 1px solid rgba(16,185,129,0.3);
      border-radius: 8px;
      font-size: 0.82rem;
      color: #6ee7b7;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">✨ Panaversity Hackathon 1</div>
    <h1>Physical AI &amp; Humanoid Robotics RAG API</h1>
    <p>
      FastAPI backend powering the AI-Native textbook chatbot.<br/>
      Built with Cohere embeddings, Qdrant vector search, and RAG pipeline.
    </p>
    <div class="links">
      <a href="/docs" class="btn-primary">📖 API Docs (Swagger)</a>
      <a href="/redoc" class="btn-ghost">ReDoc</a>
      <a href="/api/health" class="btn-ghost">Health Check</a>
    </div>
    <div class="status">🟢 Server is running</div>
  </div>
</body>
</html>
""")


@app.on_event("startup")
async def startup() -> None:
    app.state.start_time = time.time()

    # Postgres — non-fatal if not configured or unreachable
    try:
        if settings.database_url:
            app.state.db_pool = await create_pool()
            await init_schema(app.state.db_pool)
            await purge_old_logs(app.state.db_pool, settings.log_retention_days)
        else:
            logger.warning("DATABASE_URL not set — running without Postgres")
            app.state.db_pool = None
    except Exception as exc:
        logger.warning("Postgres not reachable at startup (continuing): %s", exc)
        app.state.db_pool = None

    # Qdrant — non-fatal if not configured or unreachable
    try:
        app.state.qdrant_client = get_qdrant_client()
        ensure_collection(app.state.qdrant_client, settings.qdrant_collection)
    except Exception as exc:
        logger.warning("Qdrant not reachable at startup (continuing): %s", exc)
        app.state.qdrant_client = None


@app.on_event("shutdown")
async def shutdown() -> None:
    if app.state.db_pool:
        await app.state.db_pool.close()


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR"},
    )
