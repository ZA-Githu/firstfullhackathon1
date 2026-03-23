import type { Metadata } from "next";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export const metadata: Metadata = {
  title: "Page Not Found",
  description: "The page you are looking for does not exist.",
};

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4">
      <div className="max-w-md w-full text-center space-y-6 rounded-2xl border border-white/20 bg-white/5 backdrop-blur-sm p-10">
        <p className="text-7xl font-heading font-bold gradient-text">404</p>
        <h1 className="text-2xl font-heading font-semibold">Page not found</h1>
        <p className="text-muted-foreground">
          The page you are looking for does not exist or has been moved.
        </p>
        <Button asChild className="bg-gradient-button text-white hover:opacity-90">
          <Link href="/">← Back to Home</Link>
        </Button>
      </div>
    </div>
  );
}
