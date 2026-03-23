# Tasks — 1-rag-chatbot Backend
version: 1.0.0
date: 2026-03-06
feature: 1-rag-chatbot
status: in-progress
total: 72
completed: 0

---

## Phase 1 — Project Scaffold
**Gate:** `make dev` starts without errors; `GET /api/health` returns 200

### T-001 — Create project root structure
- [ ] Create `ai-native-book-backend/` with all directories: `app/routes/`, `app/services/`, `app/models/`, `app/db/`, `tests/unit/`, `tests/integration/`, `.github/workflows/`
- **Test:** `ls` confirms all directories exist

### T-002 — Create `requirements.txt`
- [ ] Pin all production dependencies:
  ```
  fastapi==0.115.0
  uvicorn[standard]==0.30.6
  pydantic==2.8.2
  pydantic-settings==2.4.0
  openai==1.51.0
  langchain==0.3.0
  langchain-text-splitters==0.3.0
  qdrant-client==1.11.0
  asyncpg==0.29.0
  slowapi==0.1.9
  httpx==0.27.2
  python-dotenv==1.0.1
  tiktoken==0.7.0
  ```
- **Test:** `pip install -r requirements.txt` exits 0

### T-003 — Create `requirements-dev.txt`
- [ ] Pin all dev/test dependencies:
  ```
  pytest==8.3.3
  pytest-asyncio==0.24.0
  pytest-cov==5.0.0
  httpx==0.27.2
  black==24.8.0
  flake8==7.1.1
  mypy==1.11.2
  types-httpx
  respx==0.21.1
  ```
- **Test:** `pip install -r requirements-dev.txt` exits 0

### T-004 — Create `pyproject.toml`
- [ ] Configure Black (line-length = 88), Flake8 (max-line-length = 88, ignore = E203,W503), Mypy (strict = true)
- [ ] Configure pytest: `asyncio_mode = "auto"`, testpaths = `["tests"]`
- **Test:** `black . --check` and `flake8 app/` exit 0 on empty project

### T-005 — Create `.env.example`
- [ ] Document all 11 environment variables with placeholder values and inline comments
- **Test:** File exists; no real secrets present

### T-006 — Create `.env` (local only)
- [ ] Populate with real local/dev values for: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION, DATABASE_URL, INGEST_API_KEY, CORS_ORIGINS, ENVIRONMENT=development
- [ ] Confirm `.gitignore` excludes `.env`
- **Test:** `.env` not tracked by git (`git status` shows untracked or ignored)

### T-007 — Create `app/config.py`
- [ ] `class Settings(BaseSettings)` with all env vars typed
- [ ] `model_config = SettingsConfigDict(env_file=".env")`
- [ ] `get_settings()` cached with `@lru_cache`
- **Test:** `from app.config import get_settings; s = get_settings(); assert s.environment in ("development", "production")`

### T-008 — Create `app/db/postgres.py`
- [ ] `create_pool()` — asyncpg connection pool, max_size=3
- [ ] `get_pool()` dependency returning pool from app state
- [ ] `execute_query(pool, sql, *args)` helper (parameterized, no string interpolation)
- [ ] `init_schema(pool)` — runs CREATE TABLE IF NOT EXISTS for sessions, request_logs, ingested_chunks
- **Test:** Unit test mocks asyncpg; asserts `create_pool` is called with DATABASE_URL

### T-009 — Create `app/db/qdrant.py`
- [ ] `get_qdrant_client()` — `QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)` singleton
- [ ] `ensure_collection(client, name)` — creates collection if not exists (1536-dim, cosine)
- [ ] `ping_qdrant(client)` — lightweight collections list call; returns True/False
- **Test:** Unit test mocks QdrantClient; asserts `ensure_collection` calls `recreate_collection` with correct vector params

### T-010 — Create `app/main.py`
- [ ] FastAPI app factory with title, version, description
- [ ] Add CORS middleware: origins from `settings.cors_origins.split(",")`
- [ ] Add slowapi `RateLimitMiddleware`
- [ ] Register all 4 routers under `/api` prefix
- [ ] `@app.on_event("startup")`: create asyncpg pool, init schema, ensure Qdrant collection
- [ ] `@app.on_event("shutdown")`: close pool
- [ ] Global exception handler: catches unhandled exceptions → 500 JSON response
- **Test:** `make dev` starts; `curl http://localhost:8000/api/health` returns 200

