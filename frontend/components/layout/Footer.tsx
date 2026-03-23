/**
 * Footer — minimal site footer with site name, year, and credits.
 */
export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="w-full border-t border-border/40 bg-background/50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-muted-foreground">
          <p className="font-heading font-semibold gradient-text">
            AI-Native Driven Development
          </p>
          <p>
            &copy; {year} &mdash; Built with{" "}
            <span className="text-foreground">Next.js</span>
          </p>
        </div>
      </div>
    </footer>
  );
}
