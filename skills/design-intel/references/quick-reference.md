# design-intel — UX Quick-Reference (Volltext)

> Generiert aus `data/ux-guidelines.json` (Single Source of Truth). Neu erzeugen:
> `python3 scripts/gen_quickref.py` (siehe unten) — oder Datei-Objekt in der JSON ändern.
> Nur bei Bedarf laden; für die gezielte Abfrage `search.py --domain ux "<problem>"`.

## 1. Accessibility  (7 Regeln)
- **a11y-contrast** — Body text contrast ≥ 4.5:1; large text (≥24px or 19px bold) ≥ 3:1; UI components/graphics ≥ 3:1.
  - ✗ Anti-Pattern: Gray-on-gray, low-contrast placeholder text used as labels.
- **a11y-focus-visible** — Every interactive element has a visible focus ring (2px, ≥3:1 against its background). Never remove focus outlines without a stronger replacement.
  - ✗ Anti-Pattern: outline:none with no substitute — keyboard users get lost.
- **a11y-keyboard** — All functionality is reachable and operable by keyboard alone, in a logical tab order; no keyboard traps.
  - ✗ Anti-Pattern: Custom widgets that only respond to mouse/hover.
- **a11y-labels** — Icon-only buttons carry an accessible name (aria-label or visually-hidden text). Images have alt; decorative images use empty alt or aria-hidden.
  - ✗ Anti-Pattern: Icon buttons with no name; alt text describing 'image'.
- **a11y-target-size** — Interactive targets ≥ 44×44px (WCAG 2.5.5 / Apple HIG), with ≥8px spacing between adjacent targets.
  - ✗ Anti-Pattern: Tiny tap targets crammed together on mobile.
- **a11y-motion** — Honor prefers-reduced-motion: disable or reduce non-essential animation; never gate content behind motion.
  - ✗ Anti-Pattern: Parallax and autoplay that ignore the OS reduced-motion setting.
- **a11y-auth** — Do not require a cognitive test (memorizing, transcribing) to authenticate; allow paste and password managers (WCAG 2.2 Accessible Authentication).
  - ✗ Anti-Pattern: Blocking paste in password/OTP fields.

## 2. Touch  (4 Regeln)
- **touch-feedback** — Every tap/click gives feedback within 100ms (pressed state, ripple, or optimistic update). No 0ms silent state changes.
  - ✗ Anti-Pattern: Button that looks dead until the network returns.
- **touch-loading** — Show loading state for anything >300ms: skeletons for content, spinners for actions, disabled+label for buttons.
  - ✗ Anti-Pattern: Frozen UI with no signal that work is happening.
- **touch-hover-not-only** — Never hide essential actions behind hover only — touch devices have no hover. Provide a persistent or tap-revealed path.
  - ✗ Anti-Pattern: Row actions that only appear on :hover.
- **touch-destructive-confirm** — Destructive actions need friction: confirm dialog, undo window, or type-to-confirm. Prefer undo over confirm for reversible ops.
  - ✗ Anti-Pattern: One-tap permanent delete with no undo.

## 3. Performance  (4 Regeln)
- **perf-image-format** — Serve WebP/AVIF with width/height set; lazy-load below-the-fold images; use responsive srcset.
  - ✗ Anti-Pattern: Full-res PNG hero shipped to phones.
- **perf-cls** — Reserve space for images, ads, embeds and fonts to keep CLS < 0.1; use aspect-ratio and font-display:swap with metric-adjusted fallbacks.
  - ✗ Anti-Pattern: Content jumping as images and fonts load.
- **perf-list-virtualize** — Virtualize lists beyond ~100 rows; paginate or windowing rather than rendering thousands of nodes.
  - ✗ Anti-Pattern: Rendering a 5000-row table into the DOM at once.
- **perf-main-thread** — Keep the main thread free: debounce/throttle input handlers, move heavy work off the render path, avoid layout thrash (batch reads then writes).
  - ✗ Anti-Pattern: Scroll handler doing synchronous layout every frame.

## 4. Style  (4 Regeln)
- **style-consistency** — Commit to one aesthetic and apply it consistently — one radius scale, one shadow system, one spacing scale. Consistency reads as craft.
  - ✗ Anti-Pattern: Mixing flat and skeuomorphic, three radii, random shadows.
- **style-svg-icons** — Use a single SVG icon set (one weight/family). Never use emoji as UI icons.
  - ✗ Anti-Pattern: Emoji sprinkled as functional icons.
- **style-elevation** — Express hierarchy with one consistent elevation language (border OR shadow OR surface tint) — pick one primary and use it everywhere.
  - ✗ Anti-Pattern: Heavy drop-shadows on a flat/brutalist layout.
- **style-restraint-accent** — One accent color carries interaction and emphasis. Everything else is neutral. Restraint reads as premium.
  - ✗ Anti-Pattern: Four competing brand colors on one screen.

## 5. Layout  (5 Regeln)
- **layout-mobile-first** — Design mobile-first with fluid breakpoints; content reflows, no fixed-px containers that overflow small screens.
  - ✗ Anti-Pattern: Desktop-only layout that forces horizontal scroll on phones.
