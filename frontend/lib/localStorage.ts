import type { WaitlistEntry } from "@/types";

/** localStorage key for the waitlist array */
const WAITLIST_KEY = "waitlist";

/**
 * Returns the current waitlist entries from localStorage.
 * Returns an empty array if the key is absent, the JSON is corrupt, or
 * localStorage is unavailable. Never throws.
 */
export function getWaitlist(): WaitlistEntry[] {
  try {
    const raw = localStorage.getItem(WAITLIST_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    if (Array.isArray(parsed)) {
      return parsed as WaitlistEntry[];
    }
    return [];
  } catch {
    // Handles SecurityError, JSON parse errors, etc.
    return [];
  }
}

/**
 * Appends a new entry to the waitlist in localStorage.
 *
 * @returns `{ success: true }` on success,
 *          `{ success: false, storageBlocked: true }` if storage is blocked.
 *
 * Handles:
 *   (a) First-ever save — key absent → writes `[newEntry]`
 *   (b) Appending to existing array
 *   (c) SecurityError thrown by the browser (private/strict mode)
 */
export function saveWaitlistEntry(
  entry: Omit<WaitlistEntry, "submittedAt">
): { success: true } | { success: false; storageBlocked: boolean } {
  try {
    const existing = getWaitlist();
    const newEntry: WaitlistEntry = {
      ...entry,
      submittedAt: new Date().toISOString(),
    };
    const updated = [...existing, newEntry];
    localStorage.setItem(WAITLIST_KEY, JSON.stringify(updated));
    return { success: true };
  } catch (error) {
    // SecurityError is thrown when localStorage is blocked (e.g. private mode,
    // strict third-party cookie settings, or iframe sandbox restrictions).
    if (
      error instanceof Error &&
      (error.name === "SecurityError" || error.name === "QuotaExceededError")
    ) {
      return { success: false, storageBlocked: true };
    }
    return { success: false, storageBlocked: true };
  }
}
