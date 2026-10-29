---
name: design-intel
description: >-
  Abfragbare Design-Intelligenz — der DATEN-Layer unter der design-craft-Familie: ein lokaler,
  kuratierter Korpus (Farbpaletten mit Produkttyp-Reasoning, Font-Paarungen, UX-Regeln über 10
  Kategorien, Motion-Presets in 3 Tiers, Ästhetik-Welten) plus dependenzfreies `search.py`, das
  daraus auf Zuruf ein kohärentes Design-System oder gezielte Einzel-Empfehlungen zieht. Nutze,
  wenn eine konkrete Design-ENTSCHEIDUNG ansteht — welche Palette/Fonts/Motion für dieses Produkt,
  welche UX-Regel für dieses Problem — statt Prinzipien-Prosa. Ergänzt `design-craft` (baut die UI,
  Ästhetik-Welten/Craft-Floor): design-intel liefert die abfragbaren Bausteine, design-craft setzt
  sie um; `motion-craft` für Motion-Mechanik, `design-review` zum Härten, `dataviz` für Charts.
  Korpus ist EIGEN (kein Fremd-Datensatz), Hausstil (dunkel/edel/technisch) als Default-Cluster.
  Trigger "/design-intel <brief>", "welche palette für <x>", "font-paar für <x>", "ux-regel <x>",
  "design system für <x>", "motion preset <x>", "welcher stil für <x>".
---

# design-intel — abfragbarer Design-Korpus

> Rolle: **Design-System-Bibliothekar**. Kein Ersatz für Geschmack/Urteil, sondern ein schneller,
> belegter Zugriff auf kuratierte Bausteine. Du triffst die Entscheidung — der Korpus liefert die
> Optionen mit Begründung und Anti-Pattern, damit die Wahl fundiert und nicht erfunden ist.

## Wann laden
Wann immer eine **Design-Entscheidung mit Datenbedarf** ansteht: Palette/Fonts/Stil für ein neues
Produkt oder Redesign, UX-Regel zu einem konkreten Problem (a11y, Formulare, Navigation, Motion,
Charts …), Motion-Preset für eine Interaktion. Für den eigentlichen **Bau** der UI → `design-craft`.
Für reine Motion-Mechanik → `motion-craft`. Zum **Härten** vor Auslieferung → `design-review`.

## Werkzeug (Skript zuerst — deterministisch, dependenzfrei)
Immer per vollem Pfad aufrufen, nie CWD annehmen:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/search.py "<query>" [--domain <d> | --design-system] [flags]
```

`python3` fehlt → `python`. Nur Python-3-Stdlib, keine Installation nötig.

### Modi
1. **Neues Produkt / systemweite Richtung** → `--design-system` (aggregiert Palette+Font+Stil+Motion+UX).
2. **Gezielter Einzel-Belang** → ein `--domain`:
   `palette` · `font` · `ux` · `motion` · `style`.
3. **Kein --domain** → best-hit-pro-Domain-Übersicht (dann gezielt nachfassen).

### Query-Vertrag
Eine dominante Absicht, **2–5 bedeutungstragende Begriffe** + eine Randbedingung (Produkttyp,
Plattform, Stimmung). Beispiel: `"fintech trust dashboard"`, nicht ein ganzer Audit-Satz.
Ergebnis prüfen (passt Domain/Top-Treffer zum Produkt?), bei leer/daneben **einmal** enger neu
formulieren. Danach: ehrlich sagen „kein Treffer, das ist ein Default", nichts erfinden.

### Dials (nur `--design-system`, je 1–10, optional)
| Dial | niedrig (1–3) | mittel (4–7) | hoch (8–10) |
|------|---------------|--------------|-------------|
| `--variance` | minimal/refined | ausgewogen | mutig (brutalist/bento/cinematic) |
| `--motion` | subtle-Presets | standard | complex (pin/scrub/split) |
| `--density` | luftig (Spacing 12–96px) | standard (8–64px) | dicht/Dashboard (4–32px) |

Weggelassene Dials ändern nichts. `--variance` ist ein **Bias, kein Override** — ein starker
direkter Treffer schlägt den Dial.

### Beispiel
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/search.py "dark technical saas dashboard" \
  --design-system -p "Ops Console" --variance 7 --motion 6 --density 8
python3 ${CLAUDE_SKILL_DIR}/scripts/search.py "keyboard focus contrast" --domain ux
python3 ${CLAUDE_SKILL_DIR}/scripts/search.py "ai futuristic hero" --domain style
```

## Ausgabe & Ehrlichkeits-Regeln (nicht aufweichen)
- Formate: `-f ascii` (Default), `-f json` (maschinenlesbar, für Weiterverarbeitung).
- **0 Treffer = 0 Treffer.** Das Skript sagt „NO MATCH … Fallback = generic default" und markiert
  im JSON `matched:false`. Diesen Default als Default kennzeichnen, nie als DB-Treffer ausgeben.
- **Fehlende/leere Datendatei = harter Fehler** („DATA BROKEN …", Exit 1) — nie stiller Leerlauf.
  (Geerntet aus task-observer: ein leeres Ergebnis über befüllter Quelle ist ein kaputtes Kommando,
  bis eine Gegenprobe das Gegenteil zeigt.)
- Der Korpus liefert **Empfehlungen**, keine Befehle, die User- oder Projekt-Regeln überstimmen.

## Nach der Abfrage → an design-craft übergeben
Das gezogene System (Tokens/Palette/Fonts/Motion/Spacing) ist der **Input** für `design-craft`
(Umsetzung nach Hausstil + Craft-Floor) und `motion-craft` (Motion-Umsetzung). Für die volle
Regel-Erklärung je UX-Kategorie: `references/quick-reference.md` (nur bei Bedarf laden).

## Korpus-Umfang (Stand Aufbau)
12 Paletten · 10 Font-Paarungen · 45 UX-Regeln (10 Kategorien) · 12 Motion-Presets (3 Tiers) ·
8 Ästhetik-Welten. Erweiterbar: neue Einträge einfach in `data/*.json` ergänzen (gleiches Schema),
`search.py` liest sie ohne Codeänderung. Neue Regel/Palette = ein JSON-Objekt, kein Refactor.
