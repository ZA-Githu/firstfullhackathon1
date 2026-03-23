"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";
import { cn } from "@/lib/utils";
import {
  SignInButton,
  SignUpButton,
  UserButton,
  useUser,
} from "@clerk/nextjs";

/** Navigation links for the site */
const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/book", label: "Book" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

/**
 * Navbar — responsive site navigation.
 * Desktop: horizontal links + theme toggle.
 * Mobile: hamburger button → slide-down menu.
 * Uses usePathname() for active link highlighting.
 */
export function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const { isSignedIn } = useUser();

  function isActive(href: string): boolean {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  }

  function closeMobile() {
    setMobileOpen(false);
  }

  return (
    <header className="sticky top-0 z-40 w-full backdrop-blur-sm bg-white/80 dark:bg-slate-900/80 border-b border-border/40">
      <nav aria-label="Main navigation" className="container mx-auto px-4">
        <div className="flex h-14 items-center justify-between">
          {/* Logo / Site name */}
          <Link
            href="/"
            className="font-heading font-bold text-lg gradient-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded"
          >
            AI-Native Book
          </Link>

          {/* Desktop links */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "px-3 py-1.5 rounded-md text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500",
                  isActive(link.href)
                    ? "font-semibold text-primary-500"
                    : "text-foreground/70 hover:text-foreground hover:bg-accent/10"
                )}
              >
                {link.label}
              </Link>
            ))}
            <div className="ml-2 flex items-center gap-2">
              <ThemeToggle />
              {!isSignedIn ? (
                <>
                  <SignInButton mode="modal">
                    <button className="text-sm font-medium hover:text-primary-500 transition-colors">
                      Sign In
                    </button>
                  </SignInButton>
                  <SignUpButton mode="modal">
                    <button className="bg-[#6c47ff] text-white rounded-full font-medium text-sm h-9 px-4 cursor-pointer hover:bg-[#5a3ad6] transition-colors">
                      Sign Up
                    </button>
                  </SignUpButton>
                </>
              ) : (
                <UserButton />
              )}
            </div>
          </div>

          {/* Mobile: theme toggle + hamburger */}
          <div className="flex items-center gap-1 md:hidden">
            <ThemeToggle />
            <button
              type="button"
              aria-expanded={mobileOpen}
              aria-controls="mobile-menu"
              aria-label={mobileOpen ? "Close navigation menu" : "Open navigation menu"}
              onClick={() => setMobileOpen((prev) => !prev)}
              className="h-9 w-9 inline-flex items-center justify-center rounded-md hover:bg-accent/10 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
            >
              {mobileOpen ? (
                <X className="h-5 w-5" aria-hidden="true" />
              ) : (
                <Menu className="h-5 w-5" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div
            id="mobile-menu"
            className="md:hidden py-3 border-t border-border/40"
          >
            <div className="flex flex-col gap-1">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={closeMobile}
                  className={cn(
                    "px-3 py-2 rounded-md text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500",
                    isActive(link.href)
                      ? "font-semibold text-primary-500 bg-primary-500/10"
                      : "text-foreground/70 hover:text-foreground hover:bg-accent/10"
                  )}
                >
                  {link.label}
                </Link>
              ))}
              <div className="flex items-center gap-2 px-3 py-2">
                {!isSignedIn ? (
                  <>
                    <SignInButton mode="modal">
                      <button className="text-sm font-medium hover:text-primary-500 transition-colors">
                        Sign In
                      </button>
                    </SignInButton>
                    <SignUpButton mode="modal">
                      <button className="bg-[#6c47ff] text-white rounded-full font-medium text-sm h-9 px-4 cursor-pointer hover:bg-[#5a3ad6] transition-colors">
                        Sign Up
                      </button>
                    </SignUpButton>
                  </>
                ) : (
                  <UserButton />
                )}
              </div>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
