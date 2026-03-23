---
id: topic-02
title: "ڈیٹا پائپ لائنز اور ماڈل انضمام"
sidebar_label: "ڈیٹا پائپ لائنز"
---

## ڈیٹا پائپ لائنز اور ماڈل انضمام

خام ڈیٹا ingestion، chunking، embedding، ویکٹر اسٹوریج، retrieval سے گزر کر ماڈل میں جاتا ہے۔ ہر پرت میں ناکامی کے طریقے ہیں۔ آپ کی پائپ لائن صرف اتنی ہی قابل اعتماد ہے جتنی اس کی سب سے کمزور کڑی۔

### Embedding پائپ لائنز اور ویکٹر اسٹورز

Embeddings متن کو ایسے vectors میں تبدیل کرتے ہیں جو معنوی مفہوم کو پکڑتے ہیں۔

| اسٹور | بہترین استعمال | پیمانہ |
|---|---|---|
| **pgvector** | PostgreSQL دکانیں | < 1M vectors |
| **Qdrant** | پروڈکشن، اعلی کارکردگی | لاکھوں vectors |
| **Chroma** | ترقی، مقامی | چھوٹا-درمیانہ |

pgvector سے شروع کریں اور صرف اس وقت منتقل ہوں جب ثابت ضروری ہو۔

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

اچھی chunking معنوی اکائیوں کو محفوظ رکھتی ہے۔ خراب chunking جملوں کو درمیان میں کاٹتی ہے، retrieval معیار کو تباہ کرتی ہے۔

### ٹائپ شدہ فنکشن کالز (Tool Use)

Tool use AI کی متنی دنیا اور آپ کی ٹائپ شدہ ایپلیکیشن دنیا کے درمیان پل بناتا ہے۔

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

### صارف تجربے کے لیے Streaming

ایک جملے سے لمبے جوابات ہمیشہ stream کریں۔ مکمل جواب کے لیے ۳ سیکنڈ کا انتظار ٹوٹا ہوا لگتا ہے۔ وہی ۳ سیکنڈ متن streaming میں آتے ہوئے تیز لگتے ہیں۔

```python
with client.messages.stream(
    model="claude-opus-4-6",
    messages=messages,
    max_tokens=1024,
) as stream:
    for text in stream.text_stream:
        yield text  # Send chunk to client immediately
```

Streaming پروڈکشن صارف تجربے کے لیے ناگزیر ہے۔
