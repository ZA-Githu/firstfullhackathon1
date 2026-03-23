# AI-Native Driven Development — Book Website

A premium, static book website built with **Next.js 15**, **Tailwind CSS**, **shadcn/ui**, and **MDX**.

## Features

- 5 chapters × 2 topics — all content in MDX files (no CMS needed)
- Reading progress bar on the Book page
- Sticky table of contents with active-section highlighting
- Glassmorphism design with gradient accents
- Dark / light mode with OS preference detection and localStorage persistence
- Waitlist form saved to localStorage (no backend required)
- Fully accessible — WCAG 2.1 AA, keyboard navigation, skip links
- Deployed on Vercel free tier

## Local Development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Build

```bash
npm run build   # production build — must pass with zero errors
npm run lint    # ESLint check — must pass with zero warnings
```

## Updating Content

All book content lives in `/content/chapters/`. Each file is an MDX file with frontmatter:

```mdx
---
chapterNumber: 1
topicNumber: 1
title: "Chapter Title"
description: "One-sentence description."
slug: "chapter-01-topic-01"
---

## Your Content Here
```

**To add or edit a chapter:**
1. Edit or create the MDX file in `content/chapters/`
2. Ensure all frontmatter fields are present
3. Run `npm run build` to verify
4. Commit and push — Vercel auto-deploys

No application code changes required when adding content.

## Deploy to Vercel

1. Push to GitHub
2. Import repository at [vercel.com/new](https://vercel.com/new)
3. Vercel auto-detects Next.js — click **Deploy**
4. Live URL appears within ~2 minutes

## Environment Variables

No environment variables are required for the MVP. See `.env.example` for documentation.

## Project Structure

```
app/                    Next.js 15 App Router pages
components/             Reusable React components
  layout/               Navbar, Footer, SkipLink, ThemeToggle
  home/                 Hero, ChapterCard
  book/                 ProgressBar, TableOfContents, MDXContent, ChapterSection
  about/                AuthorCard
  contact/              WaitlistForm
content/chapters/       MDX book content (10 files)
lib/                    mdx.ts, localStorage.ts, utils.ts
hooks/                  useReadingProgress.ts, useActiveSection.ts
types/                  index.ts — shared TypeScript interfaces
specs/                  Spec-driven development artifacts
```
