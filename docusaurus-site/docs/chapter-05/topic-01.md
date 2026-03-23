---
id: topic-01
title: "Emerging Patterns and Tools"
sidebar_label: "Emerging Patterns & Tools"
---

## Emerging Patterns and Tools

The most significant architectural shift is AI agents acting as operating systems orchestrating specialised models and tools.

### Agents as Operating Systems

An orchestrator agent coordinates planning, research, implementation, evaluation, and communication agents. Each has specific tools, a well-defined interface, and domain-relevant memory. The human sets top-level intent and approves critical decisions.

```
TextbookMasterAgent (orchestrator)
├── RAGQuerySkill       → search textbook content
├── ChapterGenerationSkill → write/expand chapters
├── PersonalizationSkill   → adapt to learner profile
├── TranslationSkill       → Urdu translation
└── IngestionSkill         → embed new content
```

This is exactly how this textbook's backend is built — `TextbookMasterAgent` orchestrates five reusable skills via Claude's tool-use API.

### Context Windows and Multimodal AI

Context windows from 128K to 1 million tokens reshape system design:

| Context Size | Best Use |
|---|---|
| 8K–32K | Standard chat, code review |
| 128K | Long documents, full codebases |
| 1M | Entire textbooks, video analysis |

Long context does **not** eliminate RAG. Use long context when precision matters most and RAG when scale and cost matter most.

### Vision-Language-Action (VLA) Models

VLA models are the next frontier for Physical AI. They take visual input, understand language instructions, and output robot actions.

```
Camera Input → Vision Encoder
                    ↓
Language Instruction → Language Model → Action Output → Robot
```

Key VLA models:
- **RT-2** (Google): robotics transformer, web-scale training
- **OpenVLA**: open-source, runs on Jetson Orin Nano
- **π0** (Physical Intelligence): dexterous manipulation

### The Code Generation Maturity Curve

Teams progress through five stages:

1. **Autocomplete** — tab completion in IDE
2. **Function generation** — generate one function at a time
3. **Component generation** — generate full components
4. **Feature generation** — generate entire features from spec
5. **System generation** — generate systems from intent

Leading AI-Native teams reach Stage 5 for well-specified features. Bet on patterns, not tools. The patterns remain as specific tools change every 18 months.
