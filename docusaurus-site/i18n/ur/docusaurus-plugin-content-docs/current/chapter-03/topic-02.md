---
id: topic-02
title: "ڈیٹا پائپ لائنز اور ماڈل انٹیگریشن"
sidebar_label: "ڈیٹا پائپ لائنز"
---

## ڈیٹا پائپ لائنز اور ماڈل انٹیگریشن

خام ڈیٹا ingestion، chunking، embedding، vector storage، retrieval، اور ماڈل میں بہتا ہے۔ ہر تہہ میں ناکامی کی موڈز ہیں۔ آپ کی پائپ لائن صرف اس کے کمزور ترین لنک جتنی قابل اعتماد ہے۔

### Embedding پائپ لائنز اور Vector Stores

Embeddings ٹیکسٹ کو vectors میں تبدیل کرتی ہیں جو معنوی معنی کو پکڑتی ہیں۔

| Store | بہترین کے لیے | پیمانہ |
|---|---|---|
| **pgvector** | PostgreSQL دکانیں | < 1M vectors |
| **Qdrant** | پروڈکشن، اعلی کارکردگی | لاکھوں vectors |
| **Chroma** | ترقی، لوکل | چھوٹا-درمیانہ |

pgvector کے ساتھ شروع کریں اور صرف اس وقت منتقل کریں جب ثابت ہو کہ ضروری ہے۔

### Chunking حکمت عملی

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,   # 20% overlap
    length_function=tiktoken_len,
)
chunks = splitter.split_text(document)
```

اچھا chunking معنوی اکائیوں کو محفوظ رکھتا ہے۔ برا chunking جملوں کو درمیانِ فکر کاٹتا ہے، retrieval کے معیار کو تباہ کرتا ہے۔

### Typed Function Calls (ٹول استعمال)

ٹول استعمال AI کی ٹیکسٹ دنیا اور آپ کی typed ایپلیکیشن دنیا کو جوڑتا ہے۔

```python
tools = [{
    "name": "search_textbook",
    "description": "طبیعی AI کی کتاب میں متعلقہ مواد تلاش کریں",
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

### صارف کے تجربے کے لیے Streaming

ہمیشہ ایک جملے سے لمبے responses کو stream کریں۔ مکمل response کے لیے 3 سیکنڈ کا انتظار ٹوٹا ہوا محسوس ہوتا ہے۔ ٹیکسٹ streaming میں اسی 3 سیکنڈ کو تیز محسوس ہوتا ہے۔

```python
with client.messages.stream(
    model="claude-opus-4-6",
    messages=messages,
    max_tokens=1024,
) as stream:
    for text in stream.text_stream:
        yield text  # فوراً کلائنٹ کو chunk بھیجیں
```

پروڈکشن صارف کے تجربے کے لیے streaming غیر مذاکراتی ہے۔