### T-011 — Create `app/dependencies.py`
- [ ] `get_db_pool` — FastAPI Depends, returns pool from app.state
- [ ] `verify_ingest_key` — checks `X-API-Key` header == `settings.ingest_api_key`; raises 401 if missing/wrong
- [ ] `limiter` — `slowapi.Limiter(key_func=get_remote_address)`
- **Test:** Unit test: `verify_ingest_key` raises HTTPException(401) when header missing

### T-012 — Create `Makefile`
- [ ] `make dev`, `make test`, `make lint`, `make typecheck`, `make format`, `make db-init`, `make ingest`
- **Test:** `make lint` exits 0 on scaffold

---

## Phase 2 — Service Layer (with unit tests)
**Gate:** All unit tests green; `pytest --cov=app --cov-fail-under=80`

### T-013 — Create `app/models/requests.py`
- [ ] `IngestSource(BaseModel)`: text (min 10), metadata: ChunkMetadata
- [ ] `ChunkMetadata(BaseModel)`: chapter, section, slug, source_url (optional)
- [ ] `IngestRequest(BaseModel)`: github_repo_url (AnyHttpUrl | None), docs_path="docs", sources (list | None), clear_collection=False. Validator: at least one of github_repo_url or sources required.
- [ ] `ChatRequest(BaseModel)`: query (1–1000), session_id (UUID | None), top_k (1–20, default 5), user_background (str | None), language ("en"|"ur", default "en")
- [ ] `ChatSelectedRequest(BaseModel)`: query (1–1000), selected_text (10–5000), session_id (UUID | None), language. `@field_validator` rejects `<script>`, `<img>`, `<iframe>`, `<object>`, `<embed>` in both fields. Strips whitespace.
- **Test:** `test_requests.py` — 8 tests: valid payloads pass; invalid lengths raise ValidationError; HTML tags raise ValidationError; both fields stripped

### T-014 — Create `app/models/responses.py`
- [ ] `SourceReference(BaseModel)`: chapter, section, slug, relevance_score (float, 0–1)
- [ ] `ChatResponse(BaseModel)`: answer, sources (list[SourceReference]), session_id (UUID), tokens_used (int)
- [ ] `ChatSelectedResponse(BaseModel)`: answer, session_id (UUID), tokens_used (int)
- [ ] `IngestResponse(BaseModel)`: status, chunks_stored (int), skipped_duplicates (int), collection (str)
- [ ] `HealthResponse(BaseModel)`: status ("healthy"|"degraded"), version, qdrant ("ok"|"error"), db ("ok"|"error"), uptime_seconds (int)
- [ ] `ErrorResponse(BaseModel)`: error, code, detail (str | None)
- **Test:** Instantiate each model with valid data; assert field types correct

### T-015 — Create `app/services/chunker.py`
- [ ] `chunk_document(text: str, metadata: ChunkMetadata) -> list[ChunkDocument]`
- [ ] Use `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100, length_function=tiktoken_len)`
- [ ] Before splitting: parse H1/H2/H3 headings with regex; assign nearest heading to each chunk
- [ ] Each `ChunkDocument` has: text, metadata (with chapter/section/slug resolved), content_hash (SHA-256 of text)
- [ ] Discard chunks with < 50 tokens
- **Test:** `test_chunker.py` — 5 tests:
  - [ ] Long text → multiple chunks; each chunk ≤ 800 tokens
  - [ ] Short text (< 50 tokens) → empty list returned
  - [ ] H2 heading "## ROS 2 Nodes" correctly assigned to following chunks
  - [ ] Same text twice → same content_hash (deterministic)
  - [ ] Overlap: adjacent chunks share ~100 tokens of content

### T-016 — Create `app/services/embedder.py`
- [ ] `async def embed_texts(texts: list[str]) -> list[list[float]]`
- [ ] Batch: max 100 texts per API call; loop if more
- [ ] Use `openai.AsyncOpenAI` client
- [ ] Retry on `openai.RateLimitError`: exponential backoff (1s, 2s, 4s), max 3 attempts; raise on 4th
- [ ] Validate output: each vector is length 1536; raise ValueError if not
- **Test:** `test_embedder.py` — 5 tests:
  - [ ] Mock `openai.AsyncOpenAI`; assert returns list of 1536-dim vectors
  - [ ] Batching: 150 texts → 2 API calls (100 + 50)
  - [ ] RateLimitError → retries 3 times then raises
  - [ ] Empty input list → returns empty list
  - [ ] Wrong vector length → raises ValueError

