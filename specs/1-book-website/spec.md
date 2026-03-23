# Feature Specification: AI-Native Book Website

**Feature Branch**: `1-book-website`
**Created**: 2026-03-06
**Status**: Draft
**Input**: User description: "AI-Native Book Website — Create a premium Single source of truth book website AI-Native-Driven Development And explain 5 chapters of this topic."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — First-Time Visitor Discovers the Book (Priority: P1)

A curious developer or product leader lands on the Home page from a social link or search result.
They immediately see an arresting hero section with the book title, a compelling one-liner, and a
call-to-action that takes them straight into the book. Within 10 seconds they understand what the
book teaches, who it's for, and how to read it.

**Why this priority**: The Home page is the highest-traffic entry point. If it fails to communicate
value instantly, every other page becomes irrelevant.

**Independent Test**: Navigate to `/` on a fresh browser. The hero section, book preview cards for
all 5 chapters, and a "Start Reading" CTA are visible without scrolling on a 1440px viewport.
Value delivered: visitor is informed and guided.

**Acceptance Scenarios**:

1. **Given** a visitor arrives at `/`, **When** the page finishes loading, **Then** the hero section
   displays the book title "AI-Native Driven Development", a subtitle, and a prominent CTA button
   linking to `/book`.
2. **Given** a visitor scrolls below the hero, **When** the book preview section is visible,
   **Then** all 5 chapter cards are shown with chapter number, title, and a one-sentence description.
3. **Given** a visitor is on a 320px-wide mobile screen, **When** the page loads, **Then** the hero
   and chapter preview cards stack vertically with no horizontal overflow and all text remains legible.
4. **Given** a visitor activates the dark-mode toggle, **When** the switch completes, **Then** the
   entire page switches colour scheme instantly without a reload and the glassmorphism cards remain
   visually distinct.

---

### User Story 2 — Reader Reads the Full Book with Chapter Navigation (Priority: P1)

A reader opens the Book page and reads through the five chapters sequentially or jumps directly to
a chapter using a sticky table of contents. A progress bar at the top of the page tracks how far
through the book they have scrolled. They can navigate between chapters without leaving the page.

**Why this priority**: The Book page is the product — it must work flawlessly.

**Independent Test**: Navigate to `/book`. The ToC sidebar lists all 5 chapters with their 2 topics
each. Click Chapter 3 — page smooth-scrolls to that chapter. Scroll to the bottom of the page —
the progress bar reaches 100%. Value delivered: reader can consume the full book content.

**Acceptance Scenarios**:

1. **Given** a reader navigates to `/book`, **When** the page loads, **Then** a sticky sidebar (desktop)
   or collapsible menu (mobile) shows all 5 chapter titles and their 2 topic headings each (10 items total).
2. **Given** a reader clicks a chapter link in the ToC, **When** the navigation completes, **Then**
   the page smooth-scrolls to that chapter section and the active chapter is highlighted in the ToC.
3. **Given** a reader scrolls down the Book page, **When** they are at any point, **Then** a progress
   bar at the top of the viewport shows percentage read (0% at top, 100% at bottom).
4. **Given** a reader has scrolled past the midpoint, **When** they click a chapter above their current
   position in the ToC, **Then** the page scrolls upward smoothly to the correct anchor.
5. **Given** MDX content includes code blocks or callout boxes, **When** the content renders,
   **Then** code blocks have syntax highlighting and callouts have distinct background colours in
   both dark and light mode.
6. **Given** a reader is on a 375px mobile screen, **When** the Book page loads, **Then** the ToC
   is hidden by default and accessible via a floating "Contents" button; the reading area spans
   the full screen width.

---

### User Story 3 — Visitor Learns About the Author (Priority: P2)

A visitor navigates to the About page to understand who wrote the book and why. They see the author's
name, photo, biography, and the motivation behind the book. This builds trust before they commit to
reading or sharing.

**Why this priority**: Trust-building is secondary to core content but essential for conversion.

**Independent Test**: Navigate to `/about`. Author name, avatar/photo with alt text, biography
paragraph, and mission statement are all visible. Value delivered: visitor gains confidence in the
source.

**Acceptance Scenarios**:

1. **Given** a visitor navigates to `/about`, **When** the page loads, **Then** the author's name,
   profile image (with descriptive `alt` text), and biography are displayed.
2. **Given** the About page loads on a 768px viewport, **When** the layout renders, **Then** the
   author image and biography stack vertically with readable body text (≥ 16px).
3. **Given** a visitor uses a screen reader on the About page, **When** they navigate to the author
   image, **Then** the screen reader announces a meaningful description (not "image" or empty).

---

### User Story 4 — Visitor Joins the Waitlist via Contact Form (Priority: P2)

