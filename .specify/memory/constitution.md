<!-- Sync Impact Report
  Version change: 0.0.0 (template) → 1.0.0 (initial ratification)
  Modified principles: all placeholders replaced with project-specific values
  Added sections:
    - Core Principles (7 principles)
    - Technology Constraints
    - Development Workflow
    - Governance
  Removed sections: none
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ aligned (constitution check)
    - .specify/templates/spec-template.md ✅ aligned
    - .specify/templates/tasks-template.md ✅ aligned
  Follow-up TODOs: none — all fields resolved
-->

# AI-Native Driven Development — Book Website Constitution

## Core Principles

### I. Zero External UI Dependencies
Every UI component MUST be built exclusively with **shadcn/ui** and **Tailwind CSS**.
No other component libraries (MUI, Chakra, Ant Design, Radix direct, etc.) SHALL be installed or imported.
All design tokens (colours, spacing, typography, gradients, blur values) MUST be defined in `tailwind.config.ts`
and consumed from there — no inline ad-hoc style values.
**Rationale:** Controls bundle size, enforces visual consistency, and removes upgrade/breaking-change risk
from third-party component libraries.

### II. Mobile-First, Glassmorphism Design System
Every component MUST be designed for the smallest viewport (320px) first, then enhanced for 768px and 1440px.
Glassmorphism cards MUST use `backdrop-filter: blur()`, semi-transparent backgrounds, and a subtle border.
Gradient usage (backgrounds, buttons, headings) MUST reference the Tailwind palette — no arbitrary values.
**Rationale:** Guarantees a premium, cohesive visual identity across all devices without per-breakpoint rewrites.

### III. MDX as Single Source of Truth for Content
All book content MUST live exclusively in MDX files under `/content/chapters/`.
Frontmatter (title, chapterNumber, topicNumber, description) MUST be present in every MDX file.
Adding or removing an MDX file MUST automatically update the Book page table of contents at build time
without requiring changes to any component or routing logic.
**Rationale:** Decouples content authoring from engineering; any contributor can update chapters without
touching application code.

### IV. Performance Budget (NON-NEGOTIABLE)
- First Contentful Paint (FCP): **< 1.5 seconds** on simulated 4G (Lighthouse).
- Total JavaScript bundle: **< 150 KB** (gzip compressed, images excluded).
- Lighthouse Performance score: **≥ 90**.
- All pages MUST use Next.js SSG or ISR — no client-side data fetching for content.
- Images MUST use `next/font` and `next/image` with `width`, `height`, and lazy-loading set.
**Rationale:** Performance is a user-experience and SEO first-class requirement, not an afterthought.

### V. Accessibility — WCAG 2.1 AA (NON-NEGOTIABLE)
- Lighthouse Accessibility score MUST be **≥ 90** on every page.
- Every interactive element MUST be keyboard-focusable with a visible focus ring (no `outline: none`
  without a replacement).
- All images MUST have descriptive `alt` text; decorative images MUST have `alt=""`.
- Every page MUST include a "Skip to main content" link as the first focusable element.
- Text/background colour combinations MUST meet 4.5 : 1 contrast (normal text) and 3 : 1 (large text).
- Form inputs MUST be associated with `<label>` elements and use `aria-required` / `aria-describedby`.
**Rationale:** Accessibility is a legal obligation and a quality signal — inaccessible sites are unacceptable.

### VI. TypeScript Strict Mode + Code Quality
- `tsconfig.json` MUST have `"strict": true` with zero TypeScript errors in production builds.
- ESLint MUST pass with the Next.js recommended ruleset and zero warnings in the production build output.
- All components MUST be reusable, self-contained, and accept typed props — no hard-coded page-specific
  content inside shared components.
- The smallest viable diff MUST be preferred; unrelated code MUST NOT be refactored in the same PR.
**Rationale:** Strict types catch bugs at compile time; reusable components prevent duplication and
accelerate future changes.

### VII. Dark / Light Mode — Persistent & Accessible
- The site MUST detect OS-level preference via `prefers-color-scheme` on first load.
- User preference MUST be persisted in `localStorage` and restored on next visit.
- The toggle control MUST be present in the site-wide header on all four pages.
- The toggle MUST include `aria-label="Toggle dark mode"` and be keyboard operable.
- Both modes MUST independently meet WCAG 2.1 AA contrast requirements.
**Rationale:** Comfort in varied lighting environments is expected; inaccessible colour modes defeat the
purpose of the toggle.

## Technology Constraints

| Constraint | Rule |
|---|---|
| Framework | Next.js 15 (App Router) — MUST use `app/` directory |
| Styling | Tailwind CSS + shadcn/ui only; no other UI libraries |
| Content | MDX files in `/content/chapters/` only |
| Language | TypeScript with `strict: true`; no plain `.js` source files |
| Fonts | Maximum 2 font families; MUST be loaded via `next/font` |
| Secrets | MUST use `.env`; secrets NEVER hardcoded; `.env.example` MUST document all vars |
| Deployment | Vercel free tier; auto-deploy from `main` branch; no paid add-ons required |
| Pages | Exactly 4: Home (`/`), Book (`/book`), About (`/about`), Contact (`/contact`) |
| Book structure | 5 chapters × 2 topics each (10 MDX files minimum) |

## Development Workflow

1. **Clarify first** — requirements and intent MUST be understood before any code is written.
2. **Spec → Plan → Tasks → Implement** — follow the SpecKit Plus workflow for every feature.
3. **PHR after every prompt** — a Prompt History Record MUST be created under `history/prompts/`
   for every user input (constitution, feature, or general stage).
4. **ADR on significant decisions** — when a decision is architecturally significant (framework choice,
   data model, API contract, security model), suggest `/sp.adr <title>`. Never auto-create ADRs.
5. **Smallest viable diff** — PRs MUST touch only what is required; no speculative refactors.
6. **No invented contracts** — never assume APIs or data shapes; ask for clarification if missing.
7. **Commit message convention** — `type(scope): description` (e.g., `feat(book): add chapter navigation`).

## Governance

- This constitution supersedes all other coding conventions and project guidelines.
- Amendments require: (a) a written rationale, (b) version bump per semantic versioning rules,
  (c) propagation to all dependent templates (plan, spec, tasks), and (d) a documenting commit.
- All PRs and code reviews MUST verify compliance with the principles above.
- Complexity MUST be justified against a principle; unjustified complexity is a blocker.
- The runtime development guidance file is `CLAUDE.md` at the project root.
- Constitution compliance is reviewed at the start of every `/sp.plan` session.

**Version**: 1.0.0 | **Ratified**: 2026-03-06 | **Last Amended**: 2026-03-06