- **layout-no-hscroll** — No unintended horizontal scroll; set a 16px side gutter minimum; test at 320px width.
  - ✗ Anti-Pattern: A wide element pushing the viewport sideways.
- **layout-viewport-zoom** — Set viewport meta correctly and never disable pinch-zoom (no maximum-scale=1, no user-scalable=no).
  - ✗ Anti-Pattern: Disabling zoom 'for design reasons'.
- **layout-measure** — Cap body text measure at 60-75 characters; center long-form in a readable column rather than full-bleed.
  - ✗ Anti-Pattern: Paragraphs running the full 1440px width.
- **layout-grid** — Use a consistent grid/spacing scale (e.g. 4px base) for every gap and inset; no magic numbers.
  - ✗ Anti-Pattern: Ad-hoc 13px/17px/23px paddings.

## 6. Typography  (4 Regeln)
- **typo-base-size** — Base body ≥16px, line-height ~1.5; never set body copy below 12px.
  - ✗ Anti-Pattern: 11px body text to fit more in.
- **typo-scale** — Use a modular type scale (e.g. 1.2-1.333 ratio) with a limited step count; enforce clear H1>H2>H3 hierarchy.
  - ✗ Anti-Pattern: Six heading sizes all within 2px of each other.
- **typo-tracking** — Tighten tracking on large display (-0.01 to -0.03em); leave body at default. Balance headings (text-wrap:balance) and avoid orphans.
  - ✗ Anti-Pattern: Loose tracking on huge headings; a one-word orphan line.
- **typo-color-tokens** — Drive text color from semantic tokens (text/muted/inverse), not raw hex per component.
  - ✗ Anti-Pattern: Hardcoded #333 scattered across components.

## 7. Animation  (4 Regeln)
- **anim-purposeful** — Motion must convey meaning (spatial continuity, causality, state) — not decorate. If it does not aid understanding, cut it.
  - ✗ Anti-Pattern: Everything spins/bounces on load.
- **anim-timing** — Use context-aware timing: micro (100-150ms), UI transitions (200-300ms), larger moves (300-500ms). Not one duration for everything.
  - ✗ Anti-Pattern: Every transition set to a flat 500ms.
- **anim-exit-faster** — Exits are faster than entrances; use ease-out for enters, ease-in for exits. Springs for interactive/dragged elements.
  - ✗ Anti-Pattern: Slow linear fades that make the UI feel sluggish.
- **anim-cheap-props** — Animate only transform and opacity for 60fps; never animate width/height/top/left in hot paths (they trigger layout).
  - ✗ Anti-Pattern: Animating width/height on scroll.

## 8. Forms  (5 Regeln)
- **forms-visible-labels** — Every field has a persistent visible label; placeholders are hints, never the label.
  - ✗ Anti-Pattern: Placeholder-only fields that lose their label on input.
- **forms-inline-validation** — Validate inline near the field on blur/submit; show the error adjacent with a clear fix, not only a summary at the top.
  - ✗ Anti-Pattern: Generic 'error occurred' banner at page top.
- **forms-error-clarity** — Error messages state what is wrong and how to fix it, in plain language; never blame the user or use codes alone.
  - ✗ Anti-Pattern: 'Invalid input' with no guidance.
- **forms-progressive** — Ask only what is needed now; use progressive disclosure and sensible defaults; group related fields.
  - ✗ Anti-Pattern: A 30-field form on first contact.
- **forms-input-types** — Use correct input types/inputmode/autocomplete so mobile keyboards and password managers help the user.
  - ✗ Anti-Pattern: type=text for email/phone/number.

## 9. Navigation  (4 Regeln)
- **nav-hierarchy** — Keep primary nav shallow and predictable; surface the most-used destinations, hide the rest under clear grouping.
  - ✗ Anti-Pattern: A flat mega-menu of 30 equal links.
- **nav-bottom-limit** — Mobile bottom nav ≤5 items; put the primary destinations there, not everything.
  - ✗ Anti-Pattern: Seven crammed bottom-tab icons.
- **nav-back-behavior** — Back must be predictable; preserve scroll and state on return; support deep links to any meaningful view.
  - ✗ Anti-Pattern: Back that dumps the user to home and loses state.
- **nav-current-location** — Always show where the user is (active state, breadcrumbs for depth) so they can orient and escape.
  - ✗ Anti-Pattern: No active indicator; user can't tell the current section.

## 10. Charts  (4 Regeln)
- **charts-not-color-only** — Never rely on color alone to distinguish series; add direct labels, patterns, or shapes; ensure colorblind-safe palettes.
  - ✗ Anti-Pattern: Red/green lines indistinguishable to colorblind users.
- **charts-legend-tooltip** — Provide readable legends and tooltips; prefer direct labeling over a distant legend when few series.
  - ✗ Anti-Pattern: A legend the user must map back and forth to read.
- **charts-honest-axis** — Start bar-chart axes at zero; do not truncate to exaggerate differences; label units.
  - ✗ Anti-Pattern: Truncated y-axis inflating a tiny difference.
- **charts-right-type** — Match chart type to intent: trend→line, comparison→bar, part-of-whole→stacked/treemap (not pie for many slices), distribution→histogram/box.
  - ✗ Anti-Pattern: A 12-slice pie chart.
