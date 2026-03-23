import hashlib
import time

from fastapi import APIRouter, Depends, Request

from app.db import postgres
from app.dependencies import get_db_pool, get_qdrant, limiter
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.services import rag_pipeline

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(
    request: Request,
    body: ChatRequest,
    pool=Depends(get_db_pool),
    qdrant=Depends(get_qdrant),
) -> ChatResponse:
    start = time.time()
    response = await rag_pipeline.run_rag(body, pool, qdrant)
    latency_ms = int((time.time() - start) * 1000)

    query_hash = hashlib.sha256(body.query.encode()).hexdigest()
    await postgres.log_request(
        pool,
        endpoint="/api/chat",
        session_id=str(response.session_id),
        query_hash=query_hash,
        tokens_used=response.tokens_used,
        latency_ms=latency_ms,
        status_code=200,
    )
    return response
