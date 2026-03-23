---
id: topic-01
title: "Architecture Patterns for AI-Native Apps"
sidebar_label: "Architecture Patterns"
---

## Architecture Patterns for AI-Native Apps

Four foundational patterns power every production AI-Native system.

### Pattern 1: Retrieval-Augmented Generation (RAG)

RAG retrieves relevant context from your data and injects it into the prompt. Use RAG when your product has proprietary knowledge the model lacks, when you need citations, or when fine-tuning is not feasible.

```python
# RAG pipeline overview
query_vector = embedder.embed(user_query)
chunks = qdrant.search(query_vector, top_k=5)
context = "\n\n".join(chunk.text for chunk in chunks)
answer = llm.generate(system=f"Context:\n{context}", user=user_query)
```

**When to use RAG:**
- Proprietary knowledge the model lacks (e.g., your textbook content)
- Need citations and source references
- Fine-tuning is too expensive or slow

Start with 512-token chunks and 20% overlap, then tune based on retrieval quality metrics.

### Pattern 2: Agent Loops

Agent loops let the AI take actions, observe results, and decide next steps.

```python
while True:
    response = llm.create(tools=tools, messages=messages)
    if response.stop_reason == "end_turn":
        break
    # Execute tool calls, feed results back
    tool_results = execute_tools(response.tool_calls)
    messages.append(tool_results)
```

**Rules for production agents:**
- Define stop conditions to prevent runaway execution
- Require human approval for irreversible actions
- Give agents minimum permissions (least privilege)
- Log every tool call with inputs, outputs, and timestamps

### Pattern 3: Structured Output

Force the model to produce JSON your application can parse reliably.

```python
from pydantic import BaseModel

class ChapterSummary(BaseModel):
    title: str
    key_points: list[str]
    difficulty: str

response = client.messages.parse(
    model="claude-opus-4-6",
    output_config={"format": ChapterSummary.model_json_schema()},
    messages=[{"role": "user", "content": "Summarise Chapter 1"}]
)
```

### Pattern 4: The Evaluation-Feedback Loop

Production traffic → Evaluation → Metrics → Prompt improvement → Repeat.

Build evaluation infrastructure **before** optimising prompts. Teams that run this loop rigorously see quality compound over months.

:::info Architecture decision
For this textbook, we use RAG (Qdrant + Cohere embeddings) for the chatbot and structured output (Pydantic) for the agent skills. Both patterns are live at `/api/chat` and `/api/agent`.
:::
