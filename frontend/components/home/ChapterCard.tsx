import Link from "next/link";

interface ChapterCardProps {
  chapterNumber: number;
  title: string;
  description: string;
  slug: string;
}

/**
 * ChapterCard — glassmorphism card displaying a chapter preview.
 * Links to the first topic of the chapter on the Book page.
 */
export function ChapterCard({
  chapterNumber,
  title,
  description,
}: ChapterCardProps) {
  // Link to the chapter's first topic anchor on the Book page
  const href = `/book#ch${chapterNumber}-t1`;

  return (
    <Link
      href={href}
      className="group block rounded-2xl backdrop-blur-sm bg-white/10 dark:bg-white/5 border border-white/20 dark:border-white/10 p-6 transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-primary-500/20 hover:bg-white/15 dark:hover:bg-white/8 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2"
      aria-label={`Read Chapter ${chapterNumber}: ${title}`}
    >
      {/* Chapter number badge */}
      <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-button text-white text-sm font-bold shadow-lg shadow-primary-500/30">
        {chapterNumber}
      </div>

      {/* Chapter title */}
      <h3 className="font-heading text-lg font-semibold text-foreground group-hover:text-primary-500 transition-colors line-clamp-2">
        {title}
      </h3>

      {/* Description */}
      <p className="mt-2 text-sm text-muted-foreground line-clamp-3">
        {description}
      </p>

      {/* Read more indicator */}
      <div className="mt-4 flex items-center gap-1 text-sm font-medium text-primary-500 group-hover:gap-2 transition-all">
        Read chapter{" "}
        <span aria-hidden="true" className="transition-transform group-hover:translate-x-1">
          →
        </span>
      </div>
    </Link>
  );
}
