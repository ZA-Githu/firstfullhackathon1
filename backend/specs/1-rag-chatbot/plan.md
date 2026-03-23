# Architecture Plan — 1-rag-chatbot Backend
version: 1.0.0
date: 2026-03-06
author: Ismat Zehra
feature: 1-rag-chatbot
status: approved

---

## 0. Open Questions — Resolved

| # | Decision | Rationale |
|---|---------|-----------|
| OQ-01 | `/api/ingest` pulls Markdown files directly from a GitHub repo URL | Zero friction for maintainer — no manual uploads or file streaming |
| OQ-02 | Sessions are ephemeral per tab — UUID generated per page load, stored in Neon Postgres but not tied to user identity | No login required; free-tier Postgres handles short-lived rows; 24hr TTL auto-purge |
| OQ-03 | LLM answer capped at 400 output tokens (~300 words) | Concise answers fit chatbot UI; avoids Render free-tier 30s timeout |
| OQ-04 | `/api/ingest` accepts `github_repo_url` + `docs_path` parameter and clones/fetches the tree via GitHub API | Same as OQ-01; GitHub raw content API requires no auth for public repos |

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Docusaurus Frontend                        │
│  (React/MDX pages — chatbot UI widget)                       │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS POST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Render Free Tier)              │
│                                                             │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ /api/    │  │ /api/chat    │  │ /api/chat-selected   │  │
│  │ ingest   │  │              │  │                      │  │
│  └────┬─────┘  └──────┬───────┘  └──────────┬───────────┘  │
│       │               │                     │              │
│  ┌────▼─────┐  ┌──────▼───────┐  ┌──────────▼───────────┐  │
│  │ Chunker  │  │ RAG Pipeline │  │ Selected-Text        │  │
│  │ + Embedder│  │ (retrieve +  │  │ Pipeline             │  │
│  │ + Qdrant │  │  augment +   │  │ (augment + generate  │  │
│  │  upsert  │  │  generate)   │  │  — NO retrieval)     │  │
│  └────┬─────┘  └──────┬───────┘  └──────────┬───────────┘  │
│       │               │                     │              │
│  ┌────▼───────────────▼─────────────────────▼───────────┐  │
│  │              Service Layer                            │  │
│  │  embedder.py  retriever.py  generator.py  chunker.py  │  │
│  └───────────────────────────────────────────────────────┘  │
│       │               │                                    │
│       ▼               ▼                                    │
│  ┌─────────┐   ┌─────────────┐   ┌───────────────────────┐ │
│  │ Qdrant  │   │   OpenAI    │   │   Neon Postgres       │ │
│  │ Cloud   │   │   API       │   │  (sessions + logs)    │ │
│  │ Free    │   │ (ada-002 +  │   │                       │ │
│  │         │   │  gpt-4o-mini│   │                       │ │
│  └─────────┘   └─────────────┘   └───────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 Directory Structure

```
ai-native-book-backend/
├── app/
│   ├── main.py                  # FastAPI app factory, middleware, router registration
│   ├── config.py                # pydantic-settings: all env vars with types + defaults
│   ├── dependencies.py          # FastAPI Depends: rate limiter, auth check, db pool
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ingest.py            # POST /api/ingest
│   │   ├── chat.py              # POST /api/chat
│   │   ├── chat_selected.py     # POST /api/chat-selected
│   │   └── health.py            # GET /api/health
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chunker.py           # RecursiveCharacterTextSplitter wrapper
│   │   ├── embedder.py          # OpenAI text-embedding-ada-002 client
│   │   ├── retriever.py         # Qdrant search (query vector → top_k chunks)
│   │   ├── generator.py         # OpenAI gpt-4o-mini chat completions
│   │   ├── rag_pipeline.py      # Orchestrates: embed → retrieve → augment → generate
│   │   ├── selected_pipeline.py # Orchestrates: augment → generate (no retrieval)
│   │   └── github_fetcher.py    # GitHub API: fetch .md files from repo tree
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py          # IngestRequest, ChatRequest, ChatSelectedRequest
│   │   └── responses.py         # IngestResponse, ChatResponse, ChatSelectedResponse, HealthResponse
│   │
│   └── db/
│       ├── __init__.py
│       ├── postgres.py          # asyncpg connection pool, query helpers
│       └── qdrant.py            # QdrantClient singleton, collection helpers
│
├── tests/
│   ├── conftest.py              # pytest fixtures: mock_openai, mock_qdrant, test_client
│   ├── unit/
│   │   ├── test_chunker.py
│   │   ├── test_embedder.py
│   │   ├── test_retriever.py
│   │   ├── test_generator.py
│   │   ├── test_rag_pipeline.py
│   │   ├── test_selected_pipeline.py
│   │   └── test_github_fetcher.py
│   └── integration/
│       ├── test_ingest.py
│       ├── test_chat.py
│       ├── test_chat_selected.py
│       └── test_health.py
│
├── .github/
│   └── workflows/
│       └── ci.yml              # lint → typecheck → test → deploy
│
├── .specify/memory/
│   └── constitution.md
├── specs/1-rag-chatbot/
│   ├── spec.md
│   ├── plan.md                  # This file
│   └── tasks.md                 # Created by /sp.tasks
├── history/prompts/
├── .env.example
├── .env                         # gitignored
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml               # Black + Flake8 + Mypy config
├── Makefile
└── README.md
```

### 2.2 Service Responsibilities

#### `chunker.py`
- Input: raw Markdown string + metadata dict `{ chapter, section, slug, source_url }`
- Uses `langchain.text_splitter.RecursiveCharacterTextSplitter`
- Chunk size: 800 tokens (tiktoken cl100k_base), overlap: 100 tokens
- Parses H1/H2/H3 headings before splitting to assign section metadata per chunk
- Output: `list[ChunkDocument]` — each with `text`, `metadata`, `content_hash` (SHA-256)

#### `embedder.py`
- Input: `list[str]` (texts to embed)
- Calls `openai.embeddings.create(model="text-embedding-ada-002", input=texts)`
- Batches requests: max 100 texts per API call
- Output: `list[list[float]]` (1536-dim vectors)
- Retry: exponential backoff × 3 on `openai.RateLimitError`

#### `retriever.py`
- Input: query vector `list[float]`, `top_k: int`, collection name `str`
- Calls `qdrant_client.search(collection_name, query_vector, limit=top_k)`
- Output: `list[RetrievedChunk]` — text, metadata, score
- **This function is NEVER called from `selected_pipeline.py`** — enforced by import isolation

#### `generator.py`
- Input: system prompt `str`, user query `str`, session history `list[Message]`
- Calls `openai.chat.completions.create(model="gpt-4o-mini", max_tokens=400)`
- Output: `GeneratorResult` — answer text, tokens used
- Builds conversation: `[system, ...history[-10:], user]`

#### `rag_pipeline.py`
- Orchestrates: `embedder.embed([query])` → `retriever.search(vector)` → build augmented prompt → `generator.generate()`
- Returns `ChatResponse` with answer + sources

#### `selected_pipeline.py`
- Orchestrates: build augmented prompt from `selected_text` only → `generator.generate()`
- **Does NOT import or call `retriever`** — import-level isolation
- Returns `ChatSelectedResponse` with answer only

#### `github_fetcher.py`
- Input: `github_repo_url: str`, `docs_path: str` (e.g. `"docs"`)
- Uses GitHub contents API: `https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1`
- Filters `.md` and `.mdx` files under `docs_path`
- Fetches each file's raw content via `https://raw.githubusercontent.com/...`
- Output: `list[FetchedFile]` — content, path, derived metadata

---

## 3. Data Models

### Request Models (Pydantic v2)

```python
class IngestRequest(BaseModel):
    github_repo_url: AnyHttpUrl | None = None
    docs_path: str = "docs"
    sources: list[IngestSource] | None = None   # direct text upload fallback
    clear_collection: bool = False

class IngestSource(BaseModel):
    text: str = Field(min_length=10)
    metadata: ChunkMetadata

class ChunkMetadata(BaseModel):
    chapter: str
    section: str
    slug: str
    source_url: str | None = None

class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    session_id: UUID | None = None
    top_k: int = Field(default=5, ge=1, le=20)
    user_background: str | None = None
    language: Literal["en", "ur"] = "en"

class ChatSelectedRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    selected_text: str = Field(min_length=10, max_length=5000)
    session_id: UUID | None = None
    language: Literal["en", "ur"] = "en"

    @field_validator("query", "selected_text")
    @classmethod
    def reject_html(cls, v: str) -> str:
        if re.search(r"<(script|img|iframe|object|embed)", v, re.IGNORECASE):
            raise ValueError("HTML tags not permitted in input fields")
        return v.strip()
```

### Neon Postgres Schema

```sql
-- Session message history
CREATE TABLE sessions (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id  UUID NOT NULL,
  role        TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content     TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_sessions_session_id ON sessions(session_id);

-- Request audit log (no PII)
CREATE TABLE request_logs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  endpoint    TEXT NOT NULL,
  session_id  UUID,
  query_hash  TEXT NOT NULL,
  tokens_used INT,
  latency_ms  INT,
  status_code INT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Ingest content hash registry (deduplication)
CREATE TABLE ingested_chunks (
  content_hash TEXT PRIMARY KEY,
  slug         TEXT NOT NULL,
  ingested_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### Qdrant Collection

```
Collection name: ai-native-book
Vector size: 1536
Distance: Cosine

Payload fields per point:
  text:         string   (chunk text)
  chapter:      string
  section:      string
  slug:         string
  source_url:   string | null
  chunk_index:  int
  content_hash: string
```

---

## 4. Request Lifecycle

### /api/chat — Full RAG
```
Request → Pydantic validation → Rate limit check
  → session_id: resolve or generate UUID
  → Fetch last 10 session messages from Neon
  → embedder.embed([query]) → 1536-dim vector
  → retriever.search(vector, top_k) → list[RetrievedChunk]
  → Build system prompt with chunks as context
  → generator.generate(system_prompt, query, history)
  → Store [user: query, assistant: answer] in Neon sessions table
  → Log request_logs row (hash, tokens, latency, status)
  → Return ChatResponse { answer, sources, session_id, tokens_used }
```

### /api/chat-selected — Isolated Context
```
Request → Pydantic validation (incl. HTML reject) → Rate limit check
  → session_id: resolve or generate UUID
  → Fetch last 10 session messages from Neon
  → Build system prompt with selected_text as sole context
  → generator.generate(system_prompt, query, history)
  → Store session messages in Neon
  → Log request_logs row
  → Return ChatSelectedResponse { answer, session_id, tokens_used }
  ⚠️  retriever is NEVER called in this path
```

### /api/ingest — Content Pipeline
```
Request → Auth check (X-API-Key header) → Pydantic validation
  → if github_repo_url: github_fetcher.fetch_docs() → list[FetchedFile]
  → else: use sources directly
  → if clear_collection: qdrant.delete_collection() + recreate
  → For each file/source:
      → chunker.chunk(text, metadata) → list[ChunkDocument]
      → For each chunk:
          → Check content_hash in Neon ingested_chunks → skip if exists
          → embedder.embed([chunk.text]) → vector
          → qdrant.upsert(point_id, vector, payload)
          → Insert content_hash into Neon ingested_chunks
  → Return IngestResponse { status, chunks_stored, skipped_duplicates, collection }
```

---

## 5. Key Architectural Decisions

### Decision 1: LangChain vs Haystack for RAG
**Chosen: LangChain**
- Rationale: Better ecosystem for OpenAI + Qdrant integration; `RecursiveCharacterTextSplitter` is production-tested; wider community support for hackathon troubleshooting
- Trade-off: Heavier dependency than Haystack; acceptable for free-tier since startup is one-time cost

### Decision 2: GitHub API vs file upload for ingestion
**Chosen: GitHub contents API (raw content fetch)**
- Rationale: Public Docusaurus repos are on GitHub; no auth required for public repos; one API call fetches the full tree; zero friction for maintainer
- Trade-off: Requires internet access during ingestion; acceptable (ingestion is a manual admin trigger, not a hot path)

### Decision 3: Ephemeral sessions (per-tab UUID, no cross-session persistence)
**Chosen: Ephemeral — UUID generated per session, stored in Neon, 24hr TTL**
- Rationale: No user auth = no identity to tie sessions to; per-tab UUIDs give conversational continuity within a reading session; 24hr TTL keeps Neon free tier clean
- Trade-off: Refreshing the page starts a new session. Acceptable for hackathon scope.

### Decision 4: asyncpg vs SQLAlchemy for Neon Postgres
**Chosen: asyncpg (direct, no ORM)**
- Rationale: FastAPI is async-first; asyncpg is the fastest async Postgres driver; schema is simple (3 tables, no complex relations); no ORM overhead needed
- Trade-off: Raw SQL instead of ORM queries — mitigated by parameterized queries (no injection risk)

### Decision 5: Qdrant Cloud Free vs self-hosted Qdrant
**Chosen: Qdrant Cloud Free Tier**
- Rationale: $0 cost; persistent storage (no data loss on Render restart); 1GB free storage (sufficient for textbook); no Docker overhead on Render free tier
- Trade-off: External network hop for every retrieval query; acceptable given p95 ≤ 5s budget

---

## 6. CI/CD Pipeline (.github/workflows/ci.yml)

```
Trigger: push to any branch + PR to main

Steps:
  1. checkout
  2. setup-python@v5 (Python 3.11)
  3. pip install -r requirements-dev.txt
  4. black . --check                     (formatter gate)
  5. flake8 app/ tests/                  (linter gate)
  6. mypy app/ --strict                  (type gate)
  7. pytest --cov=app --cov-fail-under=80 (test + coverage gate)
  8. [on main only] deploy to Render via Render Deploy Hook (curl)
```

---

## 7. Environment Variables

| Variable | Required | Default | Description |
|----------|---------- |---------|-------------|
| OPENAI_API_KEY | ✅ | — | OpenAI API key |
| QDRANT_URL | ✅ | — | Qdrant Cloud cluster URL |
| QDRANT_API_KEY | ✅ | — | Qdrant API key |
| QDRANT_COLLECTION | ✅ | ai-native-book | Qdrant collection name |
| DATABASE_URL | ✅ | — | Neon Postgres connection string (asyncpg format) |
| INGEST_API_KEY | ✅ | — | Shared secret for /api/ingest |
| CORS_ORIGINS | ✅ | — | Comma-separated allowed origins |
| ENVIRONMENT | ✅ | development | development \| production |
| GITHUB_TOKEN | ❌ | — | GitHub token for private repos (optional) |
| MAX_ANSWER_TOKENS | ❌ | 400 | Max LLM output tokens |
| LOG_RETENTION_DAYS | ❌ | 7 | Days before purging request_logs |

---

## 8. Makefile Targets

```makefile
make dev          # uvicorn app.main:app --reload --port 8000
make test         # pytest --cov=app --cov-report=term-missing --cov-fail-under=80
make lint         # black . --check && flake8 app/ tests/
make typecheck    # mypy app/ --strict
make format       # black .
make db-init      # Run schema migrations against DATABASE_URL
make ingest       # POST /api/ingest with local test payload
```

---

## 9. Performance Budget

| Metric | Budget | Strategy |
|--------|--------|---------|
| p95 /api/chat | ≤ 5s | top_k=5 (not 10); gpt-4o-mini (fast); Qdrant cloud same-region |
| p95 /api/chat-selected | ≤ 3s | No retrieval; gpt-4o-mini only |
| p95 /api/ingest | ≤ 60s | Batch embeddings (100/call); async upserts |
| p95 /api/health | ≤ 500ms | Lightweight ping queries only |
| Render cold start | ≤ 30s | Acceptable for free tier |
| Neon Postgres queries | ≤ 50ms | Indexed on session_id |

---

## 10. Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| OpenAI rate limits during ingestion | Medium | High | Batch embeddings; exponential backoff × 3 |
| Render free-tier cold start kills UX | High | Medium | Cache-warmup ping in frontend; show "Waking up..." spinner |
| Qdrant collection corruption on re-ingest | Low | High | `clear_collection: false` by default; explicit flag required |
| Neon free-tier connection limit (max 5) | Medium | Medium | asyncpg pool max_size=3; connection reuse |
| LLM hallucination despite system prompt | Low | High | System prompt enforces "textbook only"; test with off-topic queries in CI |

---

## 11. Phase Plan

| Phase | Scope | Gate |
|-------|-------|------|
| 1 | Project scaffold: FastAPI app, config, Pydantic models, middleware, .env, Makefile | `make dev` starts without errors |
| 2 | Service layer: chunker + embedder + retriever + generator (with mocks) | Unit tests green, 80%+ coverage |
| 3 | RAG pipeline + /api/chat endpoint | Integration test SC-01, SC-02 pass |
| 4 | Selected-text pipeline + /api/chat-selected endpoint | SC-03, SC-04, SC-05 pass |
| 5 | GitHub fetcher + /api/ingest endpoint | SC-11, SC-12, SC-13 pass |
| 6 | /api/health + Neon session logging + request log purge | SC-10 passes; logs visible in Neon |
| 7 | CI/CD pipeline + README + deploy to Render | All 15 SCs pass in CI; live URL accessible |

---

## 12. ADR Suggestions

📋 **Architectural decision detected: LangChain vs Haystack for RAG pipeline**
Document reasoning and tradeoffs? Run `/sp.adr langchain-vs-haystack`

📋 **Architectural decision detected: Ephemeral sessions vs persistent cross-session history**
Document reasoning and tradeoffs? Run `/sp.adr session-persistence-strategy`

📋 **Architectural decision detected: asyncpg vs SQLAlchemy for Neon Postgres**
Document reasoning and tradeoffs? Run `/sp.adr asyncpg-vs-sqlalchemy`
