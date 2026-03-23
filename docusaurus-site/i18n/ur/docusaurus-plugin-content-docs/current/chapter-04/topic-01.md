---
id: topic-01
title: "AI-Native خصوصیات کی جانچ"
sidebar_label: "AI-Native خصوصیات کی جانچ"
---

## AI-Native خصوصیات کی جانچ

تشخیص پر مبنی جانچ یہ جانچتی ہے کہ آیا آؤٹ پٹ معیار کے معیار پر پورا اترتے ہیں نہ کہ عین متوقع قدروں سے ملانا۔ معیار کے معیار میں مطابقت، حقائق کی درستگی، شکل کی تعمیل، حفاظت اور مناسب لمبائی شامل ہیں۔

### روایتی جانچ AI کے لیے کیوں ناکام ہوتی ہے

```python
# This will ALWAYS fail for AI — outputs are non-deterministic
assert llm.generate("What is ROS 2?") == "ROS 2 is a robotics middleware..."

# This is correct — evaluate against quality criteria
result = llm.generate("What is ROS 2?")
assert "middleware" in result.lower() or "robot" in result.lower()
assert len(result) > 50
assert not contains_hallucination(result)
```

### گولڈن سیٹ تشخیص

ان پٹ/متوقع-آؤٹ پٹ جوڑوں کا منتخب مجموعہ برقرار رکھیں جہاں متوقع آؤٹ پٹ ایک معیار کی حد ہے، عین میل نہیں۔

```python
GOLDEN_SET = [
    {
        "input": "What is Nav2?",
        "expected_keywords": ["navigation", "ROS 2", "planner"],
        "min_length": 50,
        "must_not_contain": ["I don't know", "I cannot"]
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

انسانی درجہ بندیوں کے ساتھ حقیقی پروڈکشن ٹریفک سے بنائیں۔ جب بھی prompts، ماڈلز، یا پائپ لائن کنفیگریشن تبدیل کریں تشخیص دوبارہ چلائیں۔

### AI بطور جج تشخیص

بڑے پیمانے پر تشخیص کے لیے جہاں انسانی درجہ بندی بہت مہنگی ہو، ایک الگ AI ماڈل کو جج کے طور پر استعمال کریں۔

```python
JUDGE_PROMPT = """
Rate this answer on a scale of 1-5 for:
- Accuracy (is it factually correct?)
- Relevance (does it answer the question?)
- Completeness (is it thorough enough?)

Question: {question}
Answer: {answer}

Respond with JSON: {{"accuracy": N, "relevance": N, "completeness": N}}
"""
```

جج کو نمونے پر انسانی درجہ بندیوں سے اس کے اسکور کا موازنہ کر کے کیلیبریٹ کریں۔ ایک اچھا کیلیبریٹ جج انسانی فیصلے سے مطابقت رکھتا ہے۔

### CI میں Regression جانچ

```yaml
# .github/workflows/eval.yml
- name: Run evaluation suite
  run: python -m pytest tests/evals/ --threshold=0.85
  # Block deploy if quality drops below 85%
```

وہ تعیناتیاں روکیں جو واضح انسانی منظوری کے بغیر آپ کے گولڈن سیٹ پر regressions متعارف کراتی ہیں۔

:::tip
ہر commit پر آؤٹ پٹ schema درستگی کی تصدیق کرنے والے contract tests چلائیں۔ معیار کی تشخیص ایک شیڈول پر یا اہم ریلیز سے پہلے چلائیں۔
:::
