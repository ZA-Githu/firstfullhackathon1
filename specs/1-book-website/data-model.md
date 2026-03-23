# Data Model: AI-Native Book Website

**Phase**: 1 — Design & Contracts
**Date**: 2026-03-06
**Feature**: 1-book-website

---

## Entities

### Chapter

Represents one of the five book chapters. Derived from MDX frontmatter at build time.

```ts
interface Chapter {
  chapterNumber: number     // 1–5, unique, used for sort order
  title: string             // Display title, e.g. "The AI-Native Paradigm"
  description: string       // One-sentence summary shown on Home page chapter cards
  slug: string              // URL-safe identifier, e.g. "chapter-01"
  topics: Topic[]           // Always exactly 2 topics per chapter
}
```

**Validation rules**:
- `chapterNumber` MUST be an integer in range 1–5.
- `title` MUST be a non-empty string ≤ 80 characters.
- `description` MUST be a non-empty string ≤ 200 characters.
- `slug` MUST match `/^chapter-0[1-5]$/`.
- `topics` MUST have exactly 2 elements.

---

### Topic

Represents one of the two topics within a chapter. Each topic maps 1:1 to an MDX file.

```ts
interface Topic {
  chapterNumber: number     // 1–5 — parent chapter reference
  topicNumber: number       // 1–2 within the chapter
  title: string             // Display title
  description: string       // One-sentence description (used in ToC tooltip or subtitle)
  slug: string              // Unique identifier, e.g. "chapter-01-topic-01"
  content: string           // Raw MDX string (loaded server-side; not serialised to client)
  anchorId: string          // DOM anchor ID for smooth-scroll, e.g. "ch1-t1"
}
```

**Validation rules**:
- `topicNumber` MUST be 1 or 2.
- `slug` MUST match `/^chapter-0[1-5]-topic-0[12]$/`.
- `anchorId` MUST be unique across all 10 topics.
- `content` MUST be non-empty (if empty: render "Coming soon" placeholder).

---

### WaitlistEntry

Represents a visitor's waitlist submission, stored in localStorage.

```ts
interface WaitlistEntry {
  name: string              // Required; non-empty
  email: string             // Required; valid email format
  message?: string          // Optional; max 500 characters
  submittedAt: string       // ISO 8601 datetime string, e.g. "2026-03-06T14:30:00.000Z"
}
```

**Validation rules**:
- `name`: non-empty string.
- `email`: matches HTML5 email pattern; non-empty.
- `message`: optional; if present, ≤ 500 characters.
- `submittedAt`: generated at submission time via `new Date().toISOString()`.

**Storage contract**: See `contracts/localStorage.md`.

---

### UserPreference

Represents the visitor's persisted display preferences.

```ts
interface UserPreference {
  colorMode: 'dark' | 'light'   // Persisted dark/light choice
}
```

**Storage contract**: Managed entirely by `next-themes`; key is `theme` in localStorage.

---

## MDX File Naming Convention

```
/content/chapters/chapter-{CC}-topic-{TT}.mdx
```

Where `CC` = zero-padded chapter number (01–05), `TT` = zero-padded topic number (01–02).

**Examples**:
```
chapter-01-topic-01.mdx   → Chapter 1, Topic 1
chapter-03-topic-02.mdx   → Chapter 3, Topic 2
```

**Required frontmatter** (every MDX file MUST include all fields):

```yaml
---
chapterNumber: 1
topicNumber: 1
title: "What is AI-Native Development?"
description: "Defining the paradigm shift from AI-assisted to AI-native software engineering."
slug: "chapter-01-topic-01"
---
```

---

## State Transitions

### WaitlistForm

```
IDLE
  → (user fills fields, clicks Submit)
VALIDATING
  → (validation fails) → IDLE (with field errors displayed)
  → (validation passes) → SAVING
SAVING
  → (localStorage write succeeds) → SUCCESS
  → (localStorage throws SecurityError) → SUCCESS_WITH_WARNING
SUCCESS / SUCCESS_WITH_WARNING
  → (terminal states — form replaced by confirmation message)
```

### ThemeToggle

```
SYSTEM_DEFAULT (first load, no localStorage key)
  → (OS = dark) → DARK
  → (OS = light) → LIGHT
DARK ↔ LIGHT  (user toggles; persisted to localStorage key 'theme')
```

---

## `lib/mdx.ts` — Function Signatures

```ts
// Returns all 5 chapters with their topics, sorted by chapterNumber
export async function getAllChapters(): Promise<Chapter[]>

// Returns all 10 topics sorted by chapterNumber, then topicNumber
export async function getAllTopics(): Promise<Topic[]>

// Returns the MDX source string for a single topic (for server-side rendering)
export async function getTopicContent(slug: string): Promise<string | null>
```

---

## `lib/localStorage.ts` — Function Signatures

```ts
// Returns current waitlist array from localStorage (empty array if absent or error)
export function getWaitlist(): WaitlistEntry[]

// Appends entry to waitlist array in localStorage
// Returns { success: true } or { success: false, storageBlocked: true }
export function saveWaitlistEntry(entry: Omit<WaitlistEntry, 'submittedAt'>):
  { success: true } | { success: false; storageBlocked: boolean }
```
