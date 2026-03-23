"use client";

import { useTheme } from "next-themes";
import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

/**
 * ThemeToggle — client component that toggles between light and dark mode.
 * Uses next-themes useTheme() hook. Renders Sun (light) or Moon (dark) icon.
 * Fully keyboard operable with a visible aria-label.
 */
export function ThemeToggle() {
  // Avoid hydration mismatch: only render icon after mounting
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  function toggle() {
    setTheme(theme === "dark" ? "light" : "dark");
  }

  if (!mounted) {
    // Render a placeholder button to avoid layout shift
    return (
      <Button
        variant="ghost"
        size="icon"
        aria-label="Toggle dark mode"
        className="h-9 w-9"
      >
        <span className="h-4 w-4" />
      </Button>
    );
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
      onClick={toggle}
      className="h-9 w-9"
    >
      {theme === "dark" ? (
        <Sun className="h-4 w-4" aria-hidden="true" />
      ) : (
        <Moon className="h-4 w-4" aria-hidden="true" />
      )}
    </Button>
  );
}
