import type { Metadata } from "next";
import { Hero } from "@/components/home/Hero";
import { ChapterCard } from "@/components/home/ChapterCard";
import { getAllChapters } from "@/lib/mdx";

export const metadata: Metadata = {
  title: "AI-Native Driven Development",
  description:
    "A comprehensive guide to building software systems where AI is a first-class citizen — not an afterthought.",
  openGraph: {
    title: "AI-Native Driven Development",
    description:
      "A comprehensive guide to building software systems where AI is a first-class citizen — not an afterthought.",
    type: "website",
  },
};

/**
 * Home page — Server Component.
 * Renders the gradient Hero section + 5 glassmorphism chapter preview cards.
 */
export default async function HomePage() {
  const chapters = await getAllChapters();

  return (
    <>
      {/* Hero section */}
      <Hero />

      {/* Chapter preview cards */}
      <section
        aria-label="Book chapters"
        className="container mx-auto px-4 py-16"
      >
        <div className="text-center mb-12">
          <h2 className="font-heading text-3xl font-bold gradient-text sm:text-4xl">
            What You&apos;ll Learn
          </h2>
          <p className="mt-3 text-muted-foreground max-w-xl mx-auto">
            Five chapters packed with practical knowledge, real-world examples,
            and actionable techniques.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {chapters.map((chapter, index) => (
            <div
              key={chapter.chapterNumber}
              className="animate-fade-in-up"
              style={{ animationDelay: `${index * 80}ms`, animationFillMode: "both" }}
            >
              <ChapterCard
                chapterNumber={chapter.chapterNumber}
                title={chapter.title}
                description={chapter.description}
                slug={chapter.slug}
              />
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <p className="text-muted-foreground text-sm">
            All content is free to read online.{" "}
            <a
              href="/book"
              className="text-primary-500 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded"
            >
              Start reading now →
            </a>
          </p>
        </div>
      </section>
    </>
  );
}