### T-017 — Create `app/services/retriever.py`
- [ ] `async def retrieve(query_vector: list[float], top_k: int, collection: str) -> list[RetrievedChunk]`
- [ ] Calls `qdrant_client.search(collection_name=collection, query_vector=query_vector, limit=top_k, with_payload=True)`
- [ ] Returns `list[RetrievedChunk]`: text, chapter, section, slug, relevance_score
- [ ] Handles `qdrant_client.exceptions.UnexpectedResponse` → raises `ServiceUnavailableError`
- **Test:** `test_retriever.py` — 4 tests:
  - [ ] Mock Qdrant client; assert returns correct RetrievedChunk list
  - [ ] top_k=3 → exactly 3 results
  - [ ] Qdrant unreachable → ServiceUnavailableError raised
  - [ ] Empty Qdrant result → returns empty list

### T-018 — Create `app/services/generator.py`
- [ ] `async def generate(system_prompt: str, query: str, history: list[Message]) -> GeneratorResult`
- [ ] Builds message list: `[{role: "system", content: system_prompt}, ...history[-10:], {role: "user", content: query}]`
- [ ] Calls `openai.AsyncOpenAI().chat.completions.create(model="gpt-4o-mini", messages=messages, max_tokens=settings.max_answer_tokens)`
- [ ] Returns `GeneratorResult(answer=response.choices[0].message.content, tokens_used=response.usage.total_tokens)`
- [ ] Handles `openai.APIError` → raises `ServiceUnavailableError`
- **Test:** `test_generator.py` — 5 tests:
  - [ ] Mock OpenAI; assert returns GeneratorResult with answer string
  - [ ] History > 10 → only last 10 included in messages
  - [ ] History = 0 → messages = [system, user] only
  - [ ] max_tokens=400 passed to API call
  - [ ] OpenAI APIError → ServiceUnavailableError raised

### T-019 — Create `app/services/rag_pipeline.py`
- [ ] `async def run_rag(request: ChatRequest, pool, qdrant_client) -> ChatResponse`
- [ ] Step 1: `embedder.embed_texts([request.query])` → query_vector
- [ ] Step 2: `retriever.retrieve(query_vector, request.top_k, settings.qdrant_collection)` → chunks
- [ ] Step 3: Build system prompt — prepend "textbook only" instruction + format chunks with chapter/section labels
- [ ] Step 4: Fetch last 10 session messages from Neon via `postgres.get_session_history(pool, session_id)`
- [ ] Step 5: `generator.generate(system_prompt, request.query, history)` → result
- [ ] Step 6: Save `[user: query, assistant: answer]` to Neon sessions
- [ ] Step 7: Return `ChatResponse` with sources from chunks (sorted by relevance_score desc)
- **Test:** `test_rag_pipeline.py` — 6 tests:
  - [ ] All mocked; full pipeline executes in correct order
  - [ ] Off-topic result (empty chunks) → answer contains scope disclaimer
  - [ ] Sources sorted by relevance_score descending
  - [ ] session_id=None → new UUID generated and returned
  - [ ] session_id provided → history fetched and passed to generator
  - [ ] ServiceUnavailableError from embedder propagates correctly

### T-020 — Create `app/services/selected_pipeline.py`
- [ ] `async def run_selected(request: ChatSelectedRequest, pool, ...) -> ChatSelectedResponse`
- [ ] **Does NOT import retriever.py** — enforced by module-level import check in tests
- [ ] Step 1: Build system prompt with `selected_text` as sole context + "cannot answer" instruction
- [ ] Step 2: Fetch last 10 session messages from Neon
- [ ] Step 3: `generator.generate(system_prompt, request.query, history)` → result
- [ ] Step 4: Save session messages to Neon
- [ ] Step 5: Return `ChatSelectedResponse`
- **Test:** `test_selected_pipeline.py` — 6 tests:
  - [ ] **Import isolation**: `assert "retriever" not in sys.modules` after importing selected_pipeline
  - [ ] Mock generator; assert retriever mock is NEVER called (call_count == 0)
  - [ ] Answerable selection → answer returned
  - [ ] Unanswerable question → answer == "This question cannot be answered from the selected text alone."
  - [ ] session_id=None → new UUID generated
  - [ ] selected_text strips whitespace before prompt construction

