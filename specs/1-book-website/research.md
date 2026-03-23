# Research: AI-Native Book Website

**Phase**: 0 — Outline & Research
**Date**: 2026-03-06
**Feature**: 1-book-website

All decisions below were derived from the feature spec, the project constitution,
and best-practice evaluation of available options. Zero NEEDS CLARIFICATION markers remain.

---

## Decision 1: MDX Content Strategy

**Decision**: Use MDX files in `/content/chapters/` parsed with `gray-matter` for frontmatter
and rendered via `next-mdx-remote/rsc` Server Components.

**Rationale**:
- MDX files are version-controlled alongside code — no external CMS dependency.
- `gray-matter` is the most widely used frontmatter parser (28M weekly downloads); zero risk.
- `next-mdx-remote/rsc` supports React Server Components natively in Next.js 15 App Router,
  keeping MDX rendering on the server and producing zero client JS for content.
- Auto-discovery via `fs.readdirSync('/content/chapters/')` at build time means adding a file
  automatically updates the ToC — satisfying FR-004 and SC-010.

**Alternatives considered**:
- **Contentlayer**: Deprecated in 2024; community fork (contentlayer2) has uncertain future.
- **Sanity / Contentful**: CMS adds cost, API dependency, auth complexity — violates Non-Goal "no backend".
- **`@next/mdx` only**: Works for static imports but cannot dynamically load from `fs` at runtime in
  App Router Server Components without a wrapper — `next-mdx-remote/rsc` is the right primitive.
- **`mdx-bundler`**: Requires esbuild at runtime; adds to bundle; more complex setup for no gain here.

---

## Decision 2: Syntax Highlighting

**Decision**: `rehype-pretty-code` with `shiki` as the highlighter.

**Rationale**:
- `rehype-pretty-code` runs at **build time** (in the MDX pipeline) — it emits styled HTML, not
  runtime JS. This means zero JavaScript is shipped to the client for syntax highlighting.
- Supports 100+ languages and themes; theme can match the dark/light mode via CSS variables.
- Integrates directly as a `rehypePlugin` in the `next-mdx-remote` options — no extra component needed.
- Keeps the JavaScript bundle under the 150KB budget (constitution Principle IV).

**Alternatives considered**:
- **`prism-react-renderer`**: Ships a runtime JS bundle; requires a client component wrapper.
- **`highlight.js`**: Runtime JS; larger bundle; less popular in the Next.js MDX ecosystem.
- **Plain `<code>` with CSS**: No language-aware coloring — unacceptable for a "premium" book.

---

## Decision 3: Dark / Light Mode

**Decision**: `next-themes` library.

**Rationale**:
- `next-themes` handles the SSR flash-of-incorrect-theme (FOIT) problem via a script injected
  into `<head>` before React hydration. Without it, dark-mode pages flash white on load.
- Built-in `localStorage` persistence and `prefers-color-scheme` OS detection.
- Works with Tailwind's `class` dark mode strategy — add `darkMode: 'class'` to `tailwind.config.ts`.
- Tiny bundle (~2KB gzip). Satisfies constitution Principle VII completely.
- `aria-label` and keyboard operability on the toggle button is implemented manually in `ThemeToggle.tsx`.

**Alternatives considered**:
- **Manual CSS variables + `useEffect`**: Causes hydration mismatch and FOIT without the head script trick.
- **Tailwind `media` strategy**: Cannot persist user preference; always follows OS — fails FR-017.
- **`react-dark-mode-toggle`**: External UI component — violates constitution Principle I.

---

## Decision 4: Reading Progress Bar

**Decision**: Custom hook `useReadingProgress()` using native `scroll` event + `window` measurements.

**Rationale**:
- 25 lines of TypeScript; zero dependencies; satisfies SC-003 (updates within 100ms of scroll).
- Formula: `(scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100`
- `requestAnimationFrame` throttle prevents jank.
- Renders as a `<div role="progressbar" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>`
  for screen reader compatibility (constitution Principle V).

**Alternatives considered**:
- **`react-scroll-progress` npm package**: Adds a dependency for code trivially written in-house.
- **`framer-motion` progress**: Pulls in framer-motion (~60KB) — exceeds bundle budget.

---

## Decision 5: Table of Contents Active Tracking

**Decision**: `IntersectionObserver` with `rootMargin: '-20% 0px -70% 0px'`.

**Rationale**:
- The rootMargin shrinks the observable viewport so only the section in the "reading zone"
  (roughly the upper-middle of the screen) is marked active — feels natural to readers.
- Zero dependencies; supported in all modern browsers (Chrome 51+, Firefox 55+, Safari 12.1+).
- More performant than `scroll` + `getBoundingClientRect()` polling — runs off the main thread.

**Alternatives considered**:
- **`react-intersection-observer`**: Thin wrapper around the same API; not needed.
- **Scroll event + `getBoundingClientRect()`**: Main-thread polling; worse performance.

---

## Decision 6: Fonts

**Decision**: `next/font/google` — **Inter** (body) + **Sora** (headings).

**Rationale**:
- Both fonts are loaded via `next/font` — self-hosted, zero external network requests,
  zero CLS (preloaded with `font-display: optional`).
- **Inter**: Industry-standard, highly legible variable font; excellent at all weights.
- **Sora**: Geometric sans-serif with a modern, premium feel; pairs well with Inter.
- Two font families only — satisfies constitution Principle II and Technology Constraints table.

**Alternatives considered**:
- **Clash Display**: Not available on Google Fonts; requires manual self-hosting.
- **Google Fonts CDN**: Network request to external server; privacy concern; potential CLS.
- **System font stack**: No distinct typographic personality — not "premium" enough.

---

## Decision 7: Vercel Deployment

**Decision**: Vercel free tier with automatic deployments from the `main` branch.

**Rationale**:
- Zero-config Next.js deployment — detects framework automatically.
- SSG pages are served from Vercel's global edge CDN — satisfies SC-007 (FCP < 1.5s globally).
- Free SSL/TLS, automatic HTTPS, custom domain support.
- Satisfies SC-011: first deployment achievable within 30 minutes of project setup.
- No paid add-ons required (no serverless functions, no Postgres, no Blob storage).

**Alternatives considered**:
- **Netlify**: Also free; slightly less optimized for Next.js; no advantage here.
- **GitHub Pages**: Requires `next export`; limited redirect support; no edge CDN.
- **Self-hosted**: Operations overhead; not free; not appropriate for MVP.

---

## Resolved Unknowns Summary

| Unknown | Resolution |
|---|---|
| MDX rendering in App Router | `next-mdx-remote/rsc` — RSC-compatible |
| Syntax highlighting strategy | `rehype-pretty-code` + `shiki` — zero runtime |
| Dark mode SSR flash | `next-themes` — FOIT-safe |
| Progress bar library | None — custom 25-line hook |
| ToC active section | `IntersectionObserver` — zero deps |
| Font loading | `next/font/google` — Inter + Sora |
| Deployment | Vercel free tier — auto from main |

**All NEEDS CLARIFICATION resolved. Phase 1 design may proceed.**