A visitor who wants updates or the physical/premium version fills out a waitlist form on the Contact
page. The form captures their name and email, saves the entry to localStorage (no backend required),
and displays a success confirmation. The form validates all fields before submission.

**Why this priority**: Waitlist capture is a business goal; missing it loses leads permanently.

**Independent Test**: Navigate to `/contact`. Submit the form with a valid name and email — a success
message appears. Refresh the page — the submission is retrievable from localStorage. Submit with an
empty email — an inline error appears without page reload. Value delivered: lead captured.

**Acceptance Scenarios**:

1. **Given** a visitor navigates to `/contact`, **When** the page loads, **Then** a waitlist form
   with Name, Email, and an optional Message field is displayed inside a glassmorphism card.
2. **Given** a visitor fills in all required fields and clicks Submit, **When** the form is submitted,
   **Then** a success confirmation message ("You're on the list!") replaces the form and the entry
   is saved to localStorage under the key `waitlist`.
3. **Given** a visitor clicks Submit with the Email field empty, **When** validation runs, **Then**
   an inline error message appears below the Email field and the form is NOT submitted.
4. **Given** a visitor enters an email without an `@` symbol, **When** validation runs, **Then**
   an inline error message "Please enter a valid email address" appears below the Email field.
5. **Given** a visitor navigates through the form using Tab only, **When** they reach the Submit
   button, **Then** all fields and the button were reachable in logical order with visible focus rings.

---

### User Story 5 — Dark / Light Mode Across All Pages (Priority: P2)

Any visitor can switch between dark and light display modes using a toggle in the navigation header.
Their preference persists across page refreshes and return visits. The site defaults to the visitor's
OS-level colour preference.

**Why this priority**: Expected on premium sites; inaccessible colour modes reduce credibility.

**Independent Test**: Load the site with OS set to dark mode — site renders dark. Toggle to light —
site switches instantly. Refresh — site stays light. Value delivered: comfortable reading in any environment.

**Acceptance Scenarios**:

1. **Given** a visitor's OS is set to dark mode, **When** the site loads for the first time,
   **Then** the dark colour scheme is applied automatically without flicker.
2. **Given** a visitor clicks the mode toggle, **When** the switch completes, **Then** the colour
   scheme changes immediately without a full page reload.
3. **Given** a visitor has toggled to light mode and refreshes, **When** the page loads, **Then**
   the light colour scheme is restored (preference read from localStorage).

---

### Edge Cases

- **Empty MDX file**: If a chapter MDX file has no body content, the Book page renders the chapter
  heading with a "Coming soon" placeholder rather than a blank section.
- **localStorage unavailable**: If the browser blocks localStorage (e.g., private mode with strict
  settings), the waitlist form still shows a success confirmation but warns the user that their
  entry may not persist.
- **Missing chapter slug**: If a deep-linked chapter anchor does not exist, the page scrolls to the
  top of the Book page rather than throwing an error.
- **Single-page scroll on mobile**: On very long chapter content, the ToC "Contents" button remains
  sticky at the bottom-right so it is always reachable.
