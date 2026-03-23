---
id: topic-02
title: "Data Pipelines and Model Integration"
sidebar_label: "Data Pipelines"
---

## Data Pipelines and Model Integration

Raw data flows through ingestion, chunking, embedding, vector storage, retrieval, and into the model. Each layer has failure modes. Your pipeline is only as reliable as its weakest link.

### Embedding Pipelines and Vector Stores

Embeddings convert text to vectors capturing semantic meaning.

| Store | Best For | Scale |
|---|---|---|
| **pgvector** | PostgreSQL shops | < 1M vectors |
| **Qdrant** | Production, high performance | Millions of vectors |
| **Chroma** | Development, local | Small-medium |

Start with pgvector and migrate only when proven necessary.

### Chunking Strategy

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,   # 20% overlap
    length_function=tiktoken_len,
)
chunks = splitter.split_text(document)
```

Good chunking preserves semantic units. Bad chunking cuts sentences mid-thought, destroying retrieval quality.

### Typed Function Calls (Tool Use)

Tool use bridges the AI text world and your typed application world.

```python
tools = [{
    "name": "search_textbook",
    "description": "Search the Physical AI textbook for relevant content",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "chapter": {"type": "integer", "minimum": 1, "maximum": 5}
        },
        "required": ["query"]
    }
}]
```

### Streaming for User Experience

Always stream responses longer than a sentence. A 3-second wait for a complete response feels broken. The same 3 seconds with text streaming in feels fast.

```python
with client.messages.stream(
    model="claude-opus-4-6",
    messages=messages,
    max_tokens=1024,
) as stream:
    for text in stream.text_stream:
        yield text  # Send chunk to client immediately
```

Streaming is non-negotiable for production user experience.
