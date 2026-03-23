# Implementation Plan: AI-Native Book Website

**Branch**: `1-book-website` | **Date**: 2026-03-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-book-website/spec.md`

---

## Summary

Build a premium, static book website for "AI-Native Driven Development" using Next.js 15 App Router,
Tailwind CSS, shadcn/ui, and MDX as the single content source. The site has exactly 4 pages
(Home, Book, About, Contact), 5 chapters × 2 topics each served from `/content/chapters/` MDX files,
a reading progress bar, dark/light mode persisted in localStorage, a waitlist form saved to localStorage,
and deploys to Vercel free tier. All architectural decisions are resolved — no NEEDS CLARIFICATION
markers remain.

---

## Technical Context

**Language/Version**: TypeScript 5.x with `strict: true`
**Framework**: Next.js 15.x (App Router)
**Styling**: Tailwind CSS 3.x + shadcn/ui (Radix primitives)
**Content**: MDX via `@next/mdx` + `next-mdx-remote` + `gray-matter` (frontmatter)
**Syntax Highlighting**: `rehype-pretty-code` + `shiki` (zero-runtime, static)
**Fonts**: `next/font` — Inter (body) + Clash Display or Sora (headings)
**Storage**: localStorage only (no backend, no DB)
**Testing**: Vitest + React Testing Library (unit); Playwright (E2E smoke)
**Target Platform**: Vercel free tier (static export or SSG)
**Performance Goals**: FCP < 1.5s · bundle < 150KB gzip · Lighthouse perf ≥ 90
**Constraints**: No external UI libraries beyond shadcn/ui + Tailwind; `strict: true`; 4 pages only
**Scale/Scope**: Static site; single author; ~10 MDX files; no concurrent-user concern

---

## Constitution Check

*GATE: Must pass before Phase 0. Re-checked after Phase 1 design.*

| Principle | Status | Evidence |
|---|---|---|
| I — Zero External UI Deps | ✅ PASS | Only shadcn/ui + Tailwind used; no MUI/Chakra/Ant |
| II — Mobile-First Glassmorphism | ✅ PASS | All components designed 320px → 768px → 1440px; backdrop-filter in design tokens |
| III — MDX Single Source of Truth | ✅ PASS | All content in `/content/chapters/`; frontmatter required on every file |
| IV — Performance Budget | ✅ PASS | SSG only; `next/image`; `next/font`; rehype-pretty-code (zero runtime) |
| V — Accessibility WCAG 2.1 AA | ✅ PASS | Skip links, ARIA labels, keyboard nav, focus rings all planned per-component |
| VI — TypeScript Strict + Quality | ✅ PASS | `strict: true` in tsconfig; ESLint next/core-web-vitals; reusable typed components |
| VII — Dark/Light Mode | ✅ PASS | `next-themes` for SSR-safe mode switching; localStorage persistence; `aria-label` on toggle |

**Constitution Gate: ALL PASS — proceed to Phase 0.**

---

## Project Structure

### Documentation (this feature)

```text
specs/1-book-website/
├── plan.md              ← this file
├── research.md          ← Phase 0 decisions
├── data-model.md        ← Phase 1 entities + MDX schema
├── quickstart.md        ← Phase 1 developer setup
├── contracts/
│   └── localStorage.md  ← localStorage key contracts
└── tasks.md             ← Phase 2 output (/sp.tasks — not yet created)
```

### Source Code (repository root)

```text
ai-native-book/
├── app/                          # Next.js 15 App Router
│   ├── layout.tsx                # Root layout — ThemeProvider, Nav, fonts
│   ├── page.tsx                  # Home page
│   ├── book/
│   │   └── page.tsx              # Book page (MDX loader + ToC + progress bar)
│   ├── about/
│   │   └── page.tsx              # About page
│   ├── contact/
│   │   └── page.tsx              # Contact / Waitlist page
│   └── globals.css               # Tailwind base + CSS variables for theme
│
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx            # Site-wide nav (mobile hamburger + dark toggle)
│   │   ├── Footer.tsx            # Minimal footer
│   │   └── SkipLink.tsx          # "Skip to main content" — first focusable element
│   ├── ui/                       # shadcn/ui generated components (button, card, etc.)
│   ├── home/
│   │   ├── Hero.tsx              # Hero section — title, subtitle, CTA
│   │   └── ChapterCard.tsx       # Glassmorphism chapter preview card
│   ├── book/
│   │   ├── TableOfContents.tsx   # Sticky sidebar ToC (desktop) + overlay (mobile)
│   │   ├── ProgressBar.tsx       # Reading progress bar (fixed top)
│   │   ├── ChapterSection.tsx    # Wrapper per chapter in the book page
│   │   └── MDXContent.tsx        # MDX renderer with custom component map
│   ├── about/
│   │   └── AuthorCard.tsx        # Author bio + image
│   └── contact/
│       └── WaitlistForm.tsx      # Controlled form + localStorage save + validation
│
├── content/
│   └── chapters/
│       ├── chapter-01-topic-01.mdx
│       ├── chapter-01-topic-02.mdx
│       ├── chapter-02-topic-01.mdx
│       ├── chapter-02-topic-02.mdx
│       ├── chapter-03-topic-01.mdx
│       ├── chapter-03-topic-02.mdx
│       ├── chapter-04-topic-01.mdx
│       ├── chapter-04-topic-02.mdx
│       ├── chapter-05-topic-01.mdx
│       └── chapter-05-topic-02.mdx
│
├── lib/
│   ├── mdx.ts                    # getAllChapters(), getChapterBySlug() — fs-based
│   ├── localStorage.ts           # getWaitlist(), saveWaitlistEntry() — typed helpers
│   └── utils.ts                  # cn() classname merge, scroll helpers
│
├── types/
│   └── index.ts                  # Chapter, Topic, WaitlistEntry, UserPreference types
│
├── public/
│   └── author.jpg                # Author profile image (placeholder until real photo)
│
├── tailwind.config.ts            # Design tokens: colours, gradients, blur, typography
├── next.config.ts                # MDX + security headers config
├── tsconfig.json                 # strict: true
├── components.json               # shadcn/ui config
├── .env.example                  # documents any env vars (none required for MVP)
└── vercel.json                   # optional: redirect rules, headers
```

**Structure Decision**: Single Next.js 15 App Router project. No separate backend. No monorepo.
All content sourced from filesystem MDX files — no CMS, no API routes required at MVP.

---

## Phase 0: Research & Decisions

*See [`research.md`](./research.md) for full rationale. Summary below.*

| Decision | Chosen | Rejected | Rationale |
|---|---|---|---|
| Content strategy | MDX + `gray-matter` frontmatter | Contentlayer (deprecated), Sanity CMS | MDX is zero-cost, version-controlled, no build-time API calls |
| MDX rendering | `@next/mdx` + `next-mdx-remote/rsc` | `remark` only, `mdx-bundler` | `next-mdx-remote/rsc` works natively in App Router Server Components |
| Syntax highlighting | `rehype-pretty-code` + `shiki` | `prism-react-renderer`, `highlight.js` | Zero JS runtime — HTML+CSS only; supports 100+ themes |
| Dark/Light mode | `next-themes` | Manual CSS vars, Tailwind `dark:` only | SSR-safe flash prevention; localStorage persistence built-in |
| Router | App Router (Next.js 15) | Pages Router | App Router is the Next.js 15 default; Server Components reduce bundle |
| Storage | localStorage | Supabase, Airtable | MVP constraint: no backend; localStorage is sufficient for waitlist |
| Fonts | `next/font` (Inter + Sora) | Google Fonts CDN, self-hosted manually | `next/font` is zero-CLS, self-hosted, privacy-preserving |
| Progress bar | Intersection Observer + scroll event | `react-scroll-progress` library | No extra dependency; lightweight custom hook (< 30 lines) |
| Deployment | Vercel (free tier, SSG) | Netlify, GitHub Pages | Vercel has zero-config Next.js support; free SSL + CDN |

---

## Phase 1: Design & Contracts

### Component Architecture

#### Glassmorphism Design Token System (`tailwind.config.ts`)

```ts
// Colours
primary:   { 500: '#6366f1', 600: '#4f46e5' }  // Indigo gradient base
accent:    { 500: '#a855f7', 600: '#9333ea' }   // Purple gradient accent
glass:     { bg: 'rgba(255,255,255,0.05)', border: 'rgba(255,255,255,0.1)' }

