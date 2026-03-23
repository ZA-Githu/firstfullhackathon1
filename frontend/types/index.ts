/**
 * Shared TypeScript types for the AI-Native Book Website.
 * All types match the data model defined in specs/1-book-website/data-model.md
 */

/** One of the five book chapters, derived from MDX frontmatter at build time. */
export interface Chapter {
  /** 1–5, unique, used for sort order */
  chapterNumber: number;
  /** Display title, e.g. "The AI-Native Paradigm" */
  title: string;
  /** One-sentence summary shown on Home page chapter cards */
  description: string;
  /** URL-safe identifier, e.g. "chapter-01" */
  slug: string;
  /** Always exactly 2 topics per chapter */
  topics: Topic[];
}

/** One of the two topics within a chapter. Each topic maps 1:1 to an MDX file. */
export interface Topic {
  /** 1–5 — parent chapter reference */
  chapterNumber: number;
  /** 1–2 within the chapter */
  topicNumber: number;
  /** Display title */
  title: string;
  /** One-sentence description (used in ToC tooltip or subtitle) */
  description: string;
  /** Unique identifier, e.g. "chapter-01-topic-01" */
  slug: string;
  /** Raw MDX string (loaded server-side; not serialised to client) */
  content: string;
  /** DOM anchor ID for smooth-scroll, e.g. "ch1-t1" */
  anchorId: string;
}

/** A visitor's waitlist submission, stored in localStorage. */
export interface WaitlistEntry {
  /** Required; non-empty */
  name: string;
  /** Required; valid email format */
  email: string;
  /** Optional; max 500 characters */
  message?: string;
  /** ISO 8601 datetime string, e.g. "2026-03-06T14:30:00.000Z" */
  submittedAt: string;
}

/** Visitor's persisted display preferences. Managed by next-themes. */
export interface UserPreference {
  colorMode: "dark" | "light";
}
