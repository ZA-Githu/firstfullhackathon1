"use client";

import { useState } from "react";
import { useActiveSection } from "@/hooks/useActiveSection";
import { cn } from "@/lib/utils";
import type { Chapter } from "@/types";
import { BookOpen, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface TableOfContentsProps {
  chapters: Chapter[];
}

/**
 * TableOfContents — sticky sidebar (desktop) + overlay (mobile).
 *
 * Desktop (≥ md): sticky left sidebar showing all chapters and topics.
 * Mobile (< md): fixed bottom-right "Contents" button → full-screen overlay dialog.
 *
 * Uses useActiveSection() to highlight the currently-reading section.
 */
export function TableOfContents({ chapters }: TableOfContentsProps) {
  const [mobileOpen, setMobileOpen] = useState(false);

  // Build flat list of all topic anchor IDs for IntersectionObserver
  const allTopicIds = chapters.flatMap((ch) =>
    ch.topics.map((t) => t.anchorId)
  );

  // Also add chapter-level anchor IDs (ch1, ch2, etc.)
  const chapterIds = chapters.map((ch) => `ch${ch.chapterNumber}`);
  const allIds = [...chapterIds, ...allTopicIds];

  const activeId = useActiveSection(allIds);

  function isTopicActive(anchorId: string): boolean {
    return activeId === anchorId;
  }

  function isChapterActive(chapterNumber: number): boolean {
    const chId = `ch${chapterNumber}`;
    if (activeId === chId) return true;
    return chapters
      .find((c) => c.chapterNumber === chapterNumber)
      ?.topics.some((t) => t.anchorId === activeId) ?? false;
  }

  const tocContent = (
    <nav aria-label="Table of contents">
      <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-3">
        Contents
      </p>
      <ol className="space-y-1">
        {chapters.map((chapter) => (
          <li key={chapter.chapterNumber}>
            {/* Chapter-level link */}
            <a
              href={`#ch${chapter.chapterNumber}-t1`}
              onClick={() => setMobileOpen(false)}
              className={cn(
                "block rounded px-2 py-1 text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500",
                isChapterActive(chapter.chapterNumber)
                  ? "font-semibold text-primary-500"
                  : "text-foreground/70 hover:text-foreground hover:bg-accent/10"
              )}
            >
              <span className="text-xs text-muted-foreground mr-1">
                Ch {chapter.chapterNumber}.
              </span>
              {chapter.title}
            </a>

            {/* Topic-level links */}
            <ol className="ml-3 mt-1 space-y-1">
              {chapter.topics.map((topic) => (
                <li key={topic.anchorId}>
                  <a
                    href={`#${topic.anchorId}`}
                    onClick={() => setMobileOpen(false)}
                    className={cn(
                      "block rounded px-2 py-1 text-xs transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500",
                      isTopicActive(topic.anchorId)
                        ? "font-semibold text-primary-500"
                        : "text-muted-foreground hover:text-foreground hover:bg-accent/10"
                    )}
                  >
                    {topic.topicNumber}. {topic.title}
                  </a>
                </li>
              ))}
            </ol>
          </li>
        ))}
      </ol>
    </nav>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:block sticky top-20 max-h-[calc(100vh-5rem)] overflow-y-auto pr-4">
        {tocContent}
      </aside>

      {/* Mobile: floating "Contents" button */}
      <div className="md:hidden fixed bottom-6 right-6 z-40">
        <Button
          variant="gradient"
          size="sm"
          aria-label="Open table of contents"
          onClick={() => setMobileOpen(true)}
          className="shadow-lg shadow-primary-500/30 gap-1.5"
        >
          <BookOpen className="h-4 w-4" aria-hidden="true" />
          Contents
        </Button>
      </div>

      {/* Mobile overlay dialog */}
      {mobileOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Table of contents"
          className="md:hidden fixed inset-0 z-50 flex flex-col bg-background/95 backdrop-blur-md"
        >
          <div className="flex items-center justify-between p-4 border-b border-border">
            <h2 className="font-heading font-semibold">Contents</h2>
            <Button
              variant="ghost"
              size="icon"
              aria-label="Close table of contents"
              onClick={() => setMobileOpen(false)}
            >
              <X className="h-5 w-5" aria-hidden="true" />
            </Button>
          </div>
          <div className="flex-1 overflow-y-auto p-4">{tocContent}</div>
        </div>
      )}
    </>
  );
}
