---
id: topic-01
title: "Testing AI-Native Features"
sidebar_label: "Testing AI-Native Features"
---

## Testing AI-Native Features

Evaluation-based testing checks whether outputs meet quality criteria rather than matching exact expected values. Quality criteria include relevance, factual correctness, format compliance, safety, and appropriate length.

### Why Traditional Testing Fails for AI

```python
# This will ALWAYS fail for AI — outputs are non-deterministic
assert llm.generate("What is ROS 2?") == "ROS 2 is a robotics middleware..."

# This is correct — evaluate against quality criteria
result = llm.generate("What is ROS 2?")
assert "middleware" in result.lower() or "robot" in result.lower()
assert len(result) > 50
assert not contains_hallucination(result)
```

### Golden Set Evaluation

Maintain a curated collection of input/expected-output pairs where expected output is a quality bar, not an exact match.

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

Build it from real production traffic with human ratings. Re-run evaluations whenever you change prompts, models, or pipeline configuration.

### AI-as-Judge Evaluation

For large-scale evaluation where human rating is too expensive, use a separate AI model as judge.

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

Calibrate the judge by comparing its scores to human ratings on a sample. A well-calibrated judge correlates with human judgment.

### Regression Testing in CI

```yaml
# .github/workflows/eval.yml
- name: Run evaluation suite
  run: python -m pytest tests/evals/ --threshold=0.85
  # Block deploy if quality drops below 85%
```

Block deploys that introduce regressions on your golden set without explicit human approval.

:::tip
Run contract tests validating output schema correctness on every commit. Run quality evaluations on a schedule or before significant releases.
:::
