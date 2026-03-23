---
id: topic-02
title: "Prompt Engineering as a First-Class Skill"
sidebar_label: "Prompt Engineering"
---

## Prompt Engineering as a First-Class Skill

Every effective prompt has five components: **Role, Context, Task, Format, and Constraints**.

- **Role** — tells the AI who it is in this context
- **Context** — gives background it needs to understand the task
- **Task** — defines exactly what to do
- **Format** — specifies the output structure
- **Constraints** — lists what must not happen

### Chain-of-Thought Prompting

Ask the AI to reason step-by-step before concluding. For example:

```
Before recommending an approach, list three options with tradeoffs,
then choose the one that best fits our constraints.
```

This surfaces flawed assumptions before they become implemented decisions.

### Few-Shot Prompting for Consistency

When generating multiple similar artifacts, provide one complete example and ask the AI to match it exactly. Without an example each output differs. With it, output is consistent and predictable.

```
Here is an example spec for a login feature:
[EXAMPLE SPEC]

Now generate a spec in the exact same format for a password reset feature.
```

### Common Failure Modes

| Failure Mode | Result | Fix |
|---|---|---|
| Ambiguous scope | Wrong implementation | Be explicit about boundaries |
| Missing format spec | Wrong output shape | Show an example output |
| Missing constraints | Wrong technology choices | List what NOT to use |
| Task too large | Unreviewed results | Break into spec-plan-tasks-implement |

### Building a Prompt Library

Maintain a versioned library of high-performing prompts covering:
- Spec generation
- Architecture review
- Code review
- Debugging sessions
- Documentation

Treat it as a competitive asset that compounds value over time. Version it like code. Test the library whenever you upgrade models.

:::tip
Share your prompt library across the team. A great prompt written once benefits everyone. A bad prompt used by everyone costs everyone.
:::
