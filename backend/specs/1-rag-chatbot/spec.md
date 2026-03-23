# Feature Spec — 1-rag-chatbot
version: 1.0.0
date: 2026-03-06
author: Ismat Zehra
feature: 1-rag-chatbot
status: draft

---

## 1. Overview

Build the backend API for an interactive RAG chatbot embedded in a Docusaurus textbook website teaching **Physical AI & Humanoid Robotics** (Panaversity hackathon project).

The chatbot provides accurate answers **strictly grounded in the textbook content only** — no hallucination, no outside knowledge. It supports two query modes: full RAG retrieval and selected-text isolation. A maintainer endpoint handles ingestion of Markdown content from the Docusaurus `docs/` tree.

---

## 2. User Stories

### US-01 — General Textbook Query
**As a reader**, I can ask any question about the textbook content and receive a concise, accurate response with clear references to the relevant chapter/module/section.

**Covered topics:** ROS 2 nodes/topics/services, Gazebo simulation, NVIDIA Isaac platform, Vision-Language-Action (VLA) models, hardware (RTX GPUs, Jetson Orin Nano, Intel RealSense, Unitree robots), weekly modules, learning outcomes, capstone project.

**Acceptance criteria:**
- [ ] AC-01: Asking "Explain ROS 2 nodes and topics" returns a correct explanation sourced from the ROS 2 module with chapter/section references.
- [ ] AC-02: Asking "What GPU is required for the Isaac platform?" returns the correct hardware spec from the relevant chapter.
- [ ] AC-03: Asking a question entirely unrelated to the textbook returns: `"I can only answer questions based on the Physical AI & Humanoid Robotics textbook content."`
- [ ] AC-04: Response JSON contains `answer` (string) and `sources` (list of `{ chapter, section, slug }` objects).
- [ ] AC-05: p95 latency ≤ 5 seconds end-to-end.

---

### US-02 — Selected-Text Query
**As a reader who has highlighted a specific paragraph or block of text**, I can ask a question about that selection and get an answer that uses **ONLY the selected text as context**.

**Key invariant:** If the question cannot be answered from the selected text, the system returns a clear "cannot answer from selection" message — it never adds outside information or guesses.

**Acceptance criteria:**
- [ ] AC-06: Highlighting a paragraph about Jetson Orin Nano and asking "What sensors does it support?" returns an answer sourced only from that paragraph.
- [ ] AC-07: Asking "What is the capital of France?" against any selection returns: `"This question cannot be answered from the selected text alone."`
- [ ] AC-08: Vector retrieval is provably NOT called in this endpoint (assert in tests via mock call count = 0).
- [ ] AC-09: `selected_text` > 5000 chars returns HTTP 422 with validation error message.
- [ ] AC-10: Response JSON contains `answer` (string) and `session_id` (string). No `sources` field (context is the selection itself).

---

### US-03 — Content Ingestion
**As a maintainer**, I can trigger ingestion of all textbook Markdown files from the Docusaurus `docs/` structure so that content becomes searchable and usable by the chatbot.

**Ingestion behavior:**
- Accepts a list of file paths or a base URL pointing to Docusaurus docs
- Chunks content by heading boundaries (H2 / H3 level)
- Embeds each chunk with `text-embedding-ada-002` (1536 dimensions)
- Stores vectors in Qdrant collection `ai-native-book` with metadata: `{ chapter, section, slug, source_url, chunk_index }`
- Content-hash deduplication: skip re-embedding chunks with identical hash
- Supports full re-ingestion by clearing and rebuilding the collection

**Acceptance criteria:**
- [ ] AC-11: POST `/api/ingest` with valid payload returns `{ status: "ok", chunks_stored: N, skipped_duplicates: M, collection: "ai-native-book" }`.
- [ ] AC-12: Re-ingesting same content stores 0 new chunks (all skipped as duplicates).
- [ ] AC-13: After ingesting a new chapter, querying a detail from that chapter returns a correct answer within the same session.
- [ ] AC-14: Missing required auth header returns HTTP 401.
- [ ] AC-15: Ingestion with malformed payload returns HTTP 422.

---

### US-04 — Health Check
**As a frontend developer or DevOps engineer**, I can call `GET /api/health` to verify the service and all dependencies are operational.

**Acceptance criteria:**
- [ ] AC-16: Returns `{ status: "healthy", version: "1.0.0", qdrant: "ok", db: "ok" }` when all services are up.
- [ ] AC-17: Returns `{ status: "degraded", qdrant: "error", db: "ok" }` (HTTP 200) when Qdrant is unreachable.
- [ ] AC-18: No authentication required.
- [ ] AC-19: Response time ≤ 500ms.

---

## 3. Functional Requirements

