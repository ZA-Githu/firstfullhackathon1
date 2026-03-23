# Quickstart: AI-Native Book Website

**Date**: 2026-03-06
**Feature**: 1-book-website

This guide takes you from zero to a running local development server in under 5 minutes,
and from local to a live Vercel URL in under 30 minutes.

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Node.js | 20.x LTS or higher | https://nodejs.org |
| npm | 10.x (bundled with Node 20) | — |
| Git | any recent | https://git-scm.com |
| Vercel CLI (optional) | latest | `npm i -g vercel` |

---

## Local Development Setup

### 1. Bootstrap the Next.js 15 project

```bash
cd "C:/Users/Ismat Zehra/3D Objects/newhackathon1/ai-native-book"
npx create-next-app@latest . --typescript --tailwind --app --src-dir=false --import-alias="@/*"
```

Accept all defaults when prompted.

### 2. Install required dependencies

```bash
npm install next-themes next-mdx-remote gray-matter rehype-pretty-code shiki
```

### 3. Install shadcn/ui

```bash
npx shadcn@latest init
```

When prompted, choose:
- Style: **Default**
- Base colour: **Slate**
- CSS variables: **Yes**

Then add the required components:

```bash
npx shadcn@latest add button card input label textarea
```

### 4. Configure `next.config.ts`

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  pageExtensions: ['ts', 'tsx', 'mdx'],
  experimental: {
    mdxRs: true,
  },
}

export default nextConfig
```

### 5. Configure `tailwind.config.ts` design tokens

Add the glassmorphism + gradient tokens as described in `plan.md` → Phase 1.
(Full token list is in `plan.md` → Phase 1 → Component Architecture → Design Token System.)

### 6. Create `.env.example`

```bash
# No environment variables are required for the MVP.
# Add here if contact form integration is added in a future phase.
# NEXT_PUBLIC_SITE_URL=https://your-domain.vercel.app
```

Copy to `.env.local`:
```bash
cp .env.example .env.local
```

### 7. Run the development server

```bash
npm run dev
```

Open http://localhost:3000 — you should see the Next.js welcome page.

---

## Content Setup

### 8. Create the chapter content directory

```bash
mkdir -p content/chapters
```

### 9. Create the first MDX file to verify the pipeline

```bash
cat > content/chapters/chapter-01-topic-01.mdx << 'EOF'
---
chapterNumber: 1
topicNumber: 1
title: "What is AI-Native Development?"
description: "Defining the paradigm shift from AI-assisted to AI-native software engineering."
slug: "chapter-01-topic-01"
---

## What is AI-Native Development?

AI-Native development is a software engineering paradigm where AI is not bolted on as a tool
but is woven into the design, architecture, and delivery process from day one.
EOF
```

Verify the MDX pipeline is working once `lib/mdx.ts` is implemented.

---

## Deployment to Vercel

### Option A: Vercel Dashboard (recommended for first deploy)

1. Push your branch to GitHub:
   ```bash
   git add .
   git commit -m "feat: initial book website implementation"
   git push origin 1-book-website
   ```
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Vercel auto-detects Next.js — click **Deploy**
5. Your live URL appears within ~2 minutes

### Option B: Vercel CLI

```bash
vercel --prod
```

Follow the prompts to link to your Vercel account and project.

---

## Updating Content

To add or edit a chapter topic:

1. Edit or create the MDX file in `content/chapters/`
2. Ensure frontmatter includes all required fields (`chapterNumber`, `topicNumber`, `title`, `description`, `slug`)
3. Run `npm run build` locally to verify — the new topic appears in the Book page ToC automatically
4. Commit and push → Vercel auto-deploys

**No application code changes required when adding content.**

---

## Useful Commands

| Command | Purpose |
|---|---|
| `npm run dev` | Start local dev server at localhost:3000 |
| `npm run build` | Production build (run before pushing to catch errors) |
| `npm run lint` | ESLint check — must pass with zero warnings |
| `npx @next/bundle-analyzer` | Analyse bundle size (add `ANALYZE=true` env var) |

---

## Verifying the Constitution

Before each PR, run this mental checklist:

- [ ] `npm run build` → zero TypeScript errors, zero ESLint warnings
- [ ] Lighthouse Performance ≥ 90 (run via Chrome DevTools → Lighthouse)
- [ ] Lighthouse Accessibility ≥ 90
- [ ] Mobile at 320px: no horizontal overflow
- [ ] Dark mode: all pages render correctly
- [ ] Tab navigation: all interactive elements reachable; focus rings visible
- [ ] Book page: progress bar reaches 100% when scrolled to bottom
- [ ] Contact form: saves to localStorage; validation prevents bad submissions
