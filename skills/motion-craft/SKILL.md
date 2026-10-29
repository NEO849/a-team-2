---
name: motion-craft
description: >-
  Baut Web-/UI-Animation & Micro-Interactions, die eine strenge Review überleben — die Motion-Mechanik-
  Fähigkeit, die frontend-design/design-craft (statisch/Ästhetik) fehlt. Trifft die Entscheidungen in der
  Reihenfolge, die über „fühlt sich richtig an" bestimmt: soll es überhaupt animieren, welcher Zweck, welches
  Tool, welche Properties, welche Kurve/Dauer oder Spring, wie es unterbricht/exit. Schreibt die Implementierung
  in zwei Tracks — Projekt (React + Motion/GSAP) und CSP-sicheres Artifact/Single-File (WAAPI/CSS). Für
  Ästhetik/Layout/Anti-Slop-Gesamtbild siehe design-craft; für adversariale Kritik design-review; für
  deterministische Video-Renders remotion-video, für generatives Video video-move. NICHT für Video oder
  statisches Styling. Trigger "/motion-craft", "animiere <x>", "add motion <x>", "micro-interaction <x>",
  "scroll animation <x>", "welche easing/dauer <x>".
---

# motion-craft — Motion, die eine strenge Review überlebt

> Rolle: **Senior-Design-Engineer**, der die Animation selbst baut. Die Messlatte ist Emil Kowalskis
> Motion-Philosophie. Bau es so, dass es die Review beim ersten Mal besteht. Keine Motion-Optionen als Menü —
> die Entscheidung treffen, den Grund in einer Zeile nennen, den Code schreiben.

## Wann laden
Sobald etwas sich bewegen soll (Enter/Exit, Hover, State-Übergang, Scroll-Choreografie, Geste). Kommt aus
`design-craft` (Gesamtbild) oder direkt. Für das reine Ästhetik-/Layout-Urteil zurück zu `design-craft`.

## Zwei Failure-Modes (der erste ist schlimmer)
1. **Etwas animieren, das nicht animieren sollte.** Das Gate (motion-tables §1) darf null Zeilen Code produzieren — das ist Erfolg, keine Ausrede.
2. **Das Richtige mit falschen Zutaten** — `ease-in` auf Enter, `scale(0)`, Keyframes auf einem Toast, eine Dauer die ein Dropdown träge macht.

## Track zuerst klären
- **Projekt-Track:** Build vorhanden → Motion (`motion/react`) / GSAP ScrollTrigger. State-Regel: nie `useState` für kontinuierliche Werte → `useMotionValue`/`useTransform`/`useScroll`.
- **Artifact/Single-File-Track:** strikte CSP, kein Build, keine externen Libs → nur Vanilla-CSS + WAAPI + `@starting-style` + scroll-driven CSS. Siehe `artifact-design`.

## Bau-Sequenz (Reihenfolge ist Pflicht)
Die vollständigen Tabellen: **`references/motion-tables.md`** (Schritte 1-7: Gate → Zweck → Tool-Leiter → Properties → Easing/Dauer/Spring → Interruption/Exit → Reduced-Motion). In Kürze:
1. **Gate** (Frequenz-Tier) — 100+/Tag = nie animieren, Stop.
2. **Zweck** in einem Wort benennen (Feedback/Spatial/State/…), sonst nicht bauen.
3. **Tool** = das billigste, das funktioniert (CSS transition → `@starting-style` → CSS anim → WAAPI → Motion).
4. **Properties** = nur transform/opacity, nie `scale(0)`, transform-origin am Trigger.
5. **Easing/Dauer** aus der Tabelle (nie `ease-in` auf UI, UI <300ms) — oder ein Spring bei Geste/Momentum.
6. **Interruption/Exit** = Transitions für schnell-triggerbares, Exit wie Enter.
7. **Reduced-Motion + Pointer-Gating** shippen mit der Animation, jedes Mal.

## Fertige Muster & Verbote
- Copy-paste Skeletons (Scroll-Reveal, Sticky-Stack, Horizontal-Pan, Entrance, Toast, Glass) in beiden Tracks → **`references/recipes.md`**. Bei Match dort starten, nicht bei leerer Datei.
- **Never-Ship-Selbstkontrolle vor „fertig"** → **`references/forbidden.md`**.

## Output
Den Code schreiben, dann in wenigen Zeilen: Gate-Ergebnis (Tier + benannter Zweck; was abgelehnt wurde und warum) · Zutaten (Tool/Properties/Kurve/Dauer oder Spring, je eine Zeile) · Feel-Check (wenn das Ergebnis vom Gefühl abhängt: bei 2-5× Dauer abspielen / im DevTools-Animation-Inspector Frame-für-Frame / Gesten am echten Gerät). Der Code ist das Deliverable, kein Report.

## Hard-Gates (Abschluss)
- Ehrlich über Feel-Unsicherheit: wenn ein Wert nur am echten Gerät/Auge zu entscheiden ist, das sagen statt raten.
- Kein „fertig" ohne `forbidden.md`-Selbstkontrolle; bei Auslieferung → `design-review`.
- Artifact-Track: CSP-Regeln von `artifact-design` sind bindend (keine externen Libs/Fonts).

*Adaption aus emilkowalski/skills (MIT). Credits: `CREDITS.md`.*
