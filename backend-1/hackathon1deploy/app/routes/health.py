
import time

from fastapi import APIRouter, Request

from app.config import get_settings
from app.db.qdrant import ping_qdrant
from app.models.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request) -> HealthResponse:
    settings = get_settings()
    qdrant_client = getattr(request.app.state, "qdrant_client", None)
    qdrant_status = "ok" if (qdrant_client and ping_qdrant(qdrant_client)) else "error"

    db_status = "ok"
    try:
        async with request.app.state.db_pool.acquire() as conn:
            await conn.execute("SELECT 1")
    except Exception:
        db_status = "error"

    overall = (
        "healthy"
        if qdrant_status == "ok" and db_status == "ok"
        else "degraded"
    )
    uptime = int(time.time() - request.app.state.start_time)

    return HealthResponse(
        status=overall,
        version=settings.app_version,
        qdrant=qdrant_status,
        db=db_status,
        uptime_seconds=uptime,
    )