### T-021 — Create `app/services/github_fetcher.py`
- [ ] `async def fetch_docs(repo_url: str, docs_path: str, token: str | None) -> list[FetchedFile]`
- [ ] Parse `repo_url` to extract `owner/repo` (supports `https://github.com/owner/repo` format)
- [ ] Call GitHub trees API: `GET https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1`
- [ ] Auth: add `Authorization: Bearer {token}` header if `GITHUB_TOKEN` set; else unauthenticated (60 req/hr limit)
- [ ] Filter: only `.md` and `.mdx` files under `docs_path`
- [ ] Fetch each file's raw content from `https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}`
- [ ] Extract metadata from file path: `docs/week-3/ros2-nodes.md` → `{ chapter: "week-3", section: "ros2-nodes", slug: "week-3/ros2-nodes" }`
- [ ] Returns `list[FetchedFile(content: str, path: str, metadata: ChunkMetadata)]`
- **Test:** `test_github_fetcher.py` — 5 tests:
  - [ ] Mock httpx; GitHub trees API returns 3 .md files → 3 FetchedFile objects
  - [ ] Non-.md files filtered out
  - [ ] Files outside docs_path filtered out
  - [ ] Invalid repo URL → raises ValueError
  - [ ] GitHub API 404 → raises ValueError("Repository not found")

---

## Phase 3 — /api/chat Endpoint
**Gate:** SC-01 and SC-02 integration tests pass

### T-022 — Create `app/routes/chat.py`
- [ ] `router = APIRouter(prefix="/api", tags=["chat"])`
- [ ] `@router.post("/chat", response_model=ChatResponse)`
- [ ] Apply `@limiter.limit("10/minute")` decorator
- [ ] Inject: `request: Request`, `body: ChatRequest`, `pool=Depends(get_db_pool)`, `qdrant=Depends(get_qdrant_client)`
- [ ] Call `rag_pipeline.run_rag(body, pool, qdrant)`
- [ ] On `ServiceUnavailableError` → 503
- [ ] Log to `request_logs` (hash query, record latency, tokens, status)
- **Test:** `tests/integration/test_chat.py` — 7 tests:
  - [ ] SC-01: POST with "Explain ROS 2 nodes" → 200, answer non-empty, sources ≥ 1
  - [ ] SC-02: Off-topic query → 200, answer contains "only answer questions based on"
  - [ ] SC-06: query length 1001 → 422
  - [ ] SC-08: empty query → 422
  - [ ] SC-09: 11 requests → 11th is 429 with Retry-After header
  - [ ] Missing body → 422
  - [ ] language="ur" → 200 with stub response

### T-023 — Verify rate limiting on /api/chat
- [ ] Confirm `X-RateLimit-Limit: 10` and `X-RateLimit-Remaining: N` headers present on 200 responses
- [ ] Confirm `Retry-After: 60` header on 429 response
- **Test:** Extend `test_chat.py` with header assertions

---

## Phase 4 — /api/chat-selected Endpoint
**Gate:** SC-03, SC-04, SC-05 integration tests pass

### T-024 — Create `app/routes/chat_selected.py`
- [ ] `@router.post("/chat-selected", response_model=ChatSelectedResponse)`
- [ ] Apply `@limiter.limit("10/minute")` decorator
- [ ] Inject: `request: Request`, `body: ChatSelectedRequest`, `pool`, `qdrant` (qdrant injected but NOT passed to pipeline)
- [ ] Call `selected_pipeline.run_selected(body, pool)`
- [ ] On `ServiceUnavailableError` → 503
- [ ] Log to `request_logs`
- **Test:** `tests/integration/test_chat_selected.py` — 7 tests:
  - [ ] SC-03: Answerable selection → 200, answer non-empty, no sources field
  - [ ] SC-04: Unanswerable selection → 200, answer == "This question cannot be answered from the selected text alone."
  - [ ] SC-05: Assert retriever mock call_count == 0 (import patch)
  - [ ] SC-07: selected_text length 5001 → 422
  - [ ] SC-15: selected_text with `<script>` → 422
  - [ ] Rate limit: 11th request → 429
  - [ ] session_id returned in response and matches across follow-up

### T-025 — Verify retrieval bypass in integration
- [ ] In `test_chat_selected.py`, patch `app.services.retriever.retrieve` and assert it is never called during `/api/chat-selected` request
- **Test:** `mock_retriever.call_count == 0` assertion in each test case

---

## Phase 5 — /api/ingest Endpoint
**Gate:** SC-11, SC-12, SC-13 pass

### T-026 — Create `app/routes/ingest.py`
- [ ] `@router.post("/ingest", response_model=IngestResponse)`
- [ ] Require `Depends(verify_ingest_key)`
- [ ] Accept `IngestRequest`
- [ ] If `clear_collection=True`: delete Qdrant collection + recreate + clear `ingested_chunks` table
- [ ] If `github_repo_url` provided: call `github_fetcher.fetch_docs()` → list of files → convert to sources
- [ ] For each source: `chunker.chunk_document()` → list of chunks
- [ ] For each chunk: check `ingested_chunks` table by `content_hash` → skip if exists
- [ ] Batch new chunks: `embedder.embed_texts()` → vectors
- [ ] Qdrant upsert each new chunk with point_id = UUID, vector, payload
- [ ] Insert `content_hash` into `ingested_chunks`
- [ ] Return `IngestResponse`
- **Test:** `tests/integration/test_ingest.py` — 6 tests:
  - [ ] SC-11: Valid payload → 200, chunks_stored > 0
  - [ ] SC-12: Re-ingest same content → chunks_stored=0, skipped_duplicates > 0
  - [ ] SC-13: New content ingested → subsequent /api/chat query finds it
  - [ ] SC-14: Missing X-API-Key → 401
  - [ ] SC-15: Malformed payload (no sources, no github_repo_url) → 422
  - [ ] clear_collection=True → Qdrant collection recreated (mock asserts delete called)

### T-027 — GitHub fetch integration
- [ ] Integration test: mock httpx, provide a github_repo_url, assert `fetch_docs` is called and returned files are chunked
- **Test:** Extend `test_ingest.py` with github_repo_url scenario

---

## Phase 6 — /api/health + Session Logging + Log Purge
**Gate:** SC-10 passes; logs visible in Neon

### T-028 — Create `app/routes/health.py`
- [ ] `@router.get("/health", response_model=HealthResponse)`
- [ ] No auth, no rate limit
- [ ] Check Qdrant: call `ping_qdrant(qdrant_client)` → "ok" or "error"
- [ ] Check DB: `SELECT 1` query on asyncpg pool → "ok" or "error"
- [ ] Set `status = "healthy"` if both ok, else `"degraded"`
- [ ] Return `HealthResponse` with version from settings, uptime_seconds from `time.time() - app.state.start_time`
- **Test:** `tests/integration/test_health.py` — 4 tests:
  - [ ] SC-10: Both services up → 200, status=healthy, both=ok
  - [ ] SC-17: Qdrant unreachable → 200, status=degraded, qdrant=error
  - [ ] SC-18: No auth header required
  - [ ] SC-19: Response time ≤ 500ms (assert `latency < 0.5` in test)

### T-029 — Session history in Neon (`postgres.py` additions)
- [ ] `get_session_history(pool, session_id: UUID) -> list[Message]`
  - SELECT last 10 rows from `sessions` WHERE session_id = $1 ORDER BY created_at DESC LIMIT 10
- [ ] `save_session_messages(pool, session_id: UUID, user_msg: str, assistant_msg: str)`
  - INSERT two rows (role=user, role=assistant) in one transaction
- [ ] `expire_old_sessions(pool)` — DELETE FROM sessions WHERE created_at < NOW() - INTERVAL '24 hours'
- **Test:** Unit tests mock asyncpg; assert correct parameterized SQL called

### T-030 — Request log write + 7-day purge
- [ ] `log_request(pool, endpoint, session_id, query, tokens, latency_ms, status_code)`
  - Hashes query with SHA-256; inserts into `request_logs`
- [ ] `purge_old_logs(pool)` — DELETE FROM request_logs WHERE created_at < NOW() - INTERVAL '7 days'
- [ ] Call `purge_old_logs` in startup event (runs once on cold start)
- **Test:** Unit test asserts query stored as hash (not plaintext); assert DELETE query uses parameterized interval

---

## Phase 7 — CI/CD + Deploy + README
**Gate:** All 15 SCs pass in CI; live Render URL accessible

### T-031 — Create `.github/workflows/ci.yml`
- [ ] Trigger: `push` to any branch + `pull_request` targeting `main`
- [ ] Jobs:
  ```yaml
  lint:     black . --check && flake8 app/ tests/
  typecheck: mypy app/ --strict
  test:     pytest --cov=app --cov-report=xml --cov-fail-under=80
  deploy:   [main branch only] curl Render deploy hook URL
  ```
- [ ] All jobs run on `ubuntu-latest`, Python 3.11
- [ ] `test` job uploads coverage report as artifact
- **Test:** Push to branch; confirm all 3 gates pass in GitHub Actions

### T-032 — Create `render.yaml` (Render IaC)
- [ ] Define web service: runtime=python, buildCommand=`pip install -r requirements.txt`, startCommand=`uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Reference all env vars (Render will prompt for values on first deploy)
- **Test:** `render.yaml` valid YAML; Render accepts on first deploy

### T-033 — Create `README.md`
- [ ] Sections: Overview, Local Setup, Environment Variables table, API Reference (4 endpoints with request/response examples), Running Tests, Deploying to Render, Project Structure
- [ ] Include example `curl` commands for all 4 endpoints
- **Test:** README renders correctly on GitHub; all curl examples produce valid JSON when run against local server

### T-034 — Create `.gitignore`
- [ ] Exclude: `.env`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `htmlcov/`, `*.egg-info/`, `.coverage`
- **Test:** `git status` after `make test` shows no cache files tracked

### T-035 — Full integration smoke test (all 15 SCs)
- [ ] SC-01 ✅ ROS 2 query → answer + sources
- [ ] SC-02 ✅ Off-topic query → scope disclaimer
- [ ] SC-03 ✅ Answerable selection → answer from selection
- [ ] SC-04 ✅ Unanswerable selection → cannot-answer message
- [ ] SC-05 ✅ retriever mock call_count == 0 in /api/chat-selected
- [ ] SC-06 ✅ query 1001 chars → 422
- [ ] SC-07 ✅ selected_text 5001 chars → 422
- [ ] SC-08 ✅ empty query → 422
- [ ] SC-09 ✅ 11th request → 429 + Retry-After
- [ ] SC-10 ✅ health → healthy
- [ ] SC-11 ✅ ingest valid → chunks_stored > 0
- [ ] SC-12 ✅ re-ingest → skipped_duplicates > 0
- [ ] SC-13 ✅ new chapter queryable after ingest
- [ ] SC-14 ✅ ingest without key → 401
- [ ] SC-15 ✅ HTML in input → 422
- **Test:** `pytest tests/integration/ -v` — all 15 pass

### T-036 — Deploy to Render + verify live URL
- [ ] Push `main` to GitHub → CI/CD triggers → Render deploys
- [ ] Verify: `curl https://<your-render-url>/api/health` → `{ "status": "healthy" }`
- [ ] Run SC-01 curl against live URL
- **Test:** HTTP 200 from live Render URL on `/api/health`

---

## Task Summary

| Phase | Tasks | Key Gate |
|-------|-------|---------|
| 1 — Scaffold | T-001 to T-012 | `make dev` starts, `/api/health` responds |
| 2 — Services | T-013 to T-021 | Unit tests green, 80%+ coverage |
| 3 — /api/chat | T-022 to T-023 | SC-01, SC-02 pass |
| 4 — /api/chat-selected | T-024 to T-025 | SC-03, SC-04, SC-05 pass |
| 5 — /api/ingest | T-026 to T-027 | SC-11, SC-12, SC-13 pass |
| 6 — Health + Logging | T-028 to T-030 | SC-10 pass, logs in Neon |
| 7 — CI/CD + Deploy | T-031 to T-036 | All 15 SCs pass in CI, live URL up |

**Total: 36 task items × avg 2 sub-tasks = ~72 test-backed deliverables**