- **System colour-scheme change mid-session**: If the OS theme changes while the site is open, the
  site does NOT change automatically (user's explicit localStorage preference takes precedence).

---

## Requirements *(mandatory)*

### Functional Requirements

**Home Page**

- **FR-001**: The system MUST render a hero section at `/` containing the book title
  "AI-Native Driven Development", a subtitle, and a CTA button linking to `/book`.
- **FR-002**: The system MUST display a book preview section below the hero showing all 5 chapters,
  each with chapter number, title, and a one-sentence description.
- **FR-003**: The home page MUST be responsive across 320px, 768px, and 1440px viewports with no
  horizontal overflow.

**Book Page**

- **FR-004**: The system MUST render all 5 chapters and their 2 topics each from MDX files located
  exclusively in `/content/chapters/`, automatically at build time.
- **FR-005**: The system MUST display a sticky table of contents on desktop viewports (≥ 768px)
  listing all 5 chapters and 10 topics, with the active section highlighted as the reader scrolls.
- **FR-006**: The system MUST display a collapsible "Contents" button on mobile viewports (< 768px)
  that opens a full-screen or overlay ToC panel.
- **FR-007**: Clicking any ToC item MUST smooth-scroll the page to the corresponding chapter or
  topic anchor.
- **FR-008**: The system MUST display a reading progress bar fixed to the top of the viewport on
  the Book page, updating in real time as the user scrolls (0% at top, 100% at bottom).
- **FR-009**: The system MUST render MDX code blocks with syntax highlighting and callout components
  with visually distinct styling in both dark and light modes.

**About Page**

- **FR-010**: The system MUST render an About page at `/about` containing the author's name, a
  profile image with descriptive `alt` text, and a biography section.

**Contact / Waitlist Page**

- **FR-011**: The system MUST render a waitlist form at `/contact` with required fields: Name and
  Email, and an optional Message field.
- **FR-012**: On valid form submission, the system MUST save the entry to localStorage under the
  key `waitlist` (as a JSON array) and display a success confirmation message.
- **FR-013**: On submission with an empty required field, the system MUST display an inline
  validation error and prevent form submission.
- **FR-014**: On submission with an invalid email format, the system MUST display a field-level
  error message and prevent form submission.
- **FR-015**: If localStorage is unavailable, the system MUST display the success confirmation
  but also show a warning that the entry may not have been saved.

**Dark / Light Mode**

- **FR-016**: The system MUST detect `prefers-color-scheme` and apply the matching mode on first load.
- **FR-017**: The system MUST persist the user's mode preference in localStorage and restore it on
  subsequent visits.
- **FR-018**: The mode toggle control MUST appear in the navigation header on all four pages.

**Navigation**

- **FR-019**: The system MUST display a site-wide navigation header on all four pages with links to
  Home, Book, About, and Contact.
- **FR-020**: The active page link in the navigation MUST be visually distinguished (colour, weight,
  or underline).
- **FR-021**: On mobile viewports, the navigation MUST collapse into a hamburger menu that expands
  and collapses with an updated `aria-expanded` attribute.

**Accessibility & Performance**

- **FR-022**: Every page MUST include a "Skip to main content" link as the first focusable element.
- **FR-023**: All interactive elements MUST be keyboard-operable with a visible focus ring.
- **FR-024**: The site MUST achieve Lighthouse Performance ≥ 90 and Accessibility ≥ 90 on all pages.

### Key Entities

- **Chapter**: Has `chapterNumber` (1–5), `title`, `description`, `slug`; contains 2 topics.
- **Topic**: Has `topicNumber` (1–2 within chapter), `title`, `slug`, `content` (MDX body).
- **WaitlistEntry**: Has `name` (string), `email` (string), `message` (string, optional),
  `submittedAt` (ISO date string); stored as array in localStorage key `waitlist`.
- **UserPreference**: Has `colorMode` (`"dark"` | `"light"`); stored in localStorage key `color-mode`.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time visitor can understand the book's topic and navigate to the first chapter
  within 10 seconds of landing on the Home page.
- **SC-002**: A reader can locate any specific chapter and begin reading within 5 seconds of arriving
  on the Book page, without using browser search.
- **SC-003**: The reading progress bar updates visibly within 100ms of the user scrolling.
- **SC-004**: A visitor can complete and submit the waitlist form (with valid inputs) in under
  60 seconds from arriving at the Contact page.
- **SC-005**: The site achieves a Lighthouse Performance score ≥ 90 on every page.
- **SC-006**: The site achieves a Lighthouse Accessibility score ≥ 90 on every page.
- **SC-007**: The site loads to First Contentful Paint in under 1.5 seconds on a simulated 4G connection.
- **SC-008**: The total JavaScript bundle is under 150 KB (gzip, images excluded).
- **SC-009**: The site renders correctly (no overflow, no broken layouts) on 320px, 768px, and
  1440px viewports in both dark and light modes.
- **SC-010**: A new chapter MDX file added to `/content/chapters/` appears in the Book page ToC
  automatically after a rebuild, with zero changes to application code.
- **SC-011**: The site is live on a public Vercel URL and accessible globally within 30 minutes of
  initiating the first deployment.

---

## Assumptions

- **A-001**: The author's name, biography text, and profile image asset will be provided before the
  About page is implemented; placeholder content will be used until then.
- **A-002**: Chapter and topic titles and full MDX content for all 5 chapters × 2 topics will be
  authored as part of implementation; the spec describes structure, not the content itself.
- **A-003**: The waitlist does not require server-side persistence at this stage; localStorage is
  the sole storage mechanism (no backend, auth, or email service).
- **A-004**: "Looks like a $10k website" is interpreted as: glassmorphism card components, gradient
  hero backgrounds, smooth animations, professional typography (two font families via `next/font`),
  and pixel-perfect alignment at all defined breakpoints.
- **A-005**: No payment, authentication, comments, or CMS integration is in scope for this release.

---

## Non-Goals

- Backend API, database, or server-side session management.
- User authentication or account creation.
- Payment processing or e-commerce.
- Comments, ratings, or social sharing features.
- Real-time data (analytics dashboards, live visitor counts).
- Email delivery (the waitlist only stores to localStorage).
- CMS integration (all content is static MDX).
