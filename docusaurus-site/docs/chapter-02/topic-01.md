---
id: topic-01
title: "Spec-Driven Development with AI"
sidebar_label: "Spec-Driven Development"
---

## Spec-Driven Development with AI

The single biggest failure mode of AI-Native teams is starting to code too early. You open your IDE, fire up Claude, and start prompting: "build me a login page." The AI produces something. You tweak it. You realise the auth flow is wrong. Two hours later you have a working prototype that solves the wrong problem.

The solution is **Spec-Driven Development** — a discipline of capturing *what* you are building and *why* in a structured specification before a single line of code is written.

### The Spec-Driven Workflow

```
User Intent
    ↓
/sp.specify → spec.md  (WHAT + WHY)
    ↓
/sp.plan    → plan.md  (HOW)
    ↓
/sp.tasks   → tasks.md (WHAT ORDER)
    ↓
/sp.implement → code   (DO IT)
```

Each stage feeds the next. AI drives the drafting; the human drives the approval.

### What is a Spec?

A specification describes:
- **Who** the feature serves (user stories with priorities)
- **What** the system must do (functional requirements)
- **When** the feature is successful (acceptance criteria and success metrics)
- **What** is explicitly out of scope (non-goals)

Crucially, a spec does **not** describe *how* to build it. Those belong in the plan.

### Writing a Strong Spec Prompt

**Weak intent:**
```
Build a contact form
```

**Strong intent:**
```
/sp.specify Contact Page
Intent: Build a waitlist capture form for visitors who want
updates about the book. The form collects name, email, and
an optional message. Save submissions to localStorage (no
backend). Show a success confirmation after submit.
Success Criteria:
- Form validates email format before submission
- Submissions persist across page refreshes
- Form is keyboard-accessible
Non-goals: Email sending, backend API, authentication
```

### Anatomy of a Good Spec

**User Stories with Priorities**
Each story is independently testable. Assign P1 (critical), P2 (important), P3 (nice to have).

**Functional Requirements**
Numbered (`FR-001`, `FR-002`...). Use "MUST" for non-negotiable requirements.

**Success Criteria**
Measurable outcomes, technology-agnostic.

**Assumptions and Non-Goals**
Document what you assumed and what you explicitly excluded.

:::info Rule of thumb
A spec is complete when a developer who has never spoken to you could implement the feature correctly from the document alone.
:::

### Why Specs Make AI Better

When you give an AI a spec to implement from:

1. **Outputs are more accurate** — concrete acceptance criteria to aim for
2. **Outputs are more consistent** — documented assumptions to work from
3. **Reviews are faster** — check AI output against specific, numbered requirements

### Common Spec Mistakes

- **Too much implementation detail** — if your spec says "use PostgreSQL," it is too specific
- **Vague success criteria** — "users should be happy" is not a success criterion
- **Missing non-goals** — without explicit exclusions, scope expands silently
- **No priority order** — if everything is P1, nothing is
