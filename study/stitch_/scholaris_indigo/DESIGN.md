# Design System Document: Academic Editorial

## 1. Overview & Creative North Star
**The Creative North Star: "The Digital Curator"**

This design system rejects the "cluttered repository" aesthetic common in educational platforms. Instead, it adopts a high-end editorial approach, treating exam papers not as mere files, but as curated knowledge. The system prioritizes "The Architecture of Focus"—a philosophy where every pixel serves to reduce cognitive load and elevate the student’s intent.

To break the "template" look, we utilize **Intentional Asymmetry** and **Tonal Depth**. By avoiding rigid, boxed-in grids and opting for layered surfaces and expansive white space, we create an environment that feels authoritative, sophisticated, and calm—essential for high-stakes exam preparation.

---

## 2. Colors & Surface Architecture
Our palette centers on "Academic Excellence"—a deep, commanding indigo supported by a sophisticated range of neutral surfaces that mimic the tactile quality of high-grade paper.

### The Color Logic
*   **Primary (`#000b60`) & Primary Container (`#142283`):** These are our anchors. Use the Primary color for high-level branding and primary actions. Use the Container for active states to maintain depth.
*   **Secondary (`#4858ab`):** Reserved for secondary actions and interactive highlights.
*   **Tertiary (`#00201c`):** Our "Subtle Accent." Use the Tertiary Fixed variants (`#8df5e4`) specifically for subject categorization (e.g., Science/Math) to provide a refreshing contrast to the deep indigo.

### The "No-Line" Rule
**Borders are strictly prohibited for sectioning.** Boundaries must be defined solely through background color shifts.
*   *Example:* A `surface-container-low` section sitting on a `surface` background.
*   *The Goal:* To create a seamless, fluid interface that feels like a single cohesive piece of digital stationery.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the hierarchy below to define importance:
1.  **Base Layer:** `surface` (#fbf8ff)
2.  **Structural Sections:** `surface-container-low` (#f5f2fb)
3.  **Interactive Elements/Cards:** `surface-container-lowest` (#ffffff)
4.  **Floating Overlays:** `surface-bright` (#fbf8ff)

### The "Glass & Gradient" Rule
To add "soul" to the professional polish, use subtle linear gradients (Primary to Primary Container) for Hero backgrounds. For floating search bars or navigation, apply **Glassmorphism**: use `surface` at 80% opacity with a `24px` backdrop blur to allow the academic content to subtly bleed through.

---

## 3. Typography: The Editorial Scale
We use a dual-font strategy to balance character with extreme readability.

*   **Display & Headlines (Manrope):** A geometric sans-serif that feels modern yet established. 
    *   *Usage:* Use `display-lg` for hero statements. Use `headline-sm` for subject titles to create an "Editorial Header" feel.
*   **Body & Titles (Inter):** A workhorse typeface designed for screen readability.
    *   *Usage:* All exam metadata, table data, and instructional text.
*   **The Hierarchy Intent:** High contrast between `display-md` (2.75rem) and `body-md` (0.875rem) creates a clear path for the eye, signaling what is context (the headline) and what is content (the paper details).

---

## 4. Elevation & Depth
We convey hierarchy through **Tonal Layering** rather than traditional drop shadows.

*   **The Layering Principle:** Place a `surface-container-lowest` card (Pure White) on a `surface-container-low` section. This creates a "soft lift" that feels natural and premium.
*   **Ambient Shadows:** If a floating effect is required (e.g., a focused search bar), use a shadow with a `40px` blur, `0%` spread, and `6%` opacity using the `on-surface` color.
*   **The "Ghost Border" Fallback:** For accessibility in input fields, use the `outline-variant` (#c6c5d4) at **15% opacity**. Never use 100% opaque borders.
*   **Glassmorphism:** Use for persistent headers. This integrates the UI into the content, making the platform feel like a single, immersive tool.

---

## 5. Components

### Search Bars & Inputs
*   **The "Global Search" Hero:** A large, `xl` (0.75rem) rounded container using `surface-container-highest`. No border. The focus state transitions the background to `surface-container-lowest` with an ambient shadow.
*   **Input Fields:** Use `body-lg` for user input. Labels use `label-md` in `on-surface-variant`.

### Category Cards
*   **Styling:** Forbid dividers. Use `surface-container-lowest` as the card base. 
*   **Subject Accents:** Use a 4px vertical "Signature Stripe" on the left edge using `tertiary_fixed` to denote different subjects without cluttering the card with icons.

### Progress Indicators
*   **The Focus Bar:** Use a thin (4px) track of `primary_fixed` with the active progress in `primary`. Avoid chunky bars; keep them "hairline" to maintain the editorial feel.

### Clean Data Tables (Exam Lists)
*   **The "No-Line" Table:** Remove all horizontal and vertical rules. 
*   **Separation:** Use alternating row fills of `surface` and `surface-container-low`, or simply use generous `16px` vertical padding (from the spacing scale) to let whitespace act as the separator.
*   **Typography:** Column headers must be `label-md` in all-caps with `0.05em` letter spacing for an authoritative look.

### Buttons
*   **Primary:** Solid `primary` background with `on-primary` text. Radius: `md` (0.375rem).
*   **Secondary:** `secondary_container` background. No border.
*   **Tertiary:** No background. Use `on-primary_fixed_variant` text with an underline that appears only on hover.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical margins. For example, a wider left margin for a page title to create a "magazine" layout.
*   **Do** use `surface-container` shifts to group related exam papers rather than drawing a box around them.
*   **Do** prioritize high-contrast typography over colorful icons. Let the text do the talking.

### Don’t:
*   **Don’t** use 1px solid borders. It shatters the "editorial" flow and makes the platform look like a generic database.
*   **Don’t** use pure black shadows. Always tint shadows with the `on-surface` indigo-grey to keep them "ambient."
*   **Don’t** crowd the interface. If a screen feels "busy," increase the whitespace between sections by 1.5x. Professionalism is found in the "breath" between elements.
*   **Don't** use standard blue for links. Use `primary` or `primary_container` for a more "ink-like" and scholarly appearance.