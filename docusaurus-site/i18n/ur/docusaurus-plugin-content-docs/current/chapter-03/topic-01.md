---
id: topic-01
title: "AI-Native ایپس کے لیے آرکیٹیکچر پیٹرنز"
sidebar_label: "آرکیٹیکچر پیٹرنز"
---

## AI-Native ایپس کے لیے آرکیٹیکچر پیٹرنز

چار بنیادی پیٹرنز ہر پروڈکشن AI-Native سسٹم کو طاقت دیتے ہیں۔

### پیٹرن 1: Retrieval-Augmented Generation (RAG)

RAG آپ کے ڈیٹا سے متعلقہ سیاق و سباق کو واپس لاتا ہے اور اسے prompt میں شامل کرتا ہے۔ RAG اس وقت استعمال کریں جب آپ کے پروڈکٹ کے پاس proprietary علم ہو جو ماڈل کے پاس نہیں ہے، جب آپ کو حوالہ جات کی ضرورت ہو، یا جب fine-tuning ممکن نہ ہو۔

```python
# RAG پائپ لائن کا جائزہ
query_vector = embedder.embed(user_query)
chunks = qdrant.search(query_vector, top_k=5)
context = "\n\n".join(chunk.text for chunk in chunks)
answer = llm.generate(system=f"Context:\n{context}", user=user_query)
```

**RAG کب استعمال کریں:**
- Proprietary علم جو ماڈل کے پاس نہیں ہے (مثلاً آپ کی کتاب کا مواد)
- حوالہ جات اور ماخذ کے حوالہ جات کی ضرورت
- Fine-tuning بہت مہنگا یا سست ہے

512-token chunks اور 20% overlap کے ساتھ شروع کریں، پھر retrieval quality metrics کی بنیاد پر ٹیون کریں۔

### پیٹرن 2: Agent Loops

Agent loops AI کو کارروائیاں کرنے، نتائج کا مشاہدہ کرنے، اور اگلے مراحل کا فیصلہ کرنے دیتے ہیں۔

```python
while True:
    response = llm.create(tools=tools, messages=messages)
    if response.stop_reason == "end_turn":
        break
    # ٹول کالز کو چلائیں، نتائج کو واپس کھلائیں
    tool_results = execute_tools(response.tool_calls)
    messages.append(tool_results)
```

**پروڈکشن ایجنٹس کے لیے اصول:**
- بے لگام عمل درآمد کو روکنے کے لیے اسٹاپ کی شرائط کی تعریف کریں
- ناقابل واپسی کارروائیوں کے لیے انسانی منظوری کی ضرورت ہے
- ایجنٹس کو کم از کم اجازتیں دیں (کم سے کم استحقاق)
- ہر ٹول کال کو ان پٹس، آؤٹ پٹس، اور ٹائم اسٹیمپس کے ساتھ لاگ کریں

### پیٹرن 3: Structured Output

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
    messages=[{"role": "user", "content": "باب 1 کا خلاصہ کریں"}]
)
```

### پیٹرن 4: Evaluation-Feedback Loop

پروڈکشن ٹریفک → Evaluation → Metrics → Prompt بہتری → دہرائیں۔

prompts کو بہتر بنانے سے **پہلے** evaluation انفراسٹرکچر بنائیں۔ جو ٹیمیں اس لوپ کو سختی سے چلاتی ہیں وہ مہینوں میں معیار کو مرکب ہوتے دیکھتی ہیں۔

:::info آرکیٹیکچرل فیصلہ
اس کتاب کے لیے، ہم chatbot کے لیے RAG (Qdrant + Cohere embeddings) استعمال کرتے ہیں اور ایجنٹ مہارتوں کے لیے structured output (Pydantic) استعمال کرتے ہیں۔ دونوں پیٹرنز `/api/chat` اور `/api/agent` پر زندہ ہیں۔
:::
