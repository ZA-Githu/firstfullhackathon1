# Tasks: AI-Native Book Website

**Input**: Design documents from `/specs/1-book-website/`
**Prerequisites**: plan.md ✅ · spec.md ✅ · research.md ✅ · data-model.md ✅ · contracts/ ✅
**Branch**: `1-book-website`
**Date**: 2026-03-06
**Total Tasks**: 68

**Format**: `- [ ] [ID] [P?] [Story?] Description — file path`
- **[P]** = parallelizable (no dependency on an incomplete peer task, different file)
- **[US#]** = maps to user story in spec.md

---

## Phase 1: Setup — Project Initialization

**Purpose**: Bootstrap the Next.js 15 project with all dependencies, config, and shared types.
**No user story label** — these tasks block everything else.

- [x] T001 Initialize Next.js 15 project with TypeScript, Tailwind, App Router, no src-dir — run `npx create-next-app@latest . --typescript --tailwind --app --src-dir=false --import-alias="@/*"` in `ai-native-book/`
- [x] T002 Install MDX + content dependencies — run `npm install next-mdx-remote gray-matter rehype-pretty-code shiki` in `ai-native-book/`
- [x] T003 Install theme dependency — run `npm install next-themes` in `ai-native-book/`
- [x] T004 Initialize shadcn/ui — run `npx shadcn@latest init` (choose: Default style, Slate base, CSS variables yes)
- [x] T005 [P] Add shadcn/ui components — run `npx shadcn@latest add button card input label textarea`
- [x] T006 Configure `next.config.ts` — enable MDX (`pageExtensions: ['ts','tsx','mdx']`, `experimental.mdxRs: true`), add security headers (`X-Frame-Options`, `X-Content-Type-Options`) — file: `next.config.ts`
- [x] T007 Configure `tailwind.config.ts` — add design tokens: primary/accent colour palette, `gradient-hero`/`gradient-card`/`gradient-button` as `backgroundImage` utilities, `glass` backdrop blur value, `glass-bg`/`glass-border` colours, `fontFamily` for Inter + Sora — file: `tailwind.config.ts`
- [x] T008 [P] Configure `tsconfig.json` — verify `strict: true`; add path alias `@/*` → `./*` — file: `tsconfig.json`
- [x] T009 [P] Create shared TypeScript types — `Chapter`, `Topic`, `WaitlistEntry`, `UserPreference` interfaces matching data-model.md — file: `types/index.ts`
- [x] T010 [P] Create `.env.example` — document `NEXT_PUBLIC_SITE_URL`; copy to `.env.local` — files: `.env.example`, `.env.local`
- [x] T011 [P] Create `lib/utils.ts` — implement `cn()` classname merge helper using `clsx` + `tailwind-merge`; install deps: `npm install clsx tailwind-merge` — file: `lib/utils.ts`
- [x] T012 Create `app/globals.css` — CSS variables for light/dark theme tokens (background, foreground, card, border, ring colours); Tailwind `@layer base` resets; `dark` class strategy — file: `app/globals.css`
- [x] T013 [P] Create content directory and 10 MDX stub files — `mkdir -p content/chapters`; create all 10 files (`chapter-01-topic-01.mdx` through `chapter-05-topic-02.mdx`) with correct frontmatter and placeholder body — files: `content/chapters/chapter-0{1-5}-topic-0{1-2}.mdx`

**Checkpoint ✅ Phase 1 complete**: `npm run build` passes with zero TypeScript errors and zero ESLint warnings. All 10 MDX stubs exist with valid frontmatter.

---

## Phase 2: Foundational — Layout + Shared Infrastructure

**Purpose**: Root layout, navigation, theme provider, skip link, and MDX loader that ALL user stories depend on.
**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete.

- [x] T014 Create `lib/mdx.ts` — implement `getAllChapters(): Promise<Chapter[]>` (reads `/content/chapters/*.mdx`, parses frontmatter with `gray-matter`, sorts by `chapterNumber`) and `getAllTopics(): Promise<Topic[]>` (returns all 10 topics sorted by chapter then topic); generate `anchorId` as `ch{C}-t{T}` — file: `lib/mdx.ts`
- [x] T015 [P] Create `lib/localStorage.ts` — implement `saveWaitlistEntry()` (append to `waitlist` key, return `{success}` or `{success: false, storageBlocked: true}`) and `getWaitlist(): WaitlistEntry[]` (return `[]` on error/absent); full try/catch for `SecurityError` — file: `lib/localStorage.ts`
- [x] T016 [P] Create `components/layout/SkipLink.tsx` — `<a href="#main-content">Skip to main content</a>`; visually hidden via `sr-only` until focused; uses focus ring on `:focus-visible` — file: `components/layout/SkipLink.tsx`
- [x] T017 Create `components/layout/ThemeToggle.tsx` — client component; uses `useTheme()` from `next-themes`; renders Sun icon (light) / Moon icon (dark); `aria-label="Toggle dark mode"`; keyboard operable — file: `components/layout/ThemeToggle.tsx`
- [x] T018 Create `components/layout/Navbar.tsx` — client component; uses `usePathname()` for active link; desktop: horizontal links (Home, Book, About, Contact) + `<ThemeToggle>`; mobile: hamburger button with `aria-expanded`, slide-down menu; `<nav aria-label="Main navigation">`; active link: `font-semibold text-primary-500`; glassmorphism `backdrop-blur-sm bg-white/80 dark:bg-slate-900/80` — file: `components/layout/Navbar.tsx`
- [x] T019 Create `components/layout/Footer.tsx` — minimal footer with site name, year, and "Built with Next.js" credit; responsive — file: `components/layout/Footer.tsx`
- [x] T020 Create `app/layout.tsx` — root layout; import `next/font/google` Inter + Sora; wrap with `<ThemeProvider attribute="class" defaultTheme="system" enableSystem>`; render `<SkipLink>`, `<Navbar>`, `<main id="main-content">`, `<Footer>`; apply font CSS variables — file: `app/layout.tsx`
- [x] T021 [P] Create stub pages for all 4 routes — each with `<main id="main-content">` and a placeholder heading: `app/page.tsx`, `app/book/page.tsx`, `app/about/page.tsx`, `app/contact/page.tsx`

**Checkpoint ✅ Phase 2 complete**: Navigate all 4 routes at `localhost:3000`. Dark/light toggle works without flash. Hamburger opens/closes on mobile. Skip link appears on first Tab press. `lib/mdx.ts` unit-testable: `getAllChapters()` returns 5 items with 2 topics each.

---

## Phase 3: User Story 1 — First-Time Visitor Discovers the Book (P1)

**Goal**: Premium Home page with gradient hero, glassmorphism chapter cards, and a working CTA linking to `/book`.

**Independent Test**: Navigate to `/`. Hero visible without scroll (1440px viewport). 5 chapter cards render below hero. CTA → `/book` works. Mobile 320px: no overflow. Dark mode: cards remain visible.

### Implementation — User Story 1

- [x] T022 [US1] Create `components/home/Hero.tsx` — full-viewport gradient hero (`bg-gradient-to-br from-primary-600 via-accent-500 to-pink-500`); book title with CSS gradient text clip (`bg-clip-text text-transparent bg-gradient-to-r ...`); subtitle; `<Button asChild><Link href="/book">Start Reading →</Link></Button>`; floating decorative CSS blobs via `@keyframes float` in globals.css; responsive padding at 320px/768px/1440px — file: `components/home/Hero.tsx`
- [x] T023 [P] [US1] Create `components/home/ChapterCard.tsx` — glassmorphism card (`backdrop-blur-sm bg-white/10 dark:bg-white/5 border border-white/20 rounded-2xl`); props: `{ chapterNumber, title, description, slug }`; chapter number badge with gradient; hover: `hover:scale-105 hover:shadow-lg hover:shadow-primary-500/20 transition-all duration-300`; `<Link href={/book#ch${chapterNumber}-t1}>` — file: `components/home/ChapterCard.tsx`
- [x] T024 [US1] Implement `app/page.tsx` — Server Component; calls `getAllChapters()` from `lib/mdx.ts`; renders `<Hero>` then responsive grid of 5 `<ChapterCard>` (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`); section with `aria-label="Book chapters"` — file: `app/page.tsx`
- [x] T025 [P] [US1] Add CSS animation keyframes to `app/globals.css` — `@keyframes float` for hero decorative blobs; `@keyframes fadeInUp` for staggered card entrance — file: `app/globals.css`

**Checkpoint ✅ US1 complete**: Home page renders hero + 5 chapter cards. All cards link into the book. Mobile 320px clean. Dark/light correct. `npm run build` clean.

---

## Phase 4: User Story 2 — Reader Reads the Full Book (P1)

**Goal**: Full Book page with sticky ToC, real-time reading progress bar, smooth-scroll chapter navigation, and MDX-rendered content with syntax highlighting.

**Independent Test**: Navigate to `/book`. ToC shows 5 chapters + 10 topics. Click Chapter 3 → smooth scroll. Scroll to bottom → progress bar reaches 100%. All MDX content renders. Code blocks have syntax highlighting. Mobile: "Contents" button shows overlay ToC.

### Implementation — User Story 2

- [x] T026 [US2] Create `hooks/useReadingProgress.ts` — `'use client'` hook; attaches `scroll` event listener on `window`; computes `Math.round((scrollY / (scrollHeight - innerHeight)) * 100)`; throttles via `requestAnimationFrame`; cleans up on unmount; returns `number` 0–100 — file: `hooks/useReadingProgress.ts`
- [x] T027 [US2] Create `hooks/useActiveSection.ts` — `'use client'` hook; accepts `sectionIds: string[]`; creates `IntersectionObserver` with `rootMargin: '-20% 0px -70% 0px'`; observes each `document.getElementById(id)`; returns active section ID string; cleans up on unmount — file: `hooks/useActiveSection.ts`
- [x] T028 [P] [US2] Create `components/book/ProgressBar.tsx` — `'use client'`; calls `useReadingProgress()`; renders `<div role="progressbar" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100} aria-label="Reading progress">`; fixed `top-0 left-0 h-1 z-50`; gradient fill `bg-gradient-to-r from-primary-500 to-accent-500`; width = `${progress}%`; smooth transition `transition-[width] duration-100` — file: `components/book/ProgressBar.tsx`
- [x] T029 [US2] Create `components/book/TableOfContents.tsx` — `'use client'`; props: `{ chapters: Chapter[] }`; calls `useActiveSection()` with all 10 anchor IDs; desktop (≥ md): sticky left sidebar `sticky top-20 max-h-[calc(100vh-5rem)] overflow-y-auto`; mobile: fixed bottom-right `Contents` button → full-screen overlay `<dialog>` with `aria-modal="true"`; active entry: `font-semibold text-primary-500`; each link: `<a href={#anchorId}>` triggers smooth scroll via CSS `scroll-behavior: smooth` on `<html>` — file: `components/book/TableOfContents.tsx`
- [x] T030 [P] [US2] Create `components/book/MDXContent.tsx` — Server Component; uses `MDXRemote` from `next-mdx-remote/rsc`; custom component map for `h1`, `h2`, `h3`, `p`, `code`, `pre`, `blockquote`, `ul`, `ol`, `li`; custom `Callout` component (props: `type: 'info'|'warning'|'tip'`); `rehype-pretty-code` configured as rehype plugin with `theme: { dark: 'github-dark', light: 'github-light' }` using CSS variables — file: `components/book/MDXContent.tsx`
- [x] T031 [P] [US2] Create `components/book/ChapterSection.tsx` — Server Component; props: `{ chapter: Chapter }`; renders chapter heading with `id={chapter.topics[0].anchorId.replace('-t1','')}` anchor; then maps `chapter.topics` each with `id={topic.anchorId}` anchor heading and `<MDXContent source={topic.content}>` — file: `components/book/ChapterSection.tsx`
- [x] T032 [US2] Add `getTopicContent(slug)` to `lib/mdx.ts` — reads single MDX file by slug, returns raw MDX string for `MDXRemote`; update `getAllTopics()` to include `content` field — file: `lib/mdx.ts`
- [x] T033 [US2] Implement `app/book/page.tsx` — Server Component; calls `getAllChapters()` to get all chapters + topics with content; returns layout: `<ProgressBar>` (client), sidebar `<TableOfContents chapters={chapters}>` (client), main content area `<ChapterSection>` × 5; `scroll-behavior: smooth` on html element via globals.css; responsive two-column layout: `grid grid-cols-1 md:grid-cols-[260px_1fr]` — file: `app/book/page.tsx`
- [x] T034 [P] [US2] Add `scroll-behavior: smooth` and prose typography styles to `app/globals.css` — prose max-width, line-height, heading margins, blockquote style, code block font size — file: `app/globals.css`
- [x] T035 [P] [US2] Handle empty MDX content — update `components/book/ChapterSection.tsx` to render "Coming soon" placeholder when topic content body is empty — file: `components/book/ChapterSection.tsx`

**Checkpoint ✅ US2 complete**: Book page loads all 10 topics. Progress bar animates on scroll (100% at bottom). ToC highlights active section. Clicking any ToC entry smooth-scrolls. Code blocks highlighted. Mobile "Contents" button works. `npm run build` clean.

---

## Phase 5: User Story 3 — Visitor Learns About the Author (P2)

**Goal**: About page with author bio, profile image, vision statement, and consistent design.

**Independent Test**: Navigate to `/about`. Author name, image with alt text, and biography visible. 768px viewport: image and bio stack vertically. Screen reader: image has meaningful alt text. Dark mode: correct.

### Implementation — User Story 3

- [x] T036 [P] [US3] Add placeholder author image — copy a placeholder image to `public/author.jpg` (create 400×400px placeholder if no real photo yet) — file: `public/author.jpg`
- [x] T037 [US3] Create `components/about/AuthorCard.tsx` — glassmorphism card; `next/image` with `src="/author.jpg"`, `alt="[Author name], author of AI-Native Driven Development"`, `width={160}`, `height={160}`, `priority`; author name `<h2>`; biography `<p>` block; mission quote in `<blockquote>`; responsive: `flex flex-col md:flex-row gap-8` — file: `components/about/AuthorCard.tsx`
- [x] T038 [US3] Implement `app/about/page.tsx` — Server Component; renders page header (title + subtitle); `<AuthorCard>` with author data (hardcoded placeholder until real bio provided); vision section below card — file: `app/about/page.tsx`

**Checkpoint ✅ US3 complete**: About page renders author card. Image loads with correct alt text. Mobile: vertical stack. Dark mode: correct.

---

## Phase 6: User Story 4 — Visitor Joins the Waitlist (P2)

**Goal**: Contact page with a validated waitlist form that saves to localStorage and handles storage errors gracefully.

**Independent Test**: Navigate to `/contact`. Fill name + valid email → submit → success message shown → entry in `localStorage['waitlist']`. Submit with empty email → inline error, no submission. Tab through form → all fields + button reachable with visible focus rings.

### Implementation — User Story 4

- [x] T039 [US4] Create `components/contact/WaitlistForm.tsx` — `'use client'`; controlled inputs for `name` (required), `email` (required, pattern validation), `message` (optional); form state: `idle | validating | saving | success | success_with_warning`; on submit: validate → `saveWaitlistEntry()` → set state; inline error messages with `id` for `aria-describedby`; `aria-required="true"` on required fields; each input associated with `<label htmlFor>`; submit button: gradient + disabled while saving; success state: replace form with confirmation card "You're on the list! 🎉"; warning banner if storage blocked — file: `components/contact/WaitlistForm.tsx`
- [x] T040 [P] [US4] Implement `app/contact/page.tsx` — Server Component; renders page header ("Join the Waitlist"), brief description of what the waitlist is for, and `<WaitlistForm>` inside a centred glassmorphism card — file: `app/contact/page.tsx`
- [x] T041 [P] [US4] Verify `lib/localStorage.ts` edge cases — ensure `saveWaitlistEntry()` correctly handles: (a) first-ever save (key absent), (b) appending to existing array, (c) `SecurityError` thrown by browser — file: `lib/localStorage.ts`

**Checkpoint ✅ US4 complete**: Waitlist form saves to localStorage. Validation prevents invalid submission. Keyboard navigation works. Storage-blocked scenario shows warning. `npm run build` clean.

---

## Phase 7: User Story 5 — Dark / Light Mode Across All Pages (P2)

**Goal**: Dark/light mode persisted in localStorage, OS-preference detected on first load, toggle in navbar on all pages.

**Independent Test**: Load site with OS dark → site is dark (no flash). Toggle → light. Refresh → stays light. Toggle keyboard accessible. WCAG contrast passes in both modes.

### Implementation — User Story 5

*Note: Core `next-themes` setup was done in T003 + T017 + T020 (Phase 1–2). Tasks here are verification and contrast compliance.*

- [x] T042 [US5] Verify no FOIT (flash of incorrect theme) — confirm `<ThemeProvider>` is in `app/layout.tsx` with `attribute="class" enableSystem disableTransitionOnChange`; test by hard-refreshing with OS set to dark mode in Chrome — file: `app/layout.tsx`
- [x] T043 [P] [US5] Audit colour contrast in both modes — check all text/background combinations in `tailwind.config.ts` against WCAG 2.1 AA (4.5:1 normal text, 3:1 large text); fix any failing tokens — file: `tailwind.config.ts`
- [x] T044 [P] [US5] Verify dark mode on glassmorphism components — manually test `Hero.tsx`, `ChapterCard.tsx`, `Navbar.tsx`, `WaitlistForm.tsx` in dark mode; ensure cards remain visually distinct (no invisible borders or blending with background) — files: `components/home/Hero.tsx`, `components/home/ChapterCard.tsx`
- [x] T045 [P] [US5] Test toggle keyboard accessibility — confirm `ThemeToggle.tsx` is reachable via Tab; activatable via Enter/Space; `aria-label` announces correctly in VoiceOver/NVDA — file: `components/layout/ThemeToggle.tsx`

**Checkpoint ✅ US5 complete**: Dark/light works flawlessly. No flash on load. OS preference respected. localStorage persists. WCAG contrast passes. Toggle keyboard accessible.

---

## Phase 8: Content — 5 Chapters × 2 Topics (All User Stories)

**Goal**: Replace MDX stub files with real, substantial book content for all 10 topics.

**Independent Test**: `getAllTopics()` returns 10 topics each with non-empty `content`. Book page renders all 10 topics with headings, paragraphs, code examples, and callouts. ToC shows correct titles.

- [x] T046 [US2] Write `content/chapters/chapter-01-topic-01.mdx` — Chapter 1, Topic 1: "What is AI-Native Development?" — define AI-Native paradigm, contrast with traditional dev, 3 core attributes; include 1 code example, 1 Callout — file: `content/chapters/chapter-01-topic-01.mdx`
- [x] T047 [P] [US2] Write `content/chapters/chapter-01-topic-02.mdx` — Chapter 1, Topic 2: "AI-Assisted vs AI-Native: The Fundamental Difference" — spectrum diagram (ASCII), comparison table in MDX, real-world examples — file: `content/chapters/chapter-01-topic-02.mdx`
- [x] T048 [P] [US2] Write `content/chapters/chapter-02-topic-01.mdx` — Chapter 2, Topic 1: "Spec-Driven Development with AI" — the /sp.specify workflow, why specs before code, example prompt + spec output — file: `content/chapters/chapter-02-topic-01.mdx`
- [x] T049 [P] [US2] Write `content/chapters/chapter-02-topic-02.mdx` — Chapter 2, Topic 2: "Prompt Engineering as a First-Class Skill" — anatomy of a good prompt, chain-of-thought, few-shot examples, common failure modes — file: `content/chapters/chapter-02-topic-02.mdx`
- [x] T050 [P] [US2] Write `content/chapters/chapter-03-topic-01.mdx` — Chapter 3, Topic 1: "Architecture Patterns for AI-Native Apps" — RAG, agent loops, tool use, context windows; diagram in ASCII; code skeleton example — file: `content/chapters/chapter-03-topic-01.mdx`
- [x] T051 [P] [US2] Write `content/chapters/chapter-03-topic-02.mdx` — Chapter 3, Topic 2: "Data Pipelines and Model Integration" — embedding pipelines, vector stores, structured output, typed function calls — file: `content/chapters/chapter-03-topic-02.mdx`
- [x] T052 [P] [US2] Write `content/chapters/chapter-04-topic-01.mdx` — Chapter 4, Topic 1: "Testing AI-Native Features" — non-determinism challenge, golden-set evals, contract tests for LLM outputs — file: `content/chapters/chapter-04-topic-01.mdx`
- [x] T053 [P] [US2] Write `content/chapters/chapter-04-topic-02.mdx` — Chapter 4, Topic 2: "Monitoring, Observability, and Feedback Loops" — tracing AI calls, latency budgets, user feedback flywheel, cost monitoring — file: `content/chapters/chapter-04-topic-02.mdx`
- [x] T054 [P] [US2] Write `content/chapters/chapter-05-topic-01.mdx` — Chapter 5, Topic 1: "Emerging Patterns and Tools" — agents-as-OS, multimodal inputs, code generation maturity curve, what's next — file: `content/chapters/chapter-05-topic-01.mdx`
- [x] T055 [P] [US2] Write `content/chapters/chapter-05-topic-02.mdx` — Chapter 5, Topic 2: "Building Your AI-Native Team and Culture" — hiring for AI-native mindset, pairing humans + AI, culture of documentation, measuring AI ROI — file: `content/chapters/chapter-05-topic-02.mdx`

**Checkpoint ✅ Phase 8 complete**: All 10 MDX files have real content. `npm run build` clean. Book page renders full book with no "Coming soon" placeholders.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Performance, accessibility, responsive QA, and deploy.

- [x] T056 Add `<head>` metadata to all 4 pages — `export const metadata: Metadata` with `title`, `description`, `openGraph` for each page: `app/page.tsx`, `app/book/page.tsx`, `app/about/page.tsx`, `app/contact/page.tsx`
- [x] T057 [P] Add 404 page — `app/not-found.tsx` — friendly message + link back to Home; glassmorphism card; matches site design — file: `app/not-found.tsx`
- [x] T058 [P] Run Lighthouse Performance audit — open Chrome DevTools → Lighthouse → generate report for `/`, `/book`, `/about`, `/contact`; target ≥ 90 Performance; fix any issues (image sizes, render-blocking scripts, font loading)
- [x] T059 [P] Run Lighthouse Accessibility audit — Lighthouse + axe browser extension on all 4 pages; target ≥ 90; fix any ARIA gaps, missing labels, contrast failures
- [x] T060 [P] Responsive QA — test all 4 pages at 320px, 768px, 1440px in Chrome DevTools device emulation; dark + light modes; fix any overflow, text clipping, or layout breaks
- [x] T061 [P] Bundle size audit — run `ANALYZE=true npm run build` with `@next/bundle-analyzer`; confirm total JS < 150KB gzip; if over budget: investigate with `npx source-map-explorer`
- [x] T062 [P] Keyboard navigation audit — Tab through entire site; verify skip link, nav links, book ToC, form fields, theme toggle all reachable and activatable; visible focus rings present everywhere
- [x] T063 Add `vercel.json` — configure redirect for trailing slash (`/book/` → `/book`); add `Cache-Control` header for static assets — file: `vercel.json`
- [x] T064 [P] Create `README.md` — local dev setup (npm install + npm run dev), content update guide (add MDX file → rebuild), deploy instructions, Lighthouse score badges — file: `README.md`
- [x] T065 [P] Final `npm run build` + `npm run lint` — zero TypeScript errors; zero ESLint warnings; all pages pre-rendered as SSG (static HTML in `.next/`)
- [x] T066 Push branch and deploy to Vercel — `git add . && git commit -m "feat: complete AI-Native book website"` → `git push origin 1-book-website`; connect repo to Vercel → Deploy; confirm live URL returns HTTP 200 on `/`, `/book`, `/about`, `/contact`
- [x] T067 [P] Verify live deployment — open live Vercel URL in incognito browser; dark mode toggle works; waitlist form saves; Book page loads all 10 topics; progress bar functional; confirm SC-011 (live within 30 min) achieved
- [x] T068 [P] Create `specs/1-book-website/checklists/deployment.md` — post-deploy verification checklist: 4 pages return 200, Lighthouse ≥ 90, form saves to localStorage, dark mode persists, mobile 320px clean — file: `specs/1-book-website/checklists/deployment.md`

**Checkpoint ✅ Phase 9 complete**: Site live on Vercel. All 4 pages return 200. Lighthouse perf ≥ 90, a11y ≥ 90. Bundle < 150KB. Zero TS/ESLint errors. Constitution fully satisfied.

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    └── Phase 2 (Foundational) ← BLOCKS ALL user stories
            ├── Phase 3 (US1 — Home page)         ← can start after Phase 2
            ├── Phase 4 (US2 — Book page)          ← can start after Phase 2
            ├── Phase 5 (US3 — About page)         ← can start after Phase 2
            ├── Phase 6 (US4 — Contact page)       ← can start after Phase 2
            └── Phase 7 (US5 — Dark mode)          ← can start after Phase 2
                    └── Phase 8 (Content/MDX)      ← can start after Phase 4 (Book page)
                            └── Phase 9 (Polish)   ← starts after all US phases complete
```

### Within-Phase Critical Paths

- **Phase 2**: T014 (mdx.ts) must complete before T024/T033 (Home + Book pages)
- **Phase 4**: T026 (useReadingProgress) → T028 (ProgressBar); T027 (useActiveSection) → T029 (ToC); T032 (getTopicContent) → T033 (book page.tsx)
- **Phase 6**: T039 (WaitlistForm) → T041 (localStorage verify)

### User Story Independence

- **US1 (Home)**: Independent after Phase 2. No dependency on US2–5.
- **US2 (Book)**: Independent after Phase 2. `lib/mdx.ts` shared with US1 (T014, Phase 2).
- **US3 (About)**: Fully independent after Phase 2.
- **US4 (Contact)**: Fully independent after Phase 2. `lib/localStorage.ts` (T015, Phase 2) is shared.
- **US5 (Dark mode)**: Core setup in Phase 1–2 (T003, T017, T020). Phase 7 is verification only.

---

## Parallel Opportunities

```bash
# Phase 1 — run together:
T005 (shadcn components) | T008 (tsconfig) | T009 (types) | T010 (.env) | T011 (utils) | T013 (MDX stubs)

# Phase 2 — run together:
T014 (lib/mdx.ts) | T015 (lib/localStorage.ts) | T016 (SkipLink)

# Phase 4 (Book page) — run together after T026/T027:
T028 (ProgressBar) | T029 (ToC) | T030 (MDXContent) | T031 (ChapterSection)

# Phase 8 (Content) — ALL parallel after T046:
T047 | T048 | T049 | T050 | T051 | T052 | T053 | T054 | T055

# Phase 9 (Polish) — run together:
T057 | T058 | T059 | T060 | T061 | T062 | T064 | T065
```

---

## Implementation Strategy

### MVP (minimum live site — User Stories 1 + 2 only)

1. ✅ Complete Phase 1 (Setup)
2. ✅ Complete Phase 2 (Foundational)
3. ✅ Complete Phase 3 (US1 — Home page)
4. ✅ Complete Phase 4 (US2 — Book page)
5. ✅ Complete Phase 8 (Content — at least Chapter 1 stubs)
6. **STOP & VALIDATE**: Home + Book pages fully functional
7. Push + deploy → live URL (SC-011)

### Incremental Delivery

1. Setup + Foundational → shared foundation
2. + US1 Home → hero + chapter cards visible
3. + US2 Book → full reading experience
4. + US3 About → author trust-building
5. + US4 Contact → lead capture
6. + US5 Dark mode verify → confirmed cross-page
7. + Content → all 10 MDX files with real content
8. + Polish → Lighthouse ≥ 90, deploy

---

## Notes

- `[P]` tasks write to different files; launch them together to maximise speed
- Every task has an exact file path — no ambiguity for LLM execution
- `npm run build` MUST pass after every phase checkpoint before continuing
- Content tasks (Phase 8) are all `[P]` — all 10 MDX files can be written simultaneously
- No test tasks generated (not requested in spec); acceptance scenarios from spec.md serve as manual test scripts
