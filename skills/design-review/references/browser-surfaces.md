# Browser-Surfaces — die Teile, die du nicht gezeichnet hast

> Das billigste Signal, dass eine Seite *gebaut* statt zusammengeklickt wurde — und das, was Modelle am
> verlässlichsten überspringen. Alle aus der Palette themen, nicht mit Browser-Default shippen.

| Oberfläche | Default-Sünde | Fix |
|---|---|---|
| Text-Selection | Standard-Blau | `::selection { background: <akzent-tint>; color: <lesbar>; }` |
| Caret | Schwarz | `caret-color: <akzent>` auf Inputs/Editable |
| Custom-Scrollbar | OS-grau (wenn Deko gewünscht) | `scrollbar-color`/`scrollbar-width`; WebKit `::-webkit-scrollbar*` — sparsam, nur wo es passt |
| Focus-Ring | Weggeklickt (`outline:none` ohne Ersatz = a11y-Fail) | `:focus-visible { outline: 2px solid <akzent>; outline-offset: 2px; }` |
| Underline-Offset | Text klebt an der Linie | `text-underline-offset`, `text-decoration-thickness` |
| Zahlen in Tabellen | proportional, springen | `font-variant-numeric: tabular-nums` |
| Placeholder | zu blass/Kontrast <4.5:1 | Palette-getönt, Kontrast prüfen |
| Tap-Highlight (Mobile) | graues Rechteck | `-webkit-tap-highlight-color: transparent` + eigenes `:active` |

**Prüf-Trigger:** Diese 8 in *jedem* `design-review`-Durchlauf explizit gegenchecken — sie sind der schnellste
Nachweis von Craft und der häufigste Auslassungsfehler. Aus der committeten Welt/Palette themen, nicht generisch.

---
*Adaption (Prosa) aus pbakaus/impeccable (Apache-2.0, `craft-floor` Browser-Surfaces). Siehe `../CREDITS.md`.*
