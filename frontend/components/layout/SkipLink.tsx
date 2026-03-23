/**
 * SkipLink — visually hidden "Skip to main content" link.
 * Becomes visible on :focus-visible for keyboard users.
 * Must be the FIRST focusable element in the DOM.
 */
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus-visible:not-sr-only focus-visible:absolute focus-visible:top-4 focus-visible:left-4 focus-visible:z-[100] focus-visible:rounded-md focus-visible:bg-primary-500 focus-visible:px-4 focus-visible:py-2 focus-visible:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"
    >
      Skip to main content
    </a>
  );
}
