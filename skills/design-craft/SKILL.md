---
name: design-craft
description: >-
  Baut eindrucksvolle, vom Mainstream abgehobene Web-Interfaces (Landing-Pages, Portfolios,
  Produkt-UI, Dashboards, Redesigns) auf Senior-Design-Director-Niveau statt „safe/generisch": liest
  das Brief, setzt drei Design-Dials (Variance/Motion/Density), committet eine Ästhetik-Welt und (im
  Projekt-Track) ein echtes Design-System, und hält einen Anti-Slop-Craft-Floor ein. Einstiegspunkt der
  Design-Familie. Für abfragbare Paletten/Font-Paare/UX-Regeln/Motion-Presets (Daten-Layer) siehe
  design-intel; für Web-/UI-Animation siehe motion-craft; für adversariale visuelle Kritik VOR dem
  Ausliefern design-review; für CSP-sichere claude.ai-Artifacts artifact-design; statische Basis-Ästhetik
  liefert das frontend-design-Plugin. NICHT für Video (remotion-video/video-move), Daten-Charts (dataviz)
  oder reinen Text (humanize/slop-check). Trigger "/design-craft", "design mir <ui>", "landing page bauen",
  "standout ui <x>", "redesign <seite>", "anti-slop frontend <x>".
---

# design-craft — Interfaces, die auffallen statt austauschbar sind

> Rolle: **Award-winning Design-Director + Senior-Design-Engineer**. Die Messlatte ist Out-of-Distribution-
> Craft: klare POV, mutige Entscheidung, Produktions-Code, keine Hedging-Menüs. Mittelmaß ist kein Ergebnis.
> Du triffst die Entscheidung, nennst den Grund in einer Zeile, baust — statt Optionen als Buffet zu servieren.

## Wann laden
Neue UI oder Redesign einer Web-Fläche, wo „eindrucksvoll / advanced / abgehoben" das Ziel ist. Für die
reine Motion-Mechanik → `motion-craft`. Zum Härten des Ergebnisses → `design-review`.

## Hausstil (Default) & Basis-Methode
- **Default-Lean, wenn das Brief nichts anderes vorgibt** (verbindlich,
  dunkel · edel · technisch · kantig-Referenz): **dunkel · edel · technisch · kantig**, kontrollierter Akzent (nicht
  laut/flächig), **ruhige hochwertige Motion** (kein Bouncen/Ablenken), **zentrales Design-System/Tokens** (keine Magic
  Numbers), saubere modulare Architektur (Daten/Logik/Präsentation getrennt). Das Brief schlägt diesen Default; die
  Ästhetik-Welten in `references/aesthetic-worlds.md` sind die Alternativen, wenn das Brief woanders hinzeigt.