// Gradients (defined as background-image utilities)
'gradient-hero':   'linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%)'
'gradient-card':   'linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.15) 100%)'
'gradient-button': 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)'

// Glassmorphism
backdropBlur: { glass: '12px' }
```

#### Reading Progress Bar

Custom hook `useReadingProgress()` — attaches a `scroll` event listener on the `window`,
computes `scrollY / (scrollHeight - innerHeight) * 100`, returns a `number` (0–100).
`ProgressBar.tsx` renders a `<div>` fixed to `top-0` with `width: {progress}%` and a gradient fill.
No external library needed.

#### Table of Contents — Active Section Tracking

Custom hook `useActiveSection(sectionIds: string[])` — uses `IntersectionObserver` with
`rootMargin: '-20% 0px -70% 0px'` to detect which chapter heading is in the viewport.
Returns the active `sectionId` string. `TableOfContents.tsx` applies `font-bold text-primary-500`
to the active entry.

#### MDX Custom Component Map (`MDXContent.tsx`)

```ts
const components = {
  h1: (props) => <h1 className="text-4xl font-bold gradient-text mt-12 mb-4" {...props} />,
  h2: (props) => <h2 className="text-2xl font-semibold mt-8 mb-3" {...props} />,
  code: (props) => <code className="bg-glass rounded px-1.5 py-0.5 text-sm" {...props} />,
  pre:  (props) => <pre className="glass-card overflow-x-auto p-4 rounded-xl my-6" {...props} />,
  Callout: ({ children, type }) => <div className={`callout callout-${type} glass-card`}>{children}</div>,
  ChapterProgress: () => null,  // reserved for future interactive use
}
```

#### WaitlistForm — localStorage Contract

```ts
// Key: 'waitlist'  Value: WaitlistEntry[]
interface WaitlistEntry {
  name: string
  email: string
  message?: string
  submittedAt: string  // ISO 8601
}
```

Validation (client-side only):
- `name`: non-empty string
- `email`: HTML5 email pattern + non-empty
- On success: append to existing array (or create new array if key absent)
- On localStorage unavailable (SecurityError): show success UI + warning banner

---

## Implementation Phases

### Phase 1 — Project Setup (Estimated: 15 min)

**Goal**: Runnable Next.js 15 project with TypeScript strict, Tailwind, shadcn/ui, MDX, and `next-themes`.

Key tasks:
1. `npx create-next-app@latest ai-native-book --typescript --tailwind --app --src-dir=false`
2. Install: `next-themes @next/mdx next-mdx-remote gray-matter rehype-pretty-code shiki`
3. Configure `tailwind.config.ts` — add design tokens (colours, gradients, glass utilities)
4. Configure `next.config.ts` — enable MDX, add security headers
5. Run `npx shadcn@latest init` + add: `button card input label textarea`
6. Add `tsconfig.json` strict check; add `components.json`
7. Create `/types/index.ts` with all shared types
8. Create `.env.example`

**Gate**: `next build` passes with zero TypeScript errors and zero ESLint warnings.

---

### Phase 2 — Layout + Navigation + Theme Provider (Estimated: 20 min)

**Goal**: All four pages accessible with a consistent header, footer, dark/light toggle, and skip link.

Key tasks:
1. `app/layout.tsx` — wrap with `ThemeProvider` (next-themes), load `next/font` fonts, render `<Navbar>` and `<SkipLink>`
2. `components/layout/SkipLink.tsx` — `<a href="#main-content">Skip to main content</a>`, visually hidden until focused
3. `components/layout/Navbar.tsx`:
   - Desktop: horizontal links (Home, Book, About, Contact) + `ThemeToggle` button
   - Mobile: hamburger button → slide-down menu; `aria-expanded` updates on toggle
   - Active link: `usePathname()` comparison → `font-semibold text-primary-500`
4. `components/layout/ThemeToggle.tsx` — icon button, `aria-label="Toggle dark mode"`, Sun/Moon icons
5. `app/globals.css` — CSS variables for light/dark tokens; Tailwind `dark:` class strategy
6. Stub pages: `app/page.tsx`, `app/book/page.tsx`, `app/about/page.tsx`, `app/contact/page.tsx` — each with `<main id="main-content">`

**Gate**: Navigate all 4 pages; dark/light toggle works; hamburger opens/closes; skip link visible on Tab.

---

### Phase 3 — Home Page: Hero + Chapter Cards (Estimated: 25 min)

**Goal**: Premium Home page with gradient hero and glassmorphism chapter preview cards.

Key tasks:
1. `components/home/Hero.tsx`:
   - Full-viewport gradient background (`gradient-hero`)
   - Book title with gradient text clip
   - Subtitle + `<Button>` CTA → `/book`
   - Floating decorative blobs (CSS `@keyframes float` — pure CSS, no JS)
2. `components/home/ChapterCard.tsx`:
   - Glassmorphism card (`backdrop-blur-glass bg-glass border border-glass-border`)
   - Props: `chapterNumber`, `title`, `description`, `slug`
   - Hover: scale + glow (`hover:scale-105 hover:shadow-primary-500/20`)
3. `app/page.tsx` — imports chapter metadata from `lib/mdx.ts`; renders `<Hero>` + grid of 5 `<ChapterCard>`
4. `lib/mdx.ts` — `getAllChapters()`: reads `/content/chapters/*.mdx` with `fs`, parses frontmatter with `gray-matter`, returns sorted `Chapter[]`

**Gate**: Home page shows hero and 5 chapter cards; mobile 320px no overflow; dark/light correct.

---

### Phase 4 — Book Page: MDX + Progress Bar + ToC (Estimated: 35 min)

**Goal**: Full scrollable book with sticky ToC, reading progress bar, and MDX-rendered content.

Key tasks:
1. `lib/mdx.ts` — add `getAllTopics()`: returns all 10 topics sorted by chapter + topic number
2. `hooks/useReadingProgress.ts` — scroll event → 0–100 float
3. `hooks/useActiveSection.ts` — IntersectionObserver → active section ID
4. `components/book/ProgressBar.tsx` — fixed top bar, gradient fill, `role="progressbar"` ARIA
5. `components/book/TableOfContents.tsx`:
   - Desktop (≥ 768px): sticky left sidebar, chapter headings + topic sub-items, active highlight
   - Mobile (< 768px): fixed bottom-right `Contents` button → full-screen overlay panel
6. `components/book/MDXContent.tsx` — `next-mdx-remote/rsc` `<MDXRemote>` with custom component map
7. `components/book/ChapterSection.tsx` — wraps each chapter: heading with anchor ID, renders topics
8. `app/book/page.tsx` — Server Component; loads all topics; renders `<ProgressBar>`, `<ToC>`, `<ChapterSection>` × 5

**Gate**: All 10 MDX topics render; progress bar tracks scroll; ToC highlights active; smooth scroll on click.

---

### Phase 5 — About + Contact Pages (Estimated: 20 min)

**Goal**: Author bio page and working waitlist form.

Key tasks:
1. `components/about/AuthorCard.tsx` — glassmorphism card: `next/image` avatar, name, bio, mission quote
2. `app/about/page.tsx` — renders `<AuthorCard>` with placeholder bio text
3. `lib/localStorage.ts` — `saveWaitlistEntry(entry)` / `getWaitlist()` with try/catch for blocked storage
4. `components/contact/WaitlistForm.tsx`:
   - Controlled inputs: Name (required), Email (required + pattern), Message (optional)
   - Client component (`'use client'`)
   - On submit: validate → `saveWaitlistEntry()` → swap to success state
   - On localStorage error: success state + `<Alert>` warning
   - All inputs: `<label>` association, `aria-required`, `aria-describedby` for errors
5. `app/contact/page.tsx` — renders page header + `<WaitlistForm>`

**Gate**: Form saves to localStorage; validation prevents bad submission; keyboard-only navigation works.

---

### Phase 6 — Content: 5 Chapters × 2 Topics in MDX (Estimated: 30 min)

**Goal**: All 10 MDX files with real book content on AI-Native Driven Development.

MDX file structure (each file):

```mdx
---
chapterNumber: 1
topicNumber: 1
title: "What is AI-Native Development?"
description: "Defining the paradigm shift from AI-assisted to AI-native software engineering."
slug: "chapter-01-topic-01"
---

## [Topic Title]

[Content...]
```

**Chapter plan**:

| Chapter | Title | Topic 1 | Topic 2 |
|---|---|---|---|
| 1 | The AI-Native Paradigm | What is AI-Native Development? | AI-Assisted vs AI-Native: The Fundamental Difference |
| 2 | Designing with AI | Spec-Driven Development with AI | Prompt Engineering as a First-Class Skill |
| 3 | Building AI-Native Systems | Architecture Patterns for AI-Native Apps | Data Pipelines and Model Integration |
| 4 | Shipping and Scaling | Testing AI-Native Features | Monitoring, Observability, and Feedback Loops |
| 5 | The Future of AI-Native Development | Emerging Patterns and Tools | Building Your AI-Native Team and Culture |

**Gate**: `getAllChapters()` returns 5 chapters; `getAllTopics()` returns 10 topics; Book page renders all.

---

### Phase 7 — Polish + Deploy (Estimated: 15 min)

**Goal**: Lighthouse ≥ 90 on all metrics; live Vercel URL.

Key tasks:
1. **Performance audit** — run Lighthouse locally; fix any FCP / bundle issues
2. **Accessibility audit** — run `axe` browser extension; fix any ARIA gaps
3. **Responsive QA** — test at 320px, 768px, 1440px in Chrome DevTools; dark + light modes
4. **`next.config.ts`** — add security headers (X-Frame-Options, CSP, HSTS)
5. **`vercel.json`** — add redirect `/` → keep; ensure 404 page exists
6. **Deploy**:
   - `git push origin 1-book-website`
   - Connect repo to Vercel → auto-deploy
   - Confirm live URL returns HTTP 200 on all 4 pages
7. **`README.md`** — local dev setup, deploy instructions, content update guide

**Gate**: Vercel deployment live; all 4 pages return 200; Lighthouse perf ≥ 90, a11y ≥ 90.

---

## Risk Analysis

| Risk | Blast Radius | Mitigation |
|---|---|---|
| `next-mdx-remote` RSC compatibility with Next.js 15 | High — Book page breaks | Pin `next-mdx-remote@^4`; test during Phase 4; fallback to `@next/mdx` with static import |
| `rehype-pretty-code` + Shiki increasing bundle size | Medium — bundle budget miss | Use `bundleAnalyzer`; Shiki loads themes lazily; use `transformers` only for needed languages |
| localStorage blocked in private/strict browser mode | Low — waitlist only | Try/catch already planned in `lib/localStorage.ts`; graceful degradation with warning UI |
| Vercel free tier cold start on first load | Low — static site, no functions | SSG ensures no cold starts; all pages are pre-rendered HTML |
| Glassmorphism `backdrop-filter` unsupported on older browsers | Low — cosmetic only | CSS `@supports` fallback: solid semi-transparent background when `backdrop-filter` unavailable |

---

## Non-Functional Requirements Traceability

| NFR | Target | Implementation |
|---|---|---|
| FCP | < 1.5s | SSG + `next/font` + `next/image` + no render-blocking JS |
| Bundle | < 150KB gzip | Server Components; rehype-pretty-code (zero runtime); tree-shaking |
| Lighthouse Perf | ≥ 90 | SSG; lazy images; font-display: swap via next/font |
| Lighthouse A11y | ≥ 90 | Skip links; ARIA labels; semantic HTML; focus rings; WCAG contrast tokens |
| WCAG 2.1 AA | 4.5:1 contrast | Design tokens validated in Tailwind config; both dark + light |
| Responsive | 320 / 768 / 1440px | Mobile-first Tailwind; tested in all 3 breakpoints before deploy |
| TypeScript | strict: true | Enforced in tsconfig; CI build gate |
| Deploy | Vercel free | `next build` → Vercel auto-deploy from `main`; no paid add-ons |
