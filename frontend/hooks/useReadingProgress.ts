"use client";

import { useState, useEffect } from "react";

/**
 * useReadingProgress — tracks vertical scroll position as a 0–100 percentage.
 *
 * Attaches a scroll event listener on window.
 * Throttles updates via requestAnimationFrame for performance.
 * Cleans up listener on unmount.
 *
 * @returns number — reading progress percentage (0 = top, 100 = bottom)
 */
export function useReadingProgress(): number {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let rafId: number | null = null;

    function handleScroll() {
      if (rafId !== null) return; // throttle: skip if frame already queued

      rafId = requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        const scrollHeight = document.documentElement.scrollHeight;
        const innerHeight = window.innerHeight;
        const maxScroll = scrollHeight - innerHeight;

        if (maxScroll <= 0) {
          setProgress(100);
        } else {
          const pct = Math.min(100, Math.round((scrollY / maxScroll) * 100));
          setProgress(pct);
        }

        rafId = null;
      });
    }

    window.addEventListener("scroll", handleScroll, { passive: true });

    // Compute initial value in case page loads mid-scroll
    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (rafId !== null) cancelAnimationFrame(rafId);
    };
  }, []);

  return progress;
}
