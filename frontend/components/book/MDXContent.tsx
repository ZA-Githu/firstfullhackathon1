import { MDXRemote } from "next-mdx-remote/rsc";
import rehypePrettyCode from "rehype-pretty-code";
import type { Options as PrettyCodeOptions } from "rehype-pretty-code";
import type { MDXRemoteProps } from "next-mdx-remote/rsc";
import { cn } from "@/lib/utils";

/* -----------------------------------------------------------------------
   Custom Callout component — rendered inline in MDX as <Callout type="...">
   ----------------------------------------------------------------------- */

interface CalloutProps {
  type?: "info" | "warning" | "tip";
  children: React.ReactNode;
}

const calloutStyles: Record<string, string> = {
  info: "border-blue-500/50 bg-blue-500/5 text-blue-700 dark:text-blue-300",
  warning: "border-amber-500/50 bg-amber-500/5 text-amber-700 dark:text-amber-300",
  tip: "border-green-500/50 bg-green-500/5 text-green-700 dark:text-green-300",
};

const calloutIcons: Record<string, string> = {
  info: "ℹ️",
  warning: "⚠️",
  tip: "💡",
};

function Callout({ type = "info", children }: CalloutProps) {
  return (
    <div
      role="note"
      className={cn(
        "my-6 flex gap-3 rounded-xl border p-4",
        calloutStyles[type] ?? calloutStyles.info
      )}
    >
      <span aria-hidden="true" className="text-lg shrink-0 mt-0.5">
        {calloutIcons[type] ?? calloutIcons.info}
      </span>
      <div className="text-sm leading-relaxed [&>p]:m-0">{children}</div>
    </div>
  );
}

/* -----------------------------------------------------------------------
   Custom MDX component map
   ----------------------------------------------------------------------- */

const components: MDXRemoteProps["components"] = {
  h1: (props) => (
    <h1
      className="font-heading text-3xl font-bold mt-12 mb-4 gradient-text"
      {...props}
    />
  ),
  h2: (props) => (
    <h2
      className="font-heading text-2xl font-semibold mt-8 mb-3 text-foreground"
      {...props}
    />
  ),
  h3: (props) => (
    <h3
      className="font-heading text-xl font-semibold mt-6 mb-2 text-foreground"
      {...props}
    />
  ),
  p: (props) => (
    <p className="mb-5 leading-7 text-foreground/85" {...props} />
  ),
  ul: (props) => (
    <ul className="mb-5 ml-5 list-disc space-y-1.5 text-foreground/85" {...props} />
  ),
  ol: (props) => (
    <ol className="mb-5 ml-5 list-decimal space-y-1.5 text-foreground/85" {...props} />
  ),
  li: (props) => <li className="leading-7" {...props} />,
  blockquote: (props) => (
    <blockquote
      className="my-6 border-l-4 border-primary-500 pl-5 italic text-muted-foreground"
      {...props}
    />
  ),
  // Inline code (not inside a pre block)
  code: (props) => (
    <code
      className="rounded bg-primary-500/10 px-1.5 py-0.5 text-sm font-mono text-primary-600 dark:text-primary-400"
      {...props}
    />
  ),
  // Code blocks (wraps code elements output by rehype-pretty-code)
  pre: (props) => (
    <pre
      className="my-6 overflow-x-auto rounded-xl border border-border bg-card p-4 text-sm"
      {...props}
    />
  ),
  // Custom components available in MDX files
  Callout,
};

/* -----------------------------------------------------------------------
   rehype-pretty-code options
   ----------------------------------------------------------------------- */

const prettyCodeOptions: PrettyCodeOptions = {
  // CSS variable themes — works with both light and dark modes
  theme: {
    dark: "github-dark",
    light: "github-light",
  },
  keepBackground: false,
};

/* -----------------------------------------------------------------------
   MDXContent — Server Component
   ----------------------------------------------------------------------- */

interface MDXContentProps {
  /** Raw MDX source string */
  source: string;
}

/**
 * MDXContent — renders raw MDX content using next-mdx-remote/rsc.
 *
 * - Server Component: zero client JS for content rendering
 * - rehype-pretty-code: build-time syntax highlighting (no runtime)
 * - Custom component map for styled headings, code blocks, callouts
 */
export async function MDXContent({ source }: MDXContentProps) {
  return (
    <div className="prose-book">
      <MDXRemote
        source={source}
        components={components}
        options={{
          mdxOptions: {
            rehypePlugins: [[rehypePrettyCode, prettyCodeOptions]],
          },
        }}
      />
    </div>
  );
}
