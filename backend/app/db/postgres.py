from __future__ import annotations

import asyncpg
from app.config import get_settings

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  UUID NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content     TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);

CREATE TABLE IF NOT EXISTS request_logs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint    TEXT NOT NULL,
    session_id  UUID,
    query_hash  TEXT NOT NULL,
    tokens_used INT,
    latency_ms  INT,
    status_code INT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingested_chunks (
    content_hash TEXT PRIMARY KEY,
    slug         TEXT NOT NULL,
    ingested_at  TIMESTAMPTZ DEFAULT NOW()
);
"""


async def create_pool() -> asyncpg.Pool:
    settings = get_settings()
    if not settings.database_url:
        raise ValueError("DATABASE_URL is not configured")
    return await asyncpg.create_pool(settings.database_url, min_size=1, max_size=3)


async def init_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(SCHEMA_SQL)


async def get_session_history(
    pool: asyncpg.Pool, session_id: str
) -> list[dict[str, str]]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT role, content FROM sessions WHERE session_id = $1::uuid "
            "ORDER BY created_at DESC LIMIT 10",
            session_id,
        )
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


async def save_session_messages(
    pool: asyncpg.Pool,
    session_id: str,
    user_msg: str,
    assistant_msg: str,
) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO sessions (session_id, role, content) "
                "VALUES ($1::uuid, $2, $3)",
                session_id,
                "user",
                user_msg,
            )
            await conn.execute(
                "INSERT INTO sessions (session_id, role, content) "
                "VALUES ($1::uuid, $2, $3)",
                session_id,
                "assistant",
                assistant_msg,
            )


async def log_request(
    pool: asyncpg.Pool,
    endpoint: str,
    session_id: str | None,
    query_hash: str,
    tokens_used: int | None,
    latency_ms: int,
    status_code: int,
) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO request_logs "
            "(endpoint, session_id, query_hash, tokens_used, latency_ms, status_code) "
            "VALUES ($1, $2::uuid, $3, $4, $5, $6)",
            endpoint,
            session_id,
            query_hash,
            tokens_used,
            latency_ms,
            status_code,
        )


async def purge_old_logs(
    pool: asyncpg.Pool, retention_days: int = 7
) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM request_logs "
            "WHERE created_at < NOW() - ($1 || ' days')::INTERVAL",
            str(retention_days),
        )
        await conn.execute(
            "DELETE FROM sessions WHERE created_at < NOW() - INTERVAL '24 hours'"
        )


async def chunk_hash_exists(pool: asyncpg.Pool, content_hash: str) -> bool:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT 1 FROM ingested_chunks WHERE content_hash = $1", content_hash
        )
    return row is not None


async def record_chunk_hash(
    pool: asyncpg.Pool, content_hash: str, slug: str
) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO ingested_chunks (content_hash, slug) VALUES ($1, $2) "
            "ON CONFLICT DO NOTHING",
            content_hash,
            slug,
        )


async def clear_chunk_hashes(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM ingested_chunks")
