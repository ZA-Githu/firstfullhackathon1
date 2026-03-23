import { MDXContent } from "./MDXContent";
import type { Chapter } from "@/types";

interface ChapterSectionProps {
  chapter: Chapter;
}

/**
 * ChapterSection — Server Component that renders one full chapter.
 *
 * Each chapter heading and each topic heading gets a unique anchor ID
 * so that the Table of Contents can smooth-scroll to them.
 *
 * Renders "Coming soon" placeholder when a topic's content is empty.
 */
export function ChapterSection({ chapter }: ChapterSectionProps) {
  return (
    <section
      id={`ch${chapter.chapterNumber}`}
      aria-labelledby={`ch${chapter.chapterNumber}-heading`}
      className="mb-20"
    >
      {/* Chapter heading */}
      <div className="mb-10 pb-6 border-b border-border">
        <div className="inline-flex items-center gap-2 mb-3">
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-button text-white text-xs font-bold shadow-md shadow-primary-500/30">
            {chapter.chapterNumber}
          </span>
          <span className="text-sm font-medium text-muted-foreground uppercase tracking-widest">
            Chapter {chapter.chapterNumber}
          </span>
        </div>
        <h2
          id={`ch${chapter.chapterNumber}-heading`}
          className="font-heading text-3xl font-bold text-foreground sm:text-4xl"
        >
          {chapter.title}
        </h2>
        <p className="mt-2 text-muted-foreground">{chapter.description}</p>
      </div>

      {/* Topics */}
      <div className="space-y-16">
        {chapter.topics.map((topic) => (
          <article
            key={topic.anchorId}
            id={topic.anchorId}
            aria-labelledby={`${topic.anchorId}-heading`}
            className="scroll-mt-24"
          >
            {/* Topic heading */}
            <h3
              id={`${topic.anchorId}-heading`}
              className="font-heading text-2xl font-semibold text-foreground mb-6 flex items-center gap-3"
            >
              <span className="text-sm font-normal text-muted-foreground shrink-0">
                {chapter.chapterNumber}.{topic.topicNumber}
              </span>
              {topic.title}
            </h3>

            {/* MDX content or placeholder */}
            {topic.content ? (
              <MDXContent source={topic.content} />
            ) : (
              <div className="rounded-xl border border-dashed border-border p-8 text-center text-muted-foreground">
                <p className="text-lg font-medium">Coming soon</p>
                <p className="mt-1 text-sm">
                  This topic is being written. Check back soon!
                </p>
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
