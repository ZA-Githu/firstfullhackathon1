import type { Metadata } from "next";
import { getAllChapters } from "@/lib/mdx";
import { ProgressBar } from "@/components/book/ProgressBar";
import { TableOfContents } from "@/components/book/TableOfContents";
import { ChapterSection } from "@/components/book/ChapterSection";

export const metadata: Metadata = {
  title: "Read the Book",
  description:
    "Read AI-Native Driven Development online — all 5 chapters and 10 topics, free.",
  openGraph: {
    title: "Read AI-Native Driven Development",
    description:
      "All 5 chapters and 10 topics free to read online. From paradigm to practice.",
    type: "article",
  },
};

/**
 * Book page — Server Component.
 *
 * Layout:
 *  - Fixed reading progress bar (client component — ProgressBar)
 *  - Two-column grid on desktop: [ToC sidebar | content]
 *  - Single column on mobile with floating "Contents" button
 *
 * Data flow: getAllChapters() → 5 Chapter objects (each with 2 topics + content)
 */
export default async function BookPage() {
  const chapters = await getAllChapters();

  return (
    <>
      {/* Reading progress bar — fixed at top of viewport */}
      <ProgressBar />

      {/* Page header */}
      <div className="border-b border-border bg-gradient-card">
        <div className="container mx-auto px-4 py-10">
          <p className="text-sm font-medium text-muted-foreground uppercase tracking-widest mb-2">
            Online Edition
          </p>
          <h1 className="font-heading text-4xl font-bold gradient-text sm:text-5xl">
            AI-Native Driven Development
          </h1>
          <p className="mt-3 text-muted-foreground max-w-2xl">
            A practical guide to building software systems where AI is woven
            into every layer — from architecture to deployment.
          </p>
        </div>
      </div>

      {/* Two-column layout: ToC sidebar + content */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-[260px_1fr] gap-12">
          {/* ToC sidebar (client component — handles active section + mobile overlay) */}
          <TableOfContents chapters={chapters} />

          {/* Book content */}
          <div className="min-w-0">
            {chapters.map((chapter) => (
              <ChapterSection key={chapter.chapterNumber} chapter={chapter} />
            ))}

            {/* End of book */}
            <div className="mt-16 rounded-2xl border border-border bg-gradient-card p-8 text-center">
              <p className="font-heading text-xl font-semibold gradient-text">
                You&apos;ve reached the end!
              </p>
              <p className="mt-2 text-sm text-muted-foreground">
                Thank you for reading. Share your thoughts and join our waitlist
                for the print edition.
              </p>
              <a
                href="/contact"
                className="mt-4 inline-block text-sm text-primary-500 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded"
              >
                Join the waitlist →
              </a>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
