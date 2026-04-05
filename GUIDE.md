# AI-Native Book Project — Complete Guide

Welcome to the **AI-Native Driven Development** project! This guide covers everything you need to know to set up, run, and contribute to the project.

---

## 📚 Project Overview

This is a comprehensive educational platform consisting of:

1. **Frontend (Docusaurus)** — A modern documentation website for the AI-Native & Physical AI textbook
2. **Backend (FastAPI)** — A RAG (Retrieval-Augmented Generation) chatbot that answers questions about the textbook content
3. **Full-stack integration** — Frontend displays content, backend provides AI-powered Q&A

---

## 🗂️ Project Structure

```
ai-native-book/
├── frontend/              # Next.js/Docusaurus frontend
├── backend/               # FastAPI RAG chatbot backend
├── backend-1/             # Alternative backend version
├── docusaurus-site/       # Main documentation site (active frontend)
├── specs/                 # Feature specifications
├── history/               # Project history (PHRs, ADRs)
├── .specify/              # Spec-driven development templates
└── package.json           # Root dependencies
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** >= 20.0 (for frontend)
- **Python** >= 3.10 (for backend)
- **Git** for version control

### 1️⃣ Frontend Setup (Docusaurus Site)

The main documentation site runs on Docusaurus.

```bash
# Navigate to the docusaurus site
cd docusaurus-site

# Install dependencies
npm install

# Start development server
npm start
# or: npm run start

# Site will be available at: http://localhost:3000
```

**Available Scripts:**
- `npm start` — Start development server
- `npm run build` — Build for production
- `npm run serve` — Serve production build locally
- `npm run clear` — Clear Docusaurus cache
- `npm run typecheck` — Run TypeScript type checking

### 2️⃣ Backend Setup (FastAPI RAG Chatbot)

The backend provides an AI chatbot that answers questions about the textbook using RAG.

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration

# Start development server
make dev
# or: uvicorn app.main:app --reload --port 8000

# API will be available at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

---

## ⚙️ Environment Variables

### Backend (.env file)

You **must** configure these for the backend to work:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for embeddings (text-embedding-ada-002) and chat (gpt-4o-mini) |
| `QDRANT_URL` | ✅ Yes | Qdrant Cloud cluster URL for vector database |
| `QDRANT_API_KEY` | ✅ Yes | Qdrant Cloud API key |
| `DATABASE_URL` | ✅ Yes | Neon PostgreSQL connection string for session storage |
| `INGEST_API_KEY` | ✅ Yes | Secret key for content ingestion endpoint |
| `CORS_ORIGINS` | Optional | Comma-separated allowed origins (e.g., `http://localhost:3000`) |
| `QDRANT_COLLECTION` | Optional | Collection name (default: `ai-native-book`) |
| `ENVIRONMENT` | Optional | `development` or `production` |
| `GITHUB_TOKEN` | Optional | GitHub token for private repo ingestion |
| `MAX_ANSWER_TOKENS` | Optional | Max tokens in LLM response (default: `400`) |
| `LOG_RETENTION_DAYS` | Optional | Days to retain request logs (default: `7`) |

**Example .env:**
```env
OPENAI_API_KEY=sk-your-openai-key-here
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
DATABASE_URL=postgresql://user:password@host:5432/dbname
INGEST_API_KEY=your-secret-ingest-key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

---

## 📖 Backend API Reference

### Health Check
```bash
GET /api/health
```
Returns service health status, Qdrant connection, and database status.

### Chat Endpoint
```bash
POST /api/chat
Content-Type: application/json

{
  "query": "Explain ROS 2 nodes",
  "top_k": 5
}
```
Ask questions about the textbook. Answers are grounded in actual content.

### Selected Text Chat
```bash
POST /api/chat-selected
Content-Type: application/json

{
  "query": "What does this mean?",
  "selected_text": "The highlighted paragraph..."
}
```
Ask questions about specific highlighted text (no vector search).

### Content Ingestion
```bash
POST /api/ingest
Content-Type: application/json
X-API-Key: your-ingest-key

{
  "github_repo_url": "https://github.com/...",
  "docs_path": "docs"
}
```
Ingest textbook content from GitHub or direct payload into the vector database.

---

## 🧪 Testing

### Frontend
```bash
cd docusaurus-site
npm run build        # Build must pass with zero errors
npm run typecheck    # TypeScript check
```

### Backend
```bash
cd backend

