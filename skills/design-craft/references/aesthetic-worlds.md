# Aesthetic Worlds — Dials + benannte Design-Welten

> Die *Richtung* der Arbeit. Zuerst das Brief lesen (`design-craft` SKILL.md, „Design Read"), dann hier
> die drei Dials setzen und eine Welt committen. Der Craft-Floor (`craft-floor.md`) hält danach die Mechanik sauber.

## TOC
1. Die drei Dials (Definition + Skalen)
2. Signal → Dial-Inferenz
3. Use-Case-Presets (Startwerte)
4. Benannte Design-Welten
5. Anti-Repetition (der tiefe Slop-Grund)

---

## 1. Die drei Dials

Globale Intent-Variablen, überall exakt so benannt (keine Alias wie `LAYOUT_VARIANCE` erfinden).
Sie gaten konkrete Regeln per `>N`-Schwellen. **Baseline: `8 / 6 / 4`** (guter Standard-Landing-Startpunkt).

**DESIGN_VARIANCE** (1 = perfekte Symmetrie … 10 = artsy Chaos)
- 1-3 *Predictable:* symmetrisches Grid (12-col, gleiche fr), gleiche Paddings, zentriert.
- 4-7 *Offset:* `margin-top: -2rem`-Overlaps, gemischte Aspect-Ratios (4:3 neben 16:9), links-Header über center-Data.
- 8-10 *Asymmetric:* Masonry, `grid-template-columns: 2fr 1fr 1fr`, massive Leerzonen (`padding-left: 20vw`).
- **Mobile-Override:** Level 4-10 kollabieren unter 768px auf strikte Einspaltigkeit.

**MOTION_INTENSITY** (1 = statisch … 10 = cinematic/Physik)
- 1-3 *Static:* keine Auto-Animation, nur `:hover`/`:active`.
- 4-7 *Fluid CSS:* `transition … cubic-bezier(0.16,1,0.3,1)`, `animation-delay`-Kaskaden, transform/opacity.
- 8-10 *Advanced Choreography:* scroll-triggered Reveals, Parallax, `animation-timeline` oder GSAP ScrollTrigger.
  **Nie `window.addEventListener('scroll')`.**
- Regel-Gates: reduced-motion Pflicht ab >3 · „Motion behauptet = Motion gezeigt" ab >4 · magnetische Physik/perpetuelle Micro-Interactions nur ab >5.

**VISUAL_DENSITY** (1 = Art-Gallery/luftig … 10 = Cockpit/dicht)
- 1-3 *Art Gallery:* viel Weißraum, große Section-Gaps (`py-32`…`py-48`).
- 4-7 *Daily App:* Standard-Webapp-Spacing (`py-16`…`py-24`).
- 8-10 *Cockpit:* enge Paddings, keine Card-Boxen — 1px-Linien trennen Daten, `font-mono` für alle Zahlen.
- Gate: Card-Container gebannt ab >7.

## 2. Signal → Dial-Inferenz

Vibe-Wörter aus dem Brief auf Startwerte mappen (dann bewusst justieren):

| Brief-Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| „clean", „trust", „enterprise", „B2B", „Behörde" | 2-4 | 2-3 | 4-6 |
| „modern", „startup", „bold", „standout" | 7-9 | 5-7 | 3-5 |
| „editorial", „magazine", „story" | 6-8 | 4-6 | 3-4 |
| „luxury", „premium", „calm", „expensive" | 5-7 | 4-6 | 2-3 |
| „playful", „creative", „award-winning", „wow" | 8-10 | 7-9 | 3-5 |
| „dashboard", „data", „terminal", „pro tool" | 3-5 | 2-4 | 8-10 |

## 3. Use-Case-Presets

| Use-Case | Startwerte (V/M/D) |
|---|---|
| SaaS-Landing (standout) | 8 / 6 / 4 |
| Portfolio / Showcase | 8 / 7 / 3 |
| Editorial / Long-form | 7 / 5 / 3 |
| Premium-Consumer-Brand | 6 / 5 / 3 |
| Docs / Read-Surface | 3 / 2 / 5 |
| App-UI / Operate-Surface | 4 / 3 / 7 |
| **Redesign-Delta** | Overhaul `+2 / +2 / match existing`; Preserve `match / match / match` |

## 4. Benannte Design-Welten

Eine Welt committen (nicht mischen). Jede hat einen Kern, eine typische Dial-Range, und was sie kippt.

**Hausstil-Default**: ohne gegenteiliges Brief liegt der Default
zwischen **Dark-Tech** und **Soft-Premium** — dunkel/edel/technisch/kantig, kontrollierter Akzent (z.B. Orange/Amber),
ruhige Motion, Radien eher kantig (6-16). Erst wenn das Brief editorial/brutalist/playful verlangt, davon abweichen.

- **Soft-Premium** (V5-7 / M4-6 / D2-3): weicher Kontrast, großzügiger Weißraum, Premium-Font, Spring-Motion,
  gedämpfte Palette + *ein* ruhiger Akzent. Kippt in „teuer wirkende Blandheit" → braucht einen mutigen Typo- oder Bildmoment.
- **Editorial** (V6-8 / M4-6 / D3-4): starke Typo-Hierarchie, echte Serif *mit Grund*, asymmetrisches Raster,
  großzügiges Maß, Bild als Erzählung. Kippt in „random Serif = creative"-Tell → Serif rechtfertigen.
- **Minimalist / Notion-Linear** (V3-5 / M2-4 / D5-7): editorial-produktiv, zurückhaltende Palette, crispe Struktur,
  System-Sans ok. Kippt in „leer statt reduziert" → Detail-Präzision + echte Bilder.
- **Brutalist / Swiss-Industrial** (V7-10 / M3-6 / D4-7): harte mechanische Sprache, Swiss-Type, scharfer Kontrast,
  experimentelles Layout, Hard-Offset-Schatten *nur hier* erlaubt. Kippt in „Kostüm" → echte Grid-Strenge.
- **Dark-Tech** (V6-8 / M6-8 / D4-6): dunkle Basis, ein hochkontrastiger Akzent (NICHT Lila-Glow), präzise
  Micro-Motion, Mono für Daten. Kippt in „AI-Purple-Mesh-Hero"-Tell → Akzent aus der Marke, nicht aus dem Reflex.
- **Aurora / Kinetic** (V8-10 / M7-9 / D3-4): bewegter Gradient/Mesh *als Subjekt*, kinetische Typo, scroll-choreografiert.
  Nur ab MOTION>6 sinnvoll. Kippt in Effekt-ohne-Motiv → jeder Effekt in einem Satz begründbar.

Apple-„Liquid Glass" ist eine *Approximation* im Web (kein offizielles `liquid-glass.css`) — als solche labeln,
mit `prefers-reduced-transparency`-Fallback (Skeleton in `motion-craft/references/recipes.md`).

## 5. Anti-Repetition

Der tiefere Slop-Grund: ein LLM konvergiert über Sessions zu *einem* Attraktor. Gegenmittel:
- Nicht zweimal in Folge dieselbe Palette-Familie (bes. die Premium-Consumer-Warm-Palette, → `craft-floor.md §2`).
- Nicht dieselbe Serif über aufeinanderfolgende Projekte.
- Layout-Familien innerhalb einer Seite nicht wiederholen (→ `craft-floor.md §4`).
- Voll wirksam nur mit echtem Cross-Session-Gedächtnis — bei Verdacht den User fragen „letztes Projekt: welche Welt/Palette?".

---
*Adaption (Prosa) aus Leonxlnx/taste-skill (MIT, Dials + Welten). Siehe `../CREDITS.md`.*
