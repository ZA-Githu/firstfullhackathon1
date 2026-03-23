import type { Metadata } from "next";
import { WaitlistForm } from "@/components/contact/WaitlistForm";

export const metadata: Metadata = {
  title: "Join the Waitlist",
  description:
    "Be the first to know when AI-Native Driven Development launches. Join the waitlist for updates, early access, and exclusive content.",
  openGraph: {
    title: "Join the Waitlist — AI-Native Driven Development",
    description:
      "Get early access and exclusive content. Join hundreds of engineers on the waitlist.",
  },
};

export default function ContactPage() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-lg">
      <div className="text-center mb-10 space-y-3">
        <h1 className="text-4xl font-heading font-bold gradient-text">
          Join the Waitlist
        </h1>
        <p className="text-muted-foreground text-lg">
          Be the first to know when the book launches. No spam — just updates
          that matter.
        </p>
      </div>

      <div className="rounded-2xl border border-white/20 bg-white/5 backdrop-blur-sm p-8">
        <WaitlistForm />
      </div>
    </div>
  );
}