# Run all tests
make test
# or: pytest tests/ -v

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test suites
pytest tests/unit/ -v
pytest tests/integration/ -v
```

---

## 📝 Content Management

### Adding/Editing Documentation

All textbook content lives in the `docusaurus-site/docs/` directory as Markdown/MDX files.

**To add a new chapter:**
1. Create a new `.mdx` file in `docusaurus-site/docs/`
2. Add frontmatter:
   ```markdown
   ---
   sidebar_label: "Chapter Title"
   title: "Full Chapter Title"
   description: "Brief description"
   ---
   ```
3. Write your content in Markdown/MDX
4. Update `sidebars.ts` if needed
5. Run `npm run build` to verify
6. Commit and push

### Ingesting Content into RAG Backend

To make content available for the AI chatbot:

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-ingest-key" \
  -d '{
    "github_repo_url": "https://github.com/your-org/textbook-repo",
    "docs_path": "docs"
  }'
```

Or ingest direct content:
```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-ingest-key" \
  -d '{
    "sources": [
      {
        "text": "## Chapter Title\n\nYour content here...",
        "metadata": {
          "chapter": "Chapter 1",
          "section": "Introduction",
          "slug": "chapter-1/intro"
        }
      }
    ]
  }'
```

---

## 🌐 Deployment

### Frontend (Vercel)

1. Push to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Vercel auto-detects Docusaurus
5. Click **Deploy**
6. Live URL appears in ~2 minutes

### Backend (Render)

1. Push to GitHub
2. Create a Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Render auto-detects `render.yaml`
5. Set all required environment variables in Render dashboard
6. Click **Deploy**

**CI/CD:** Configure `RENDER_DEPLOY_HOOK` in GitHub secrets for automatic deploys on pushes to `main`.

---

## 🔧 Common Commands

### Frontend (Docusaurus)
```bash
cd docusaurus-site
npm start              # Start dev server
npm run build          # Production build
npm run serve          # Serve production build
npm run clear          # Clear cache
npm run typecheck      # TypeScript check
```

### Backend (FastAPI)
```bash
cd backend
make dev               # Start dev server
make test              # Run tests
uvicorn app.main:app --reload --port 8000  # Manual start
```

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem:** `npm install` fails
- **Solution:** Ensure Node.js >= 20.0. Check with `node --version`

**Problem:** Build fails with TypeScript errors
- **Solution:** Run `npm run typecheck` to see detailed errors
- Check `.mdx` files have proper frontmatter

**Problem:** Site not updating after content changes
- **Solution:** Clear cache with `npm run clear` and restart

### Backend Issues

**Problem:** OpenAI API errors
- **Solution:** Verify `OPENAI_API_KEY` is valid and has credits
- Check key format: should start with `sk-`

**Problem:** Qdrant connection failed
- **Solution:** Verify `QDRANT_URL` and `QDRANT_API_KEY`
- Check Qdrant cluster is accessible

**Problem:** Database connection errors
- **Solution:** Verify `DATABASE_URL` format: `postgresql://user:password@host:5432/dbname`
- Ensure Neon database is accessible

**Problem:** Ingestion returns 0 chunks
- **Solution:** Verify Markdown files are properly formatted
- Check `docs_path` is correct relative to repo root

---

## 📊 Architecture

### How RAG Works

1. **Ingestion**: Markdown docs → Chunked → Embedded (OpenAI ADA-002) → Stored in Qdrant vector DB
2. **Query**: User question → Embedded → Similar chunks retrieved from Qdrant
3. **Generation**: Query + retrieved chunks → GPT-4o-mini → Grounded answer
4. **Session**: Last 10 exchanges stored in PostgreSQL for context

### Tech Stack

**Frontend:**
- Docusaurus 3.9.2
- React 19
- TypeScript
- MDX
- Clerk (Authentication)

**Backend:**
- FastAPI (Python)
- OpenAI API (embeddings + chat)
- Qdrant (Vector Database)
- Neon PostgreSQL (Session storage)
- SlowAPI (Rate limiting)

---

## 🔐 Security Best Practices

- ✅ Never commit `.env` files
- ✅ Use `.env.example` to document required variables
- ✅ Keep API keys secret (use environment variables)
- ✅ Set `INGEST_API_KEY` to protect ingestion endpoint
- ✅ Configure `CORS_ORIGINS` to restrict access
- ✅ Use rate limiting (10 req/min per IP)
- ✅ Never hardcode secrets in code

---

## 📚 Additional Resources

- **Docusaurus Docs:** https://docusaurus.io/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Qdrant Docs:** https://qdrant.tech/documentation/
- **OpenAI API:** https://platform.openai.com/docs

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and build
4. Commit with descriptive message
5. Push and create pull request

---

## 📞 Support

If you encounter issues:
1. Check the **Troubleshooting** section above
2. Review backend logs for error messages
3. Verify all environment variables are set correctly
4. Check that all services (Qdrant, PostgreSQL) are running

---

**Happy coding! 🚀**
