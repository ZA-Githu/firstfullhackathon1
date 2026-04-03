---
id: topic-01
title: "AI-Native فیچرز کی ٹیسٹنگ"
sidebar_label: "AI-Native فیچرز کی ٹیسٹنگ"
---

## AI-Native فیچرز کی ٹیسٹنگ

Evaluation-based ٹیسٹنگ چیک کرتی ہے کہ آیا آؤٹ پٹس معیار کے معیار کو پورا کرتے ہیں نہ کہ بالکل متوقع اقدار سے مماثلت رکھتے ہیں۔ معیار کے معیار میں متعلقہ ہونا، حقیقت پسندانہ درستگی، فارمیٹ کی تعمیل، حفاظت، اور مناسب لمبائی شامل ہیں۔

### AI کے لیے روایتی ٹیسٹنگ کیوں ناکام ہوتی ہے

```python
# یہ AI کے لیے ہمیشہ ناکام ہو جائے گا — آؤٹ پٹس غیر یقینی ہیں
assert llm.generate("ROS 2 کیا ہے؟") == "ROS 2 ایک roboٹکس middleware ہے..."

# یہ درست ہے — معیار کے معیار کے خلاف تشخیص کریں
result = llm.generate("ROS 2 کیا ہے؟")
assert "middleware" in result.lower() or "robot" in result.lower()
assert len(result) > 50
assert not contains_hallucination(result)
```

### Golden Set Evaluation

ان پٹ/متوقع-آؤٹ پٹ جوڑوں کا ایک curated مجموعہ برقرار رکھیں جہاں متوقع آؤٹ پٹ ایک معیار کی بار ہے، نہ کہ بالکل مماثلت۔

```python
GOLDEN_SET = [
    {
        "input": "Nav2 کیا ہے؟",
        "expected_keywords": ["navigation", "ROS 2", "planner"],
        "min_length": 50,
        "must_not_contain": ["مجھے نہیں معلوم", "میں نہیں کر سکتا"]
    },
    # ...
]

def evaluate_golden_set(model_fn):
    scores = []
    for case in GOLDEN_SET:
        output = model_fn(case["input"])
        score = score_output(output, case)
        scores.append(score)
    return sum(scores) / len(scores)
```

اسے انسانی درجہ بندی کے ساتھ حقیقی پروڈکشن ٹریفک سے بنائیں۔ جب بھی آپ prompts، ماڈلز، یا پائپ لائن کنفیگریشن کو تبدیل کریں تو evaluations کو دوبارہ چلائیں۔

### AI-as-Judge Evaluation

بڑے پیمانے کی evaluation کے لیے جہاں انسانی درجہ بندی بہت مہنگی ہے، جج کے طور پر ایک الگ AI ماڈل استعمال کریں۔

```python
JUDGE_PROMPT = """
اس جواب کو 1-5 کے پیمانے پر درجہ دیں:
- درستگی (کیا یہ حقیقت پسندانہ طور پر درست ہے؟)
- متعلقہ ہونا (کیا یہ سوال کا جواب دیتا ہے؟)
- مکمل ہونا (کیا یہ کافی تفصیلی ہے؟)

سوال: {question}
جواب: {answer}

JSON کے ساتھ جواب دیں: {{"accuracy": N, "relevance": N, "completeness": N}}
"""
```

جج کو کیلیبریٹ کریں by comparing its scores to human ratings on a sample. ایک اچھی طرح کیلیبریٹڈ جج انسانی فیصلے کے ساتھ correlate کرتا ہے۔

### CI میں Regression ٹیسٹنگ

```yaml
# .github/workflows/eval.yml
- name: Evaluation suite چلائیں
  run: python -m pytest tests/evals/ --threshold=0.85
  # اگر معیار 85% سے نیچے گرتا ہے تو ڈپلائے کو روکیں
```

ان واضح انسانی منظوری کے بغیر regressions متعارف کرانے والے ڈپلائمنٹس کو روکیں۔

:::tip
ہر commit پر آؤٹ پٹ schema کی درستگی کی تصدیق کرنے والے contract ٹیسٹس چلائیں۔ معیار کی evaluations کو شیڈول پر یا اہم ریلیزز سے پہلے چلائیں۔
:::
