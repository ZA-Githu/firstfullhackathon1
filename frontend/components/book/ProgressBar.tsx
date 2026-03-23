"use client";

import { useReadingProgress } from "@/hooks/useReadingProgress";

/**
 * ProgressBar — fixed reading progress indicator at the top of the page.
 *
 * Uses useReadingProgress() to track scroll percentage.
 * ARIA: role="progressbar" with valuenow/valuemin/valuemax attributes.
 * Visual: gradient fill that grows from left to right as the user scrolls.
 */
export function ProgressBar() {
  const progress = useReadingProgress();

  return (
    <div
      role="progressbar"
      aria-valuenow={progress}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label="Reading progress"
      className="fixed top-0 left-0 z-50 h-1 w-full bg-transparent"
    >
      <div
        className="h-full bg-gradient-to-r from-primary-500 to-accent-500 transition-[width] duration-100"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}
