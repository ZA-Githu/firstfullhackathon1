---
id: topic-01
title: "AI-Native ایپس کے آرکیٹیکچر پیٹرن"
sidebar_label: "آرکیٹیکچر پیٹرن"
---

## AI-Native ایپس کے آرکیٹیکچر پیٹرن

چار بنیادی پیٹرن ہر پروڈکشن AI-Native نظام کو طاقت دیتے ہیں۔

### پیٹرن ۱: Retrieval-Augmented Generation (RAG)

RAG آپ کے ڈیٹا سے متعلقہ سیاق و سباق حاصل کرتا ہے اور اسے prompt میں داخل کرتا ہے۔ RAG استعمال کریں جب آپ کے پروڈکٹ میں ایسا خاصی معلومات ہو جو ماڈل کے پاس نہیں، جب آپ کو حوالہ جات چاہئیں، یا جب fine-tuning ممکن نہ ہو۔

```python
# RAG pipeline overview
query_vector = embedder.embed(user_query)
chunks = qdrant.search(query_vector, top_k=5)
context = "\n\n".join(chunk.text for chunk in chunks)
answer = llm.generate(system=f"Context:\n{context}", user=user_query)
```

**RAG کب استعمال کریں:**
- خاصی معلومات جو ماڈل کے پاس نہیں (مثلاً آپ کا نصابی کتاب مواد)
- حوالہ جات اور ماخذ حوالے کی ضرورت
- Fine-tuning بہت مہنگا یا سست ہے

512-ٹوکن chunks اور 20% overlap سے شروع کریں، پھر retrieval معیار کے اشاروں کی بنیاد پر ٹیون کریں۔

### پیٹرن ۲: ایجنٹ لوپس

ایجنٹ لوپس AI کو اقدام کرنے، نتائج دیکھنے، اور اگلے اقدام فیصلہ کرنے دیتے ہیں۔

```python
while True:
    response = llm.create(tools=tools, messages=messages)
    if response.stop_reason == "end_turn":
        break
    # Execute tool calls, feed results back
    tool_results = execute_tools(response.tool_calls)
    messages.append(tool_results)
```

**پروڈکشن ایجنٹس کے اصول:**
- بے قابو عمل کو روکنے کے لیے رکنے کی شرائط طے کریں
- ناقابل واپسی اقدامات کے لیے انسانی منظوری ضروری بنائیں
- ایجنٹس کو کم از کم اجازتیں دیں (least privilege)
- ان پٹ، آؤٹ پٹ اور وقت کے ساتھ ہر tool call لاگ کریں

### پیٹرن ۳: منظم آؤٹ پٹ

ماڈل کو JSON تیار کرنے پر مجبور کریں جسے آپ کی ایپلیکیشن قابل اعتماد طریقے سے parse کر سکے۔

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

### پیٹرن ۴: تشخیص-فیڈ بیک لوپ

پروڈکشن ٹریفک ← تشخیص ← اشارے ← Prompt بہتری ← دہرائیں۔

Prompts کو بہتر بنانے سے **پہلے** تشخیصی بنیادی ڈھانچہ بنائیں۔ وہ ٹیمیں جو یہ لوپ سختی سے چلاتی ہیں وہ مہینوں میں معیار کو مرکب ہوتے دیکھتی ہیں۔

:::info آرکیٹیکچر فیصلہ
اس نصابی کتاب کے لیے، ہم chatbot کے لیے RAG (Qdrant + Cohere embeddings) اور ایجنٹ skills کے لیے منظم آؤٹ پٹ (Pydantic) استعمال کرتے ہیں۔ دونوں پیٹرن `/api/chat` اور `/api/agent` پر لائیو ہیں۔
:::