### FR-01 — RAG Pipeline (General Chat)
The `/api/chat` endpoint executes this pipeline in sequence:
1. **Embed query** — call `text-embedding-ada-002` to get 1536-dim query vector
2. **Retrieve** — query Qdrant `ai-native-book` collection, `top_k=5` nearest neighbors (cosine similarity)
3. **Augment** — construct system prompt:
   ```
   You are a teaching assistant for the Physical AI & Humanoid Robotics textbook.
   Answer ONLY based on the provided context. If the context does not contain enough
   information to answer the question, say so clearly. Do not use outside knowledge.

   Context:
   [retrieved chunks with chapter/section labels]
   ```
4. **Generate** — call `gpt-4o-mini` with augmented prompt + user query
5. **Return** — `{ answer, sources, session_id, tokens_used }`

### FR-02 — Selected-Text Pipeline
The `/api/chat-selected` endpoint:
1. **Skip retrieval entirely** — use `selected_text` as sole context
2. **Augment** — construct system prompt:
   ```
   You are a teaching assistant. Answer ONLY based on the following text excerpt.
   If the question cannot be answered from this excerpt, respond with exactly:
   "This question cannot be answered from the selected text alone."

   Excerpt:
   [selected_text]
   ```
3. **Generate** — call `gpt-4o-mini`
4. **Return** — `{ answer, session_id, tokens_used }`

### FR-03 — Chunking Strategy
- Splitter: `RecursiveCharacterTextSplitter` (LangChain)
- Chunk size: 800 tokens, overlap: 100 tokens
- Preserve heading hierarchy: store `chapter` (H1), `section` (H2), `subsection` (H3) as metadata
- Minimum chunk size: 50 tokens (discard shorter fragments)

### FR-04 — Session Continuity
- `session_id` is an optional UUID in request; if absent, server generates one
- Session state stored in Neon Postgres: `(session_id, role, content, created_at)`
- Last 10 exchanges included in context window for conversational continuity
- Sessions expire after 24 hours (TTL enforced by DELETE query on access)

### FR-05 — Source References
- Every `/api/chat` response includes `sources`: list of chunks used, each with:
  - `chapter`: chapter title
  - `section`: section heading
  - `slug`: Docusaurus URL slug (e.g., `week-3/ros2-nodes`)
  - `relevance_score`: cosine similarity (0–1, 2 decimal places)
- Sources sorted by relevance_score descending

### FR-06 — Error Responses
All errors return `{ error: string, code: string, detail?: string }`:

| HTTP | code | Trigger |
|------|------|---------|
| 400 | BAD_REQUEST | Malformed JSON body |
| 401 | UNAUTHORIZED | Missing/invalid X-API-Key on /api/ingest |
| 422 | VALIDATION_ERROR | Pydantic constraint violation |
| 429 | RATE_LIMITED | > 10 req/min/IP |
| 500 | INTERNAL_ERROR | Unhandled exception |
| 503 | SERVICE_UNAVAILABLE | OpenAI or Qdrant unreachable |

### FR-07 — Rate Limiting
- 10 requests/minute per remote IP on `/api/chat` and `/api/chat-selected`
- Uses `slowapi` with `Limiter(key_func=get_remote_address)`
- Response headers: `X-RateLimit-Limit: 10`, `X-RateLimit-Remaining: N`, `Retry-After: 60`

### FR-08 — Input Sanitization
- Strip leading/trailing whitespace from all string fields
- Reject inputs containing HTML `<script>`, `<img>`, `<iframe>` tags → HTTP 422
- `query`: min 1 char, max 1000 chars
- `selected_text`: min 10 chars, max 5000 chars
- `top_k`: integer 1–20, default 5

### FR-09 — Request/Response Logging
Every request to `/api/chat` and `/api/chat-selected` logged to Neon Postgres table `request_logs`:
```sql
CREATE TABLE request_logs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  endpoint    TEXT NOT NULL,
  session_id  UUID,
  query_hash  TEXT NOT NULL,   -- SHA-256 of query (not plaintext)
  tokens_used INT,
  latency_ms  INT,
  status_code INT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
```
- No PII stored (query stored as hash only)
- Auto-delete rows older than 7 days (pg_cron or application-level cleanup)

### FR-10 — Future Extension Hooks (non-blocking stubs)
- `user_background` optional field in request models (stored but not yet used)
- `language` optional field: `"en"` (default) | `"ur"` — if `"ur"`, placeholder response "Urdu translation coming soon"
- These are **non-functional stubs** in v1 — included in request models but not implemented

---

## 4. Non-Functional Requirements

| NFR | Requirement |
|-----|-------------|
| NFR-01 Latency | p95 end-to-end ≤ 5s for `/api/chat`; ≤ 3s for `/api/chat-selected` (no retrieval) |
| NFR-02 Throughput | Handle 50 concurrent users on Render free tier (1 CPU, 512MB RAM) |
| NFR-03 Availability | 99% uptime (Render free tier SLA; acceptable cold-start delay ≤ 30s) |
| NFR-04 Cost | $0 infrastructure: Qdrant Cloud Free + Neon Free + Render Free |
| NFR-05 Security | OWASP Top 10; no secrets in code; HTTPS enforced; no wildcard CORS |
| NFR-06 Observability | All requests logged; /api/health exposes dependency status |
| NFR-07 Maintainability | 80%+ test coverage; Black/Flake8/Mypy CI gates |
| NFR-08 Scalability | Stateless FastAPI; horizontal scale possible (Neon + Qdrant are external) |

