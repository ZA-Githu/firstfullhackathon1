import Image from "next/image";

/**
 * AuthorCard — glassmorphism card showing author bio, profile image,
 * and mission statement.
 *
 * Uses next/image for optimised image loading with correct alt text.
 * Responsive: stacks vertically on mobile, side-by-side on md+.
 */
export function AuthorCard() {
  return (
    <div className="rounded-2xl backdrop-blur-sm bg-white/5 dark:bg-white/3 border border-white/10 p-8">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Author photo */}
        <div className="flex-shrink-0 flex justify-center md:justify-start">
          <div className="relative">
            <div className="absolute inset-0 rounded-full bg-gradient-hero opacity-30 blur-xl" />
            <Image
              src="/author.jpg"
              alt="Author of AI-Native Driven Development"
              width={160}
              height={160}
              priority
              className="relative rounded-full object-cover border-4 border-white/10 shadow-xl"
            />
          </div>
        </div>

        {/* Author info */}
        <div className="flex-1 min-w-0">
          <h2 className="font-heading text-2xl font-bold text-foreground">
            The Author
          </h2>
          <p className="mt-1 text-sm font-medium text-primary-500">
            Software Engineer &amp; AI Practitioner
          </p>

          <div className="mt-5 space-y-4 text-muted-foreground leading-7">
            <p>
              With over a decade of experience building production software
              systems, I&apos;ve watched AI transform from a niche research
              topic into the defining force of our industry. This book is the
              guide I wish I had when AI-native development was just beginning
              to take shape.
            </p>
            <p>
              My work focuses on the intersection of software architecture and
              AI systems — helping engineering teams move beyond sprinkling AI
              on top of existing systems, and instead design products where AI
              capabilities are woven into the fabric of every decision.
            </p>
            <p>
              I believe the most important skill for the next generation of
              engineers is not prompt engineering or model fine-tuning — it is
              the ability to think architecturally about AI systems, to design
              for non-determinism, and to build teams that can ship AI-native
              products responsibly.
            </p>
          </div>

          {/* Mission quote */}
          <blockquote className="mt-6 border-l-4 border-primary-500 pl-5 italic text-foreground/70">
            &ldquo;The shift from AI-assisted to AI-native is not about the
            tools — it&apos;s about the mindset. When AI becomes a first-class
            citizen in your architecture, everything else follows.&rdquo;
          </blockquote>
        </div>
      </div>
    </div>
  );
}
