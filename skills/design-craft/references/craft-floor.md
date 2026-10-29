# Craft-Floor — die Anti-Slop-Wahrheitsquelle

> Der **Boden**, nicht die Decke. Er hält die Mechanik sauber; die *Richtung* wählt das Brief
> (`aesthetic-worlds.md`) — nie diese Datei. Ein gepinntes Brief oder die committete Design-Welt
> schlägt jede Default-Regel hier; deine eigene Gewohnheit nicht.
> Geladen von `design-craft`, `motion-craft`, `design-review`. Der Detektor `scripts/design_lint.py`
> prüft die **maschinell zählbaren** Teile automatisch — handle nach seinen Findings, statt neu zu auditieren.

**Prinzip:** Das sind die *Defaults der Kategorie*, keine absoluten Verbote — das Brief kann fast
jeden zurückverdienen. Zu einem greifen, wenn die Achse frei ist, heißt: du hast nicht entschieden.

## TOC
1. Die harten Banns (kein Brief verdient sie zurück)
2. Farbe & Tiefe
3. Typografie & Schrift
4. Layout & Seiten-Gerüst
5. Motion (Kurzform — Voll-Tabellen in `motion-craft/references/`)
6. Copy & Content
7. Bilder, Icons, Fake-UI
8. „Production-Test Tells" — der belegte Katalog
9. Browser-Oberflächen (das billigste „gebaut statt zusammengeklickt"-Signal)

---

## 1. Die harten Banns — `[hard]`, kein Brief verdient sie zurück

- **`—` und `–` (Em-/En-Dash) im sichtbaren UI = Fail.** Kein „sparsam", kein „im Fließtext ok".
  Binär null. Grund: Modelle ignorieren Soft-Limits verlässlich, also ist die Regel zero-tolerance.
  Erlaubt: Bindestrich `-`, Minus in Mathe. Ersetze durch Punkt, Komma, Klammer oder Umformulierung.
- **Gradient-Text** als Betonung. Betonung kommt aus Gewicht oder Größe, nicht aus Farbverlauf-Schrift.
- **Eyebrow/Kicker über *jeder* Sektion.** Die Überschrift trägt ihr Gewicht selbst. (Restraint-Regel §4.)
- **Unicode-Glyphen/Emoji als Icon-System.** Icons sind gezeichnet (echte Lib oder authored SVG),
  ein konsistenter Stroke/Weight.
- **`window.addEventListener('scroll')` / `window.scrollY` in Framework-State / rAF-Loop auf State.**
  Zerstört Performance. Nutze Scroll-driven CSS (`animation-timeline`), Motion `useScroll`/`whileInView`
  oder GSAP ScrollTrigger.

## 2. Farbe & Tiefe

- **Die Lila-Regel:** Der „AI-Purple / Blue-Glow"-Look ist als Default verboten — keine automatischen
  lila Button-Glows, keine Zufalls-Neon-Gradients. Neutrale Basis (Zinc/Slate/Stone) + **ein**
  hochkontrastiger Akzent, Sättigung <80%, über die ganze Seite gelockt.
- **Premium-Consumer-Palette-Bann** (zweithäufigster Tell): beige/cream + brass/clay/oxblood/ochre +
  espresso für „artisan/wellness/luxury" macht die Marke unsichtbar. Verbotene Hex-Familien als Default:
  - BG: `#f5f1ea #f7f5f1 #fbf8f1 #efeae0 #ece6db #faf7f1 #e8dfcb`
  - Akzent: `#b08947 #b6553a #9a2436 #9c6e2a #bc7c3a #7d5621`
  - Text: `#1a1714 #1a1814 #1b1814`
  - Stattdessen rotieren (nicht zweimal in Folge dieselbe): Cold-Luxury, Forest, Black-and-Tan,
    Cobalt+Cream, Terracotta+Slate, Olive+Brick+Paper, Monochrom+Pop.
- **Tiefe:** Schatten tragen Offset **und** weichen Blur. Ein Zero-Offset-Farbhalo ist Deko, kein System.
- **Elevation einmal deklarieren** — Border *oder* Schatten. 1px-Border unter breitem weichem Schatten = Ghost-Card.
- **Kein farbiger `border-left/right` >1px** auf Cards/List-Items/Callouts/Alerts (Side-Stripe-Tell).
- **Hard-Offset-Schatten** (`box-shadow: 4px 4px 0`) nur in einer echt neobrutalistischen Welt.
- **Kontrast prüfen:** Body/Placeholder ≥4.5:1, große Schrift ≥3:1. Sekundärtext auf farbiger Fläche
  aus dem Hue tönen, nie neutrales Grau.
- **Theme aus der Nutzungs-Szene** wählen (wer, wo, welches Umgebungslicht) — nicht aus der Kategorie.

## 3. Typografie & Schrift

- **Inter nicht als Reflex-Default.** Zuerst `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi` oder eine
  brand-passende Serif erwägen. (Override: neutral/Linear-Stil/Behörde → System-Sans ok.)
- **Serif-Disziplin (als Default sehr entmutigt):** „fühlt sich creative/premium/editorial an" ist KEIN
  Grund. „Creative Brief = Serif" ist der meistgetestete AI-Tell. Serif nur wenn Brand eine nennt ODER
  echt editorial/luxury/heritage mit artikuliertem Warum. **Als Default gebannt: `Fraunces`, `Instrument Serif`.**
  Serif über aufeinanderfolgende Projekte rotieren, nie dieselbe wiederverwenden.
- **Emphasis in derselben Font-Familie** (Italic/Bold), nie ein Zufalls-Serif-Wort in eine Sans-Headline.
- **System-Display-Face** (Impact, Arial Black, Plattform-Sans) als Display-Stimme einer Own-World-Seite = Fail.
  Eine Face mit passendem Charakter beschaffen/self-hosten.
- **Floor:** Body-Maß 65–75ch, Display max ~6rem, Tracking-Boden -0.04em (oft liest -0.02…-0.03em besser),
  balancierte Headings, klare Scale-/Weight-Stufen. Echte Copy an jedem Breakpoint laufen lassen, Overflow fixen.
- **Italic-Descender-Clearance:** Italic-Display-Wörter mit `y g j p q` brauchen `line-height ≥1.1` + Reserve, sonst Clipping.

## 4. Layout & Seiten-Gerüst

- **Nicht als Struktur:** gleich-große Icon+Heading+Text-Cards als Seitengerüst. Cards sind der faule
  Container; verschachtelte Cards sind immer falsch. Kein 3-Spalten-gleiche-Feature-Cards-Block.
- **Hero-Metric-Template** (große Zahl, kleines Label, Support-Stats, Akzent) — verbraucht.
- **Eyebrow-Restraint** (der #1-verletzte Test): max 1 Eyebrow pro 3 Sektionen. Mechanisch: zähle
  `uppercase tracking`-Instanzen; > ceil(sektionen/3) = Fail. Alternative: weglassen.
- **Section-Nummern (01/02/03)** nur wenn die Sequenz echte Info trägt.
- **Zigzag-Cap:** max 2 Sektionen in Folge im image+text-split-Muster; die 3. = Fail.
- **Split-Header-Bann** (links große Headline + rechts kleiner Erklär-Absatz) als Default; stattdessen stacken.
- **Layout-Wiederholungs-Bann:** jede Layout-Familie höchstens einmal; 8 Sektionen → ≥4 verschiedene Familien.
- **Bento-Cell-Count:** N Items → N Zellen, keine leere Mittel-/End-Zelle. 2–3 Zellen brauchen echte visuelle Varianz.
- **Hero fittet initialen Viewport:** Headline ≤2 Zeilen, Subtext ≤20 Wörter/≤3-4 Zeilen, CTA ohne Scroll sichtbar.
  Hero-Top-Padding-Cap ~`pt-24`. Max 4 Text-Elemente im Hero (keine Trust-Strips/Pricing-Teaser/Feature-Bullets darin).
- **Modal nur** wo Unterbrechung/geschützter Fokus nötig ist — nicht per Reflex.
- **Grid vor Flex-Prozent-Mathe.** Nav einzeilig, ≤80px. `min-h-[100dvh]`, nie `h-screen`.
- **Keine doppelte CTA-Intent** („Get in touch" + „Let's talk" = Fail) — ein Label pro Intent. CTA ≤3 Wörter, kein 2-Zeilen-Wrap.

## 5. Motion (Kurzform)

Voll-Tabellen & Skeletons: `motion-craft/references/motion-tables.md`, `recipes.md`, `forbidden.md`. Der Boden hier:
- **Ein authored Moment**, nicht verstreute Effekte und nicht dieselbe identische Entrance auf jeder Sektion.
- Exponentielles ease-out aus einem bereits sichtbaren Default. Über transform/opacity hinausgreifen:
  blur, backdrop-filter, clip-path, mask, shadow gehören zur Palette, solange sie smooth bleiben.
- **Nie `ease-in` auf UI**, nie `transition: all`, nie `transform: scale(0)`-Entrance (→ `scale(0.95)`+`opacity:0`).
- **Motion muss motiviert sein** (Hierarchie/Feedback/State/Storytelling in einem Satz). „Sah cool aus" ist ungültig.
- **`prefers-reduced-motion`** immer mitliefern (sanfter, nicht null). Marquee max 1/Seite.

## 6. Copy & Content

- **Die Produkt-eigene Sprache.** Controls benennen ihre Aktion; Fehler benennen Problem UND Recovery.
- **Copy-Self-Audit:** jeden sichtbaren String neu lesen — grammatisch kaputt, unklarer Bezug,
  „LLM will tiefsinnig klingen"-Phrasen raus.
- **Keine Fake-Präzisions-Zahlen** außer echt oder als Mock gelabelt. Kein „Jane/John Doe / Acme / Nexus /
  SmartFlow", keine Filler-Verben (Elevate, Seamless, Unleash, Next-Gen, Revolutionize).
- **Coverage:** jede Brief-Anforderung präsent und in Sekunden findbar.

## 7. Bilder, Icons, Fake-UI

- **Echte Bilder auch bei Minimalismus.** Eine reine Text-Seite ist nicht Minimalismus, sie ist unfertig.
  Image-Gen-Tool zuerst wenn verfügbar; sonst `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`.
- **Div-basiertes Fake-Produkt-UI = der #1-LLM-Design-Tell.** Kein hand-gerolltes Deko-/Icon-SVG →
  Phosphor/HugeIcons/Radix/Tabler (Lucide nur auf Wunsch). Logo-Walls: echte SVG-Logos (Simple Icons/devicon), nie Text-Wordmarks.
- **Real illustration or none.** Sketch-Style-SVG-Szenen, `doodle`/`loose-sketch`-Klassen, `feTurbulence`-Grain
  lesen sich amateurhaft. Verbietet SVG das Bilder imitiert — nie SVG das Geometrie macht (Diagramme, Linework, Shader bleiben first-class).

## 8. „Production-Test Tells" — der belegte Katalog `[det]`

Aus echten generierten-Seiten-Fehlern geerntet; als Default gebannt:
- Version-Labels im Hero (`V0.6`, `BETA`, `EARLY ACCESS`), Fake-Version-Footer (`v0.6.2-rc.1`, `last sync 4s ago`).
- Section-Nummer-Eyebrows (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`).
- Rationierter Middledot `·` (max 1/Zeile), dekorative farbige Status-Dots (null by default).
- `<br>`-gebrochene, italic-gesetzte Headlines; vertikal rotierter Text; Crosshair/Hairline-Grid-Deko.
- „Quietly in use at" / „Field notes" / „On our desks"-Poesie-Labels; Wetter/Locale/Zeit-Strips (`LIS 14:23 · 18°C`).
- Generische Step-Labels („Stage 1/2/3"), Pills über Bildern, Photo-Credit-Captions als Deko.
- `border-t`+`border-b` auf jeder Spec-Zeile; gefüllte Progress-Bars als Deko.
- **Scroll-Cues** („Scroll", „↓ scroll") — wer noch nicht scrollte, sieht den Hero und weiß was Scrollen ist.
- Hero-Bottom-Deko-Strips (`BRAND. MOTION. SPATIAL.`).

## 9. Browser-Oberflächen

Die Teile, die du nicht gezeichnet hast, tragen trotzdem das Design. Text-Selection, Caret, Custom-Scrollbars,
Focus-Rings, Underline-Offset, tabular-nums in Datentabellen — alle shippen mit Browser-Defaults, die zu keinem
Design-System gehören. Aus der Palette themen. **Das billigste Signal, dass eine Seite gebaut statt zusammengeklickt
wurde — und das, was Modelle am verlässlichsten überspringen.** Detail: `design-review/references/browser-surfaces.md`.

---
*Synthese/Adaption (Prosa, kein Fremd-Code) aus: pbakaus/impeccable (Apache-2.0, `craft-floor`),
Leonxlnx/taste-skill (MIT, „AI-Tells" + Paletten-Banns), emilkowalski/skills (MIT, Motion-Banns). Siehe `../CREDITS.md`.*