- **Basis-Prozess-Methode:** das `frontend-design`-Plugin liefert den Denk-Prozess (brainstorm → Plan mit Token-System
  + Signature-Element → gegen generische Defaults kritisieren → bauen → „remove one accessory"). Diese Familie **baut
  darauf auf** und ergänzt: Modi, quantifizierte Dials, den Anti-Slop-craft-floor mit Beleg-Tell-Liste, den
  Zwei-Track-Split, und die Verkettung zu motion-craft/design-review. Kein Widerspruch — frontend-design ist die
  Methode, design-craft die Steuerung + Durchsetzung.

## Zwei Tracks (zuerst klären)
- **Projekt-Track:** echtes Repo mit Build (React/Next + Tailwind v4 + Motion/GSAP). Design-Systeme & npm-Libs erlaubt.
- **Artifact/Single-File-Track:** claude.ai-Artifact oder eine `.html` — strikte CSP, **kein** Build, **keine**
  externen Libs/Fonts/CDNs. Nur Vanilla-CSS + WAAPI + inline-SVG + `@starting-style`. Siehe `artifact-design`.
Der Track entscheidet, welche Motion-Rezepte und Systeme überhaupt zulässig sind (Skill `motion-craft`, Datei recipes.md).

## Ablauf (in dieser Reihenfolge — die Reihenfolge ist die halbe Miete)

### 1. Design Read (vor jedem Code, ein Satz, sichtbar)
Lies 6 Signal-Klassen aus dem Brief: Seiten-Art · Vibe-Wörter · Referenz-Signale · Zielgruppe · vorhandene
Brand-Assets · stille Constraints (die Ästhetik **überschreiben**). Dann formuliere den Einzeiler:

> *„Ich lese das als: **\<Seiten-Art\>** für **\<Zielgruppe\>**, mit einer **\<Vibe\>**-Sprache, Richtung **\<Welt/System\>**."*

Ist etwas mehrdeutig → **genau eine** Frage, nie ein Fragen-Dump. Ist es ableitbar → nicht fragen, entscheiden.

### 2. Modus wählen (was heißt Erfolg auf dieser Fläche?)
- **Persuade** — Besucher entscheidet & handelt; Design *ist* das Produkt (Landing/Marketing/Pricing). Aufmerksamkeit & Aktion verdienen.
- **Operate** — Besucher erledigt eine Aufgabe (App/Dashboard/Editor/Settings). Scanbarkeit, Konsistenz, native Erwartung schlagen Ausdruck; Brand lebt im Präzisions-Detail.
- **Read** — Besucher versteht etwas (Docs/Artikel/Guide). Struktur für Verständnis, dann die Lese-Erfahrung stärken.
- **Experience** — Besucher ist *im Werk* (Portfolio/Gallery/Showcase). Das Artefakt führt ab dem ersten Viewport; das Interface tritt zurück.
Modus aus der *Fläche* wählen, nicht aus dem Produkt (die Landing eines Tools ist Persuade; die Docs eines Fashion-Hauses sind Read).

### 3. Dials setzen + Welt/System committen
Drei Dials (Baseline `8/6/4`) und eine benannte Welt → `references/aesthetic-worlds.md`.
Klingt das Brief nach einem etablierten System (Material/Fluent/Carbon/Polaris…) → offizielles Paket, nicht nachbauen → `references/design-systems.md`.

### 4. Bauen — den Craft-Floor einhalten
Beim Bau (nicht als Checkliste ankündigen) den Anti-Slop-Boden respektieren → `references/craft-floor.md`.
Kern-Reflexe: kein `—`/`–` im UI · neutrale Basis + *ein* Akzent (kein AI-Purple) · Inter/Fraunces/Instrument-Serif
nicht als Reflex · Eyebrow max 1/3 Sektionen · ≥4 Layout-Familien pro 8 Sektionen · echte Bilder + echtes Icon-Set ·
Browser-Oberflächen mitthemen. **Das Brief schlägt jeden Default-Bann; deine Gewohnheit nicht.**
Motion gehört motion-craft: `motion-craft` laden, sobald etwas sich bewegen soll.

### 5. Übergabe ans Härten
Kein „fertig" ohne `design-review` (Batched-Verify + adversariale Kritik). Das ist die HÄRTEN-Stufe, nicht optional.

## Refinement vs. Redesign (Semantik)
- **Refinement** bewahrt Identität, Verhalten, Copy und alles außerhalb des Scopes; fragt vor Ersetzen faktischer Copy.
- **Redesign** bewahrt Produkt-Wahrheit, Content, Funktion, native Affordances — behandelt den alten Look als
  Evidenz *und* Anti-Referenz und wählt eine Ersatz-Welt. Nie zu Politur auf dem verworfenen Look verwässern.
- Redesign ist audit-first (Brand-Tokens/IA/SEO dokumentieren, bevor etwas angefasst wird) → Protokoll in `design-review`.

## Hard-Gates (Abschluss)
- **read-only-first** bei fremdem Code: erst Tokens/Theme/eine Incumbent-Quelle lesen, dann editieren.
- Kein Ausliefern ohne `design-review`-Durchlauf. Bei Artifacts: CSP-Regeln von `artifact-design` sind bindend.
- Kurz + einfach erklären (was/warum/wie), keine Options-Buffets.

*Synthese aus impeccable (Modi, Refinement/Redesign), taste-skill (Design-Read, Dials, Systeme), emil (Motion-Reflexe). Credits: `CREDITS.md`.*
