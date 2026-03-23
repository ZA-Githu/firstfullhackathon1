
import hashlib
import time

from fastapi import APIRouter, Depends, Request

from app.db import postgres
from app.dependencies import get_db_pool, limiter
from app.models.requests import ChatSelectedRequest
from app.models.responses import ChatSelectedResponse
from app.services import selected_pipeline

router = APIRouter(tags=["chat-selected"])


@router.post("/chat-selected", response_model=ChatSelectedResponse)
@limiter.limit("10/minute")
async def chat_selected(
    request: Request,
    body: ChatSelectedRequest,
    pool=Depends(get_db_pool),
) -> ChatSelectedResponse:
    start = time.time()
    response = await selected_pipeline.run_selected(body, pool)
    latency_ms = int((time.time() - start) * 1000)

    query_hash = hashlib.sha256(body.query.encode()).hexdigest()
    await postgres.log_request(
        pool,
        endpoint="/api/chat-selected",
        session_id=str(response.session_id),
        query_hash=query_hash,
        tokens_used=response.tokens_used,
        latency_ms=latency_ms,
        status_code=200,
    )
    return response
