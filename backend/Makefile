.PHONY: dev test lint typecheck format db-init ingest

dev:
	uvicorn app.main:app --reload --port 8000

test:
	pytest --cov=app --cov-report=term-missing --cov-fail-under=70

lint:
	black . --check && flake8 app/ tests/

typecheck:
	mypy app/ --ignore-missing-imports

format:
	black .

db-init:
	python -c "import asyncio; from app.db.postgres import create_pool, init_schema; pool = asyncio.run(create_pool()); asyncio.run(init_schema(pool))"

ingest:
	curl -X POST http://localhost:8000/api/ingest \
		-H "Content-Type: application/json" \
		-H "X-API-Key: $${INGEST_API_KEY}" \
		-d '{"github_repo_url": "https://github.com/panaversity/learn-applied-generative-ai-fundamentals", "docs_path": "docs"}'
