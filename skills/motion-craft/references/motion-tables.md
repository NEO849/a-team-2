# Motion-Tables — die Entscheidungen in der richtigen Reihenfolge

> Reihenfolge ist Pflicht: Schritt 1-2 gaten alles. Nicht nach einer Kurve greifen, bevor klar ist,
> ob überhaupt animiert wird. Keine approximierten Werte — jede Kurve/Dauer/Spring kommt aus diesen Tabellen.

## 1. Sollte das überhaupt animieren?

| Frequenz | Entscheidung |
|---|---|
| 100+×/Tag (Keyboard-Shortcut, Command-Palette-Toggle) | **Nie animieren. Stop.** |
| Zehner/Tag (Hover, Listen-Navigation) | Nur near-imperceptible — schnell & subtil, oder nichts |
| Gelegentlich (Modals, Drawers, Toasts) | Standard-Animation |
| Selten / erstmalig (Onboarding, Success, Celebration) | Hier lebt das Delight-Budget |

**Keyboard-initiierte Aktion = Disqualifikator, kein Ermessen.** Raycast hat keine Open/Close-Animation — korrekt für etwas, das man hunderte Male/Tag öffnet. Scheitert die Anfrage am Gate: klar sagen, nicht bauen, Nicht-Motion-Alternative anbieten.

## 2. Was ist der Zweck? (in einem Wort benennen, sonst nicht bauen)
Feedback · Spatial-Consistency (woher/wohin) · State-Indication · Preventing-a-jarring-change · Explanation (nur Marketing/Onboarding) · Delight (nur im selten/erstmalig-Tier).
Zusatz-Check **Funktion:** Daten, die der User liest/bearbeitet, bewegen sich nicht für Stil. Deko-Maus-Tracking gehört auf eine Marketing-Seite, nicht auf einen Graph in einer Banking-App.

## 3. Tool wählen — das billigste, das funktioniert (runtergehen, beim ersten Treffer stoppen)

| Bedarf | Tool |
|---|---|
| Hover, Press, Farbe, Klassen-/Attribut-getriebener State-Toggle | **CSS transition** |
| Entry-Animation on-mount, kein JS-State | **CSS `@starting-style`** |
| Vorbestimmte Motion, die smooth bleibt während die Seite lädt | **CSS animation** (läuft off-main-thread) |
| Programmatische Kontrolle mit CSS-Performance, keine Lib | **WAAPI** (`element.animate()`) |
| Springs, Layout-Animation, Exit-Animation, gesten-getriebene Werte | **Motion** (`motion.dev`) |

CSS-Animation schlägt JS unter Last (off-main-thread, während rAF-basiertes Frames dropt). Braucht die Aufgabe eine *Komponente* (Toast/Drawer/Command-Menu/Dropdown) statt einer Animation → fertige, zugängliche Komponente nehmen, nicht hand-rollen.

## 4. Properties wählen
- **Nur `transform` und `opacity`** (überspringen Layout & Paint, laufen auf der GPU). `width/height/margin/padding/top/left` triggern alle drei. (`clip-path` ist die sanktionierte Vierte; `height` nur für Accordions toleriert.)
- **Nie `scale(0)`** — starte von `scale(0.9-0.97)` + `opacity: 0`. Nichts erscheint real aus dem Nichts.
- **`transform-origin` am Trigger** für Popover/Dropdown/Menu/Tooltip. **Modals ausgenommen** (nicht an einen Trigger geankert, bleiben zentriert).
- **Prozente in `translate()`** sind relativ zur Eigengröße (`translateY(100%)` = eigene Höhe) — vor Hardcode-Pixel bevorzugen.
- **In Motion den vollen Transform-String** (`transform: "translateX(100px)"`), nicht `x`/`y`/`scale`-Shorthands (nicht HW-beschleunigt, droppen unter Last).
- **Nie den Transform eines Kindes aus einer CSS-Variable am Parent treiben** (recalc für jedes Kind).

## 5. Easing & Dauer — oder ein Spring

**Easing** (Entscheidungsreihenfolge):

| Situation | Easing |
|---|---|
| Enter/Exit | `ease-out` |
| Auf dem Screen bewegen/morphen | `ease-in-out` |
| Hover/Farbwechsel | `ease` |
| Konstante Motion (Marquee, Progress) | `linear` |
| Default | `ease-out` |

**Nie `ease-in` auf UI** (startet langsam, verzögert genau den beobachteten Moment). Built-in-CSS-Easings sind zu schwach — diese nutzen:
```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* starkes ease-out für UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* starkes ease-in-out für On-Screen-Bewegung */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-artige Drawer-Kurve */
```
Braucht es eine andere Kurve → von easing.dev/easings.co nehmen, nicht hand-rollen.

**Dauer:**

| Element | Dauer |
|---|---|
| Button-Press-Feedback | 100-160ms |
| Tooltips, kleine Popovers | 125-200ms |
| Dropdowns, Selects | 150-250ms |
| Modals, Drawers | 200-500ms |
| Marketing/Explanatory | Kann länger |

**UI-Animation bleibt unter 300ms.** 180ms-Dropdown fühlt sich responsiver an als 400ms.

**Stattdessen Spring** bei Drag-mit-Momentum, „lebendigem" Element, unterbrechbarer/umkehrbarer Geste, Deko-Maus-Tracking:
```js
{ type: "spring", duration: 0.5, bounce: 0.2 }            // Apple-Stil, leichter zu reasonen
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // klassische Physik, mehr Kontrolle
```
Bounce 0.1-0.3, in den meisten UIs Bounce meiden (nur Drag-to-dismiss/playful).

## 6. Interruption & Exit
- **Transitions, keine Keyframes** für schnell-triggerbares (Toasts/Toggles): Transitions retargeten vom aktuellen Wert, Keyframes starten bei null.
- **Springs für Gesten** (tragen Velocity durch die Unterbrechung).
- **Exit wie Enter** — ein Toast, der von unten reinslidet, geht nach unten raus.
- **Asymmetrisches Timing wo der User entscheidet** — langsam in der deliberaten Phase, snappy in der System-Antwort.

## 7. Reduced-Motion & Pointer-Gating (shippt mit der Animation, jedes Mal)
```css
@media (prefers-reduced-motion: reduce) { .el { animation: fade 0.2s ease; } } /* opacity/color behalten, transform-Motion raus */
@media (hover: hover) and (pointer: fine) { .el:hover { transform: scale(1.05); } } /* Touch feuert False-Hovers */
```
Reduced-Motion heißt *weniger & sanfter*, nicht null — Transitions, die Verständnis helfen, behalten; Bewegung/Positionswechsel raus.

---
*Adaption (Prosa) aus emilkowalski/skills (MIT, `animate`). Siehe `../CREDITS.md`.*
