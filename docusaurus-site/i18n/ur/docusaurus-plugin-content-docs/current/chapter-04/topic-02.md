---
id: topic-02
title: "نگرانی، مشاہدہ، اور فیڈ بیک لوپس"
sidebar_label: "نگرانی اور مشاہدہ"
---

## نگرانی، مشاہدہ، اور فیڈ بیک لوپس

AI مشاہدے کے چار ستون:

| ستون | اشارہ | الرٹ کب |
|---|---|---|
| **تاخیر (Latency)** | p50 / p95 / p99 | p95 > 5s |
| **لاگت (Cost)** | فی کال tokens، فی صارف لاگت | لاگت > 2x بڑھ جائے |
| **معیار (Quality)** | صارف فیڈ بیک درجہ بندی | درجہ بندی > 10% گرے |
| **حفاظت (Safety)** | نقصان اسکور، block rate | Block rate اچانک بڑھے |

### AI کالز کا سراغ لگانا

منظم logging کے ساتھ ہر AI کال کا شروع سے آخر تک سراغ لگائیں:

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

لاگ لائنوں کو traces سے جوڑنے کے لیے correlation IDs استعمال کریں۔ یہ معیار کے مسائل کو debug کرنا ممکن بناتا ہے۔

### صارف فیڈ بیک فلائی ویل

```
AI آؤٹ پٹ پر فیڈ بیک جمع کریں
    ↓
تجزیہ کریں کہ کون سے آؤٹ پٹ کو منفی فیڈ بیک ملتا ہے
    ↓
Prompt تبدیلیوں کے بارے میں مفروضے بنائیں
    ↓
لائیو ٹریفک پر نئے بمقابلہ پرانے prompts A/B ٹیسٹ کریں
    ↓
فاتح تعینات کریں ← نگرانی کریں ← بہتری کی تصدیق کریں
    ↓
دہرائیں
```

یہ فلائی ویل وقت کے ساتھ معیار کو مرکب کرتا ہے۔

### Prompt ورژن انتظام

Prompts کو کوڈ کی طرح سمجھیں:

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

منٹوں میں rollback کی صلاحیت برقرار رکھیں۔ فی ورژن معیار کے اشاروں کو ٹریک کریں تاکہ آپ ہمیشہ جانیں کہ حالیہ تبدیلیوں نے کارکردگی بہتر کی یا خراب۔