---

## 5. API Contracts

### POST /api/ingest
```json
// Request
{
  "sources": [
    {
      "text": "string (markdown content)",
      "metadata": {
        "chapter": "string",
        "section": "string",
        "slug": "string",
        "source_url": "string | null"
      }
    }
  ],
  "clear_collection": false
}

// Response 200
{
  "status": "ok",
  "chunks_stored": 42,
  "skipped_duplicates": 8,
  "collection": "ai-native-book"
}
```
**Headers:** `X-API-Key: <INGEST_API_KEY>` (required)

---

### POST /api/chat
```json
// Request
{
  "query": "string (1–1000 chars)",
  "session_id": "uuid | null",
  "top_k": 5,
  "user_background": "string | null",
  "language": "en | ur"
}

// Response 200
{
  "answer": "string",
  "sources": [
    {
      "chapter": "string",
      "section": "string",
      "slug": "string",
      "relevance_score": 0.87
    }
  ],
  "session_id": "uuid",
  "tokens_used": 512
}
```

---

### POST /api/chat-selected
```json
// Request
{
  "query": "string (1–1000 chars)",
  "selected_text": "string (10–5000 chars)",
  "session_id": "uuid | null",
  "language": "en | ur"
}

// Response 200
{
  "answer": "string",
  "session_id": "uuid",
  "tokens_used": 256
}
```

---

### GET /api/health
```json
// Response 200
{
  "status": "healthy | degraded",
  "version": "1.0.0",
  "qdrant": "ok | error",
  "db": "ok | error",
  "uptime_seconds": 3600
}
```

---

## 6. Success Criteria (Acceptance Tests)

| ID | Scenario | Expected |
|----|---------|---------|
| SC-01 | POST /api/chat with "Explain ROS 2 nodes" | 200, answer contains ROS 2 explanation, sources ≥ 1 |
| SC-02 | POST /api/chat with off-topic query | 200, answer = textbook-scope disclaimer |
| SC-03 | POST /api/chat-selected, question answerable from selection | 200, answer grounded in selection |
| SC-04 | POST /api/chat-selected, question not answerable from selection | 200, answer = "This question cannot be answered from the selected text alone." |
| SC-05 | POST /api/chat-selected — assert retriever mock call count = 0 | Retrieval bypassed |
| SC-06 | POST /api/chat — query length 1001 chars | 422 VALIDATION_ERROR |
| SC-07 | POST /api/chat-selected — selected_text length 5001 chars | 422 VALIDATION_ERROR |
| SC-08 | POST /api/chat — empty query `""` | 422 VALIDATION_ERROR |
| SC-09 | 11 requests in 1 minute from same IP | 11th returns 429 + Retry-After: 60 |
| SC-10 | GET /api/health when all services up | 200, status=healthy, qdrant=ok, db=ok |
| SC-11 | POST /api/ingest without X-API-Key | 401 UNAUTHORIZED |
| SC-12 | POST /api/ingest with valid payload | 200, chunks_stored > 0 |
| SC-13 | Re-ingest same content | 200, chunks_stored = 0, skipped_duplicates > 0 |
| SC-14 | Query detail from newly ingested chapter | 200, correct answer, sources reference new chapter |
| SC-15 | selected_text with `<script>` tag | 422 VALIDATION_ERROR (sanitization) |

---

## 7. Non-Goals (v1)

- **No user authentication** — chatbot is open to all readers; only `/api/ingest` requires API key
- **No Urdu translation** — `language: "ur"` returns stub response
- **No user-background personalization** — field accepted but ignored
- **No streaming responses** — single JSON response (no SSE / WebSocket)
- **No admin dashboard** — ingestion triggered manually via API call
- **No image/diagram content** — text-only ingestion; embedded diagrams ignored
- **No multi-book support** — single Qdrant collection `ai-native-book`
- **No frontend** — this spec covers the backend API only

---

## 8. Open Questions

| # | Question | Owner | Status |
|---|---------|-------|--------|
| OQ-01 | Will the Docusaurus docs be in a public GitHub repo for ingestion, or pushed via API? | Ismat | Open |
| OQ-02 | Should session history persist across browser sessions or be ephemeral per tab? | Ismat | Open |
| OQ-03 | Is there a word limit for the chatbot's answer (e.g., max 300 words)? | Ismat | Open |
| OQ-04 | Should `/api/ingest` also accept a GitHub URL and pull files directly? | Ismat | Open |
