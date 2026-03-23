---
id: topic-02
title: "Monitoring, Observability, and Feedback Loops"
sidebar_label: "Monitoring & Observability"
---

## Monitoring, Observability, and Feedback Loops

The four pillars of AI observability:

| Pillar | Metric | Alert When |
|---|---|---|
| **Latency** | p50 / p95 / p99 | p95 > 5s |
| **Cost** | Tokens per call, cost per user | Cost spikes > 2x |
| **Quality** | User feedback rating | Rating drops > 10% |
| **Safety** | Harm score, block rate | Block rate spikes |

### Tracing AI Calls

Trace every AI call end-to-end with structured logging:

```python
import structlog
log = structlog.get_logger()

async def generate_answer(query: str, session_id: str):
    start = time.time()
    result = await llm.generate(query)
    log.info(
        "ai_call_complete",
        session_id=session_id,
        model="claude-opus-4-6",
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens,
        latency_ms=(time.time() - start) * 1000,
    )
    return result
```

Use correlation IDs linking log lines to traces. This makes debugging quality issues possible.

### The User Feedback Flywheel

```
Collect feedback on AI outputs
    ↓
Analyse which outputs receive negative feedback
    ↓
Form hypotheses about prompt changes
    ↓
A/B test new vs old prompts on live traffic
    ↓
Deploy winners → Monitor → Confirm improvement
    ↓
Repeat
```

This flywheel compounds quality over time.

### Prompt Version Management

Treat prompts as code:

```python
PROMPTS = {
    "rag-v1": "Answer ONLY based on the context...",
    "rag-v2": "You are a teaching assistant... Answer ONLY...",
}

# Track per-version quality metrics
metrics = {
    "rag-v1": {"avg_rating": 3.8, "hallucination_rate": 0.04},
    "rag-v2": {"avg_rating": 4.2, "hallucination_rate": 0.01},
}
```

Maintain rollback capability within minutes. Track per-version quality metrics so you always know whether recent changes improved or degraded performance.
