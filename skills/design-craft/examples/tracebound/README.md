# Beispiel: "Tracebound" Landing-Hero (Zwei-Track-Demo)

Ein Demo, das die Design-Familie (`design-craft` + `motion-craft` + `design-review`) an echtem Output zeigt.
Dasselbe Design in zwei Ziel-Runtimes, dieselben Werte/Regeln, nur die Motion-Engine wechselt.

- **`tracebound-hero.html`** — Artifact/Single-File-Track. CSP-safe: kein externes Font/Lib/Bild, alles inline,
  Motion via WAAPI + CSS + `@starting-style`, Scroll-Reveal via IntersectionObserver (kein Scroll-Listener).
  Diese Datei enthält das komplette Stylesheet, das **beide** Tracks teilen.
- **`Hero.tsx`** — Projekt-Track. React + `motion/react` (dieselben Easing/Dauer-Werte), `useReducedMotion`,
  gegateter Hover, SVG-Pfad-Draw via `pathLength`. Nutzt das Stylesheet aus der HTML-Datei.

## Design-Read
"Produkt-Landing-Hero für technisch-anspruchsvolle Früh-Adopter, präzise kinetische Dark-Tech-Sprache."
Modus Persuade. Bewusster Anti-Cluster-Move: statt "near-black + einsamer Acid-Green-Pop" eine Duoton-
Signal-Identität (Teal zu Amber als Latenz-Rampe = semantische Farbe mit Job, kein Deko-Pop).

## Verifiziert (design-review)
`design_lint.py` clean (0 Tells, nachdem ein Em-Dash im `<title>` gefixt wurde). Headless-Screenshot Desktop
+ Narrow: Ghost-Card-Fix bestätigt (Elevation nur via Schatten + inset Bezel), kein Overflow (Diagnose:
`scrollWidth == viewportWidth`). Bekannter Kompromiss: System-Sans als Display, weil Artifact-CSP Webfonts
blockt; im echten Projekt-Track einen Grotesk self-hosten.
