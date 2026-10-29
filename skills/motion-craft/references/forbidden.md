# Forbidden — Never-Ship-Motion (Selbstkontrolle vor „fertig")

> Jede Zeile ist ein automatischer Block in `design-review`. Der Detektor `design-craft/scripts/design_lint.py`
> fängt die maschinell zählbaren (mit `[det]` markiert).

| Nie | Stattdessen |
|---|---|
| `transition: all` `[det]` | Die exakten Properties benennen |
| `transform: scale(0)`-Entrance `[det]` | `scale(0.95)` + `opacity: 0` |
| `ease-in` auf UI-Element `[det]` | `ease-out` oder starke Custom-Kurve |
| Built-in `ease-out` auf deliberater Animation | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Animation auf Keyboard-Shortcut / 100+/Tag-Aktion | Keine Animation |
| UI-Dauer >300ms ohne Grund | 150-250ms |
| `transform-origin: center` auf trigger-geankertem Popover | `var(--transform-origin)` (Modals ausgenommen) |
| Keyframes auf Toasts/Toggles/schnell-triggerbarem | CSS-Transitions (retargeten vom aktuellen Wert) |
| `width/height/margin/padding/top/left` animieren | `transform` / `opacity` |
| Motion `x`/`y`/`scale`-Props unter Last | Voller `transform`-String |
| Ungegatetes `:hover`-Motion `[det]` | `@media (hover: hover) and (pointer: fine)` |
| Fehlendes `prefers-reduced-motion` | Sanftere Variante, nicht null |
| Alles gleichzeitig rein | 30-80ms Stagger |
| **`window.addEventListener('scroll')`** `[det]` | Scroll-driven CSS / Motion `useScroll` / GSAP ScrollTrigger |
| **`window.scrollY` in Framework-State** `[det]` | Motion `useMotionValue`/`useTransform`/`useScroll` |
| `requestAnimationFrame`-Loop, der Framework-State setzt | Motion-Values (laufen außerhalb des Render-Zyklus) |
| `useState` für kontinuierliche Werte (Scroll/Drag/Maus) | `useMotionValue` / `useTransform` |
| GSAP/Three.js **und** Motion im selben Component-Tree | Eine Engine pro Tree (sie kämpfen um dieselben Frames) |
| Marquee mehr als 1× pro Seite | Max eine, oder das Muster streichen |
| Identische Entrance-Animation auf jeder Sektion | Ein authored Moment (→ `craft-floor.md §5`) |

**Motion-Motiv-Gate:** Jede Animation in einem Satz begründbar (Hierarchie/Feedback/State/Storytelling). „Sah cool aus" = streichen oder Dial auf 3 senken. „Motion behauptet = Motion gezeigt" (kein toter MOTION-Dial).

**Perf-Guardrails:** nur transform/opacity animieren; `will-change` sparsam; Grain-Filter nur auf fixed `pointer-events:none`-Pseudo-Elementen; Ziele LCP<2.5s / INP<200ms / CLS<0.1.

---
*Adaption (Prosa) aus emil (MIT, „Never Ship") + taste-skill (MIT, Forbidden Animation Patterns). Siehe `../CREDITS.md`.*
