---
id: topic-02
title: "مانیٹرنگ، Observability، اور فیڈ بیک لوپس"
sidebar_label: "مانیٹرنگ اور Observability"
---

## مانیٹرنگ، Observability، اور فیڈ بیک لوپس

AI observability کے چار ستون:

| ستون | میٹرک | اس وقت الرٹ کریں جب |
|---|---|---|
| **Latency** | p50 / p95 / p99 | p95 > 5s |
| **لاگت** | فی کال tokens، فی صارف لاگت | لاگت میں 2x سے زیادہ اضافہ |
| **معیار** | صارف کی فیڈ بیک درجہ بندی | درجہ بندی میں 10% سے زیادہ کمی |
| **حفاظت** | نقصان دہ اسکور، بلاک ریٹ | بلاک ریٹ میں اضافہ |

### AI کالز کی Tracing

structured logging کے ساتھ ہر AI کال کو end-to-end trace کریں:

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

correlation IDs استعمال کریں جو log لائنز کو traces سے جوڑتی ہیں۔ یہ معیار کے مسائل کو debug کرنا ممکن بناتا ہے۔

### صارف کی فیڈ بیک Flywheel

```
AI آؤٹ پٹس پر فیڈ بیک جمع کریں
    ↓
تجزیہ کریں کہ کون سے آؤٹ پٹس منفی فیڈ بیک حاصل کرتے ہیں
    ↓
prompt تبدیلیوں کے بارے میں مفروضے بنائیں
    ↓
لائیو ٹریفک پر نئے بمقابلہ پرانے prompts کا A/B ٹیسٹ کریں
    ↓
فاتحین کو ڈپلائے کریں → مانیٹر کریں → بہتری کی تصدیق کریں
    ↓
دہرائیں
```

یہ flywheel وقت کے ساتھ معیار کو مرکب کرتا ہے۔

### Prompt ورژن مینجمنٹ

prompts کے ساتھ کوڈ کی طرح سلوک کریں:

```python
PROMPTS = {
    "rag-v1": "صرف context کی بنیاد پر جواب دیں...",
    "rag-v2": "آپ ایک ٹیچنگ اسسٹنٹ ہیں... صرف جواب دیں...",
}

# فی-ورژن معیار کے میٹرکس کو ٹریک کریں
metrics = {
    "rag-v1": {"avg_rating": 3.8, "hallucination_rate": 0.04},
    "rag-v2": {"avg_rating": 4.2, "hallucination_rate": 0.01},
}
```

منٹوں کے اندر rollback کی صلاحیت کو برقرار رکھیں۔ فی-ورژن معیار کے میٹرکس کو ٹریک کریں تاکہ آپ کو ہمیشہ معلوم ہو کہ حالیہ تبدیلیوں نے کارکردگی کو بہتر بنایا یا خراب کیا۔
