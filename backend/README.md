# AI-Native Book RAG Chatbot Backend

A FastAPI backend providing a Retrieval-Augmented Generation (RAG) chatbot for the **Physical AI & Humanoid Robotics** textbook. Answers are strictly grounded in textbook content — no hallucination, no outside knowledge.

---

## Overview

- **RAG Pipeline**: Embeds queries with `text-embedding-ada-002`, retrieves relevant chunks from Qdrant, generates answers with `gpt-4o-mini`
- **Selected-Text Mode**: Answer questions about a highlighted paragraph without vector retrieval
- **Content Ingestion**: Ingest Markdown docs from GitHub or direct payload with deduplication
- **Session Continuity**: Last 10 exchanges stored in Neon Postgres per session
- **Rate Limiting**: 10 requests/minute per IP via slowapi

---

## Quick Start

```bash
# 1. Clone and enter directory
git clone <repo-url>
cd ai-native-book-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 4. Copy and fill environment variables
cp .env.example .env
# Edit .env with your actual values

# 5. Start development server
make dev
# or: uvicorn app.main:app --reload --port 8000
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for embeddings and chat |
| `QDRANT_URL` | Yes | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant Cloud API key |
| `QDRANT_COLLECTION` | No | Collection name (default: `ai-native-book`) |
| `DATABASE_URL` | Yes | Neon Postgres connection string |
| `INGEST_API_KEY` | Yes | Secret key for `/api/ingest` endpoint |
| `CORS_ORIGINS` | No | Comma-separated allowed origins |
| `ENVIRONMENT` | No | `development` or `production` |
| `GITHUB_TOKEN` | No | GitHub token for private repo ingestion |
| `MAX_ANSWER_TOKENS` | No | Max tokens in LLM response (default: `400`) |
| `LOG_RETENTION_DAYS` | No | Days to retain request logs (default: `7`) |

---

## API Reference

### GET /api/health

Check service health. No authentication required.

```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "qdrant": "ok",
  "db": "ok",
  "uptime_seconds": 3600
}
```

---

### POST /api/chat

Ask a question about the textbook content.

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain ROS 2 nodes and topics",
    "top_k": 5
  }'
```

Response:
```json
{
  "answer": "ROS 2 nodes are independent processes that communicate via topics...",
  "sources": [
    {
      "chapter": "Week 3",
      "section": "ROS 2 Nodes",
      "slug": "week-3/ros2-nodes",
      "relevance_score": 0.95
    }
  ],
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "tokens_used": 312
}
```

---

### POST /api/chat-selected

Ask a question about highlighted/selected text only. No vector retrieval is performed.

```bash
curl -X POST http://localhost:8000/api/chat-selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What sensors does it support?",
    "selected_text": "The Jetson Orin Nano supports Intel RealSense depth cameras and USB cameras for vision tasks."
  }'
```

Response:
```json
{
  "answer": "According to the text, the Jetson Orin Nano supports Intel RealSense depth cameras and USB cameras.",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "tokens_used": 85
}
```

---

### POST /api/ingest

Ingest textbook Markdown content. Requires `X-API-Key` header.

```bash
# Ingest from GitHub
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-ingest-key" \
  -d '{
    "github_repo_url": "https://github.com/panaversity/physical-ai-book",
    "docs_path": "docs"
  }'

# Ingest direct content
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-ingest-key" \
  -d '{
    "sources": [
      {
        "text": "## ROS 2 Nodes\n\nROS 2 nodes are independent processes...",
        "metadata": {
          "chapter": "Week 3",
          "section": "ROS 2 Nodes",
          "slug": "week-3/ros2-nodes"
        }
      }
    ]
  }'
```

Response:
```json
{
  "status": "ok",
  "chunks_stored": 42,
  "skipped_duplicates": 8,
  "collection": "ai-native-book"
}
```

---

## Running Tests

```bash
# Run all tests with coverage
make test

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run with coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing
```

---

## Deploying to Render

1. Push code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` and configure the service
5. Set all required environment variables in the Render dashboard
6. Deploy — CI/CD will auto-deploy on pushes to `main`

Alternatively, set up the `RENDER_DEPLOY_HOOK` secret in GitHub for automatic deploys via CI.

---

## Project Structure

```
ai-native-book-backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Pydantic settings
│   ├── dependencies.py        # FastAPI dependencies + rate limiter
│   ├── main.py                # FastAPI app factory
│   ├── db/
│   │   ├── postgres.py        # asyncpg pool + schema + queries
│   │   └── qdrant.py          # Qdrant client + collection management
│   ├── models/
│   │   ├── requests.py        # Pydantic request models with validation
│   │   └── responses.py       # Pydantic response models
│   ├── routes/
│   │   ├── chat.py            # POST /api/chat
│   │   ├── chat_selected.py   # POST /api/chat-selected
│   │   ├── health.py          # GET /api/health
│   │   └── ingest.py          # POST /api/ingest
│   └── services/
│       ├── chunker.py         # RecursiveCharacterTextSplitter + tiktoken
│       ├── embedder.py        # OpenAI text-embedding-ada-002
│       ├── generator.py       # OpenAI gpt-4o-mini
│       ├── github_fetcher.py  # GitHub API doc fetcher
│       ├── rag_pipeline.py    # Full RAG orchestration
│       ├── retriever.py       # Qdrant vector search
│       └── selected_pipeline.py  # Selected-text pipeline (no retrieval)
├── tests/
│   ├── conftest.py
│   ├── unit/                  # Unit tests for services
│   └── integration/           # Integration tests for API endpoints
├── .env.example
├── .github/workflows/ci.yml
├── Makefile
├── pyproject.toml
├── render.yaml
├── requirements.txt
└── requirements-dev.txt
```
