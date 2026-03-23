import Link from "next/link";
import { Button } from "@/components/ui/button";

/**
 * Hero — full-viewport gradient hero section for the Home page.
 * Includes floating decorative blobs (CSS-only, no JS).
 * Responsive: 320px / 768px / 1440px.
 */
export function Hero() {
  return (
    <section
      className="relative min-h-[calc(100vh-3.5rem)] flex items-center justify-center overflow-hidden bg-gradient-hero"
      aria-label="Book hero"
    >
      {/* Decorative floating blobs — purely decorative, hidden from screen readers */}
      <div aria-hidden="true" className="absolute inset-0 overflow-hidden">
        <div className="animate-float absolute -top-16 -left-16 h-72 w-72 rounded-full bg-white/10 blur-3xl" />
        <div className="animate-float-delayed absolute top-1/3 -right-20 h-96 w-96 rounded-full bg-white/10 blur-3xl" />
        <div className="animate-float-slow absolute -bottom-24 left-1/3 h-80 w-80 rounded-full bg-white/10 blur-3xl" />
      </div>

      {/* Hero content */}
      <div className="relative z-10 container mx-auto px-4 py-20 text-center">
        {/* Badge */}
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-4 py-1.5 text-sm text-white/90 backdrop-blur-sm">
          <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse" />
          Now available to read online
        </div>

        {/* Book title */}
        <h1 className="font-heading text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl lg:text-7xl">
          AI-Native{" "}
          <span className="block text-transparent [-webkit-text-stroke:2px_rgba(255,255,255,0.4)]">
            Driven
          </span>{" "}
          Development
        </h1>

        {/* Subtitle */}
        <p className="mx-auto mt-6 max-w-2xl text-lg text-white/80 sm:text-xl">
          A comprehensive guide to building software systems where AI is a
          first-class citizen — not an afterthought. Master the paradigm shift
          that defines the next era of engineering.
        </p>

        {/* CTAs */}
        <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Button
            asChild
            size="lg"
            className="bg-white text-primary-600 hover:bg-white/90 font-semibold shadow-xl shadow-black/20 px-8"
          >
            <Link href="/book">Start Reading →</Link>
          </Button>
          <Button
            asChild
            variant="outline"
            size="lg"
            className="border-white/30 text-white hover:bg-white/10 bg-transparent px-8"
          >
            <Link href="/contact">Join the Waitlist</Link>
          </Button>
        </div>

        {/* Stats */}
        <div className="mt-16 grid grid-cols-3 gap-6 max-w-md mx-auto">
          {[
            { value: "5", label: "Chapters" },
            { value: "10", label: "Topics" },
            { value: "Free", label: "To Read" },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-2xl font-heading font-bold text-white sm:text-3xl">
                {stat.value}
              </div>
              <div className="text-sm text-white/70">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div
        aria-hidden="true"
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1 text-white/50"
      >
        <span className="text-xs tracking-widest uppercase">Scroll</span>
        <div className="h-8 w-px bg-white/30" />
      </div>
    </section>
  );
}
