"use client";

import { useState, useEffect } from "react";

/**
 * useActiveSection — tracks which section heading is currently in the viewport.
 *
 * Uses IntersectionObserver with a narrow rootMargin to detect the section
 * the user is currently reading (the one closest to the top of the viewport).
 *
 * @param sectionIds - Array of DOM element IDs to observe.
 * @returns The ID of the currently active section, or empty string if none.
 */
export function useActiveSection(sectionIds: string[]): string {
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    if (sectionIds.length === 0) return;

    // Map from id → whether it's currently intersecting
    const intersectingMap = new Map<string, boolean>();

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          intersectingMap.set(entry.target.id, entry.isIntersecting);
        });

        // Pick the first intersecting section (topmost in DOM order)
        const active = sectionIds.find((id) => intersectingMap.get(id));
        if (active) {
          setActiveId(active);
        }
      },
      {
        // Top 20% is a "buffer" zone; bottom 70% is ignored.
        // This keeps the active entry stable as the user scrolls.
        rootMargin: "-20% 0px -70% 0px",
      }
    );

    // Observe each section element; skip IDs that don't exist in the DOM
    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => {
      observer.disconnect();
    };
  }, [sectionIds]);

  return activeId;
}
