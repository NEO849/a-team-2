# Visual Pre-Flight — die mechanische Checkliste

> NICHT optional. Jede Box laufen. Fällt eine Box, ist der Output nicht fertig. Viele Boxen sind
> **mechanisch zählbar** — der Detektor `design-craft/scripts/design_lint.py` prüft die (`[det]`).
> Diese Liste operationalisiert `design-craft/references/craft-floor.md` in Gates.

## A. Brief & Intent
- [ ] „Design Read"-Einzeiler wurde deklariert (Seiten-Art/Zielgruppe/Vibe/Welt).
- [ ] Drei Dials begründet gesetzt; Modus (Persuade/Operate/Read/Experience) gewählt.
- [ ] Jede Brief-Anforderung präsent und in Sekunden findbar (Coverage).

## B. Anti-Slop mechanisch `[det]`
- [ ] **Null `—` / `–`** irgendwo im sichtbaren UI. `[det]`
- [ ] Eyebrow-Count ≤ `ceil(sektionen / 3)` (zähle `uppercase tracking`-Instanzen). `[det]`
- [ ] ≥4 verschiedene Layout-Familien pro 8 Sektionen; keine Familie 2× (Zigzag max 2 in Folge). `[det]` (Zigzag)
- [ ] Kein 3-Spalten-gleiche-Feature-Cards-Block; keine verschachtelten Cards. `[det]` (nested)
- [ ] Bento: N Items → N Zellen, keine leere Zelle.
- [ ] Kein Gradient-Text; keine doppelte CTA-Intent; CTA ≤3 Wörter, kein 2-Zeilen-Wrap. `[det]` (gradient-text)
- [ ] Keine „Production-Test Tells" (Version-Labels, Section-Nummer-Eyebrows, Scroll-Cues, Wetter/Locale-Strips, Fake-Version-Footer, div-Fake-UI). `[det]` (Teilmenge)

## C. Farbe & Tiefe
- [ ] Neutrale Basis + genau **ein** Akzent, über die Seite gelockt; kein AI-Purple-Glow.
- [ ] Nicht die gebannte Premium-Consumer-Warm-Palette (Hex-Blocklist, `craft-floor.md §2`). `[det]`
- [ ] Schatten haben Offset + Blur (kein Zero-Offset-Halo); Elevation einmal (Border *oder* Schatten).
- [ ] Kontrast: Body/Placeholder ≥4.5:1, große Schrift ≥3:1; Button-Kontrast WCAG-AA (kein weiß-auf-weiß).

## D. Typografie
- [ ] Nicht Inter/Fraunces/Instrument-Serif als Reflex-Default; Serif (falls genutzt) begründet.
- [ ] Emphasis in derselben Font-Familie; kein System-Display-Face als Own-World-Display-Stimme.
- [ ] Body-Maß 65-75ch; Tracking ≤ -0.02em auf Display; echte Copy an jedem Breakpoint, kein Overflow/Clipping.

## E. Motion (Detail: `motion-craft/references/forbidden.md`)
- [ ] Kein `transition: all`, kein `scale(0)`-Entrance, kein `ease-in` auf UI. `[det]`
- [ ] Kein `window.addEventListener('scroll')` / `useState` für kontinuierliche Werte. `[det]`
- [ ] Jede Animation motiviert (ein Satz); „Motion behauptet = Motion gezeigt".
- [ ] `prefers-reduced-motion` vorhanden; `:hover`-Motion pointer-gegatet. `[det]` (hover-gate)

## F. Zustände & Content
- [ ] Hover, disabled, loading, error, empty vorhanden. Echte Controls, Keyboard-Focus.
- [ ] Echte Bilder (auch bei Minimalismus); echtes Icon-Set (kein Emoji-als-Icon, kein hand-SVG-Deko). `[det]` (emoji-icon)
- [ ] Copy-Self-Audit gelaufen; keine Fake-Namen/Filler-Verben/Fake-Präzisions-Zahlen.

## G. Browser-Surfaces & Responsiveness
- [ ] Selection, Caret, Focus-Ring, Scrollbar, Underline-Offset, tabular-nums gethemt (`browser-surfaces.md`).
- [ ] Responsive Komposition (Desktop + Mobile getestet), Dark-Mode getestet falls im Scope.
- [ ] `outline:none` nie ohne `:focus-visible`-Ersatz. `[det]`

## H. Perf
- [ ] Nur transform/opacity animiert; CWV-Ziele LCP<2.5s / INP<200ms / CLS<0.1 plausibel.

---
*Adaption (Prosa) aus taste-skill (MIT, Pre-Flight) + impeccable (Apache-2.0, craft-floor Verify). Siehe `../CREDITS.md`.*
