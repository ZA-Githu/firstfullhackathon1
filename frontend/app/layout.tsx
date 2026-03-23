import type { Metadata } from "next";
import { Inter, Sora } from "next/font/google";
import { ThemeProvider } from "next-themes";
import { ClerkProvider } from "@clerk/nextjs";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { SkipLink } from "@/components/layout/SkipLink";
import "./globals.css";

/** Inter — body font (variable weight, optimised by next/font) */
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

/** Sora — heading font */
const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sora",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "AI-Native Driven Development",
    template: "%s | AI-Native Driven Development",
  },
  description:
    "A comprehensive guide to building software systems where AI is a first-class citizen — not an afterthought.",
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"
  ),
};

/**
 * Root layout — wraps every page with ThemeProvider, Navbar, Footer, and SkipLink.
 * Fonts are loaded via next/font (zero CLS, self-hosted, privacy-preserving).
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${sora.variable}`}>
      <body className="font-sans antialiased min-h-screen flex flex-col">
        <ClerkProvider
          publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}
        >
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {/* Skip link — first focusable element for keyboard/screen reader users */}
            <SkipLink />

            {/* Site-wide navigation */}
            <Navbar />

            {/* Page content — id matches SkipLink href */}
            <main id="main-content" className="flex-1">
              {children}
            </main>

            {/* Site footer */}
            <Footer />
          </ThemeProvider>
        </ClerkProvider>
      </body>
    </html>
  );
}
