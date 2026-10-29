# Recipes — copy-paste Skeletons in zwei Tracks

> **Track zuerst wählen** (siehe `design-craft` SKILL.md):
> **Projekt** = Build vorhanden → Motion (`motion/react`) / GSAP erlaubt.
> **Artifact/Single-File** = strikte CSP, kein Build, keine externen Libs → nur Vanilla-CSS + WAAPI + `@starting-style`.
> Alle Werte stammen aus `motion-tables.md` — nicht approximieren.

## TOC
- A. Scroll-Reveal (Stagger) — der leichte Default
- B. Sticky-Scroll-Stack (Pin/Scrub) — schweres Geschütz
- C. Horizontal-Pan (Scroll-Hijack)
- D. Entrance on-mount
- E. Toast (interruptible)
- F. „Liquid Glass"-Approximation (mit Fallback)

---

## A. Scroll-Reveal (Stagger)
Der leichte Default. GSAP für echte Pin/Scrub-Arbeit aufsparen (B/C).

**Projekt (Motion):**
```jsx
import { motion } from "motion/react";
export function Reveal({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, transform: "translateY(16px)" }}
      whileInView={{ opacity: 1, transform: "translateY(0px)" }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >{children}</motion.div>
  );
}
```

**Artifact (CSS scroll-driven, kein JS):**
```css
@media (prefers-reduced-motion: no-preference) {
  .reveal { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 30%; }
  @keyframes reveal { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
}
```
Fallback für ältere Engines: `IntersectionObserver` → Klasse setzen, CSS-`transition` macht den Rest (kein Scroll-Listener).

## B. Sticky-Scroll-Stack (Pin/Scrub) — nur Projekt-Track
```jsx
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap"; import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
export function StickyStack({ cards }) {
  const root = useRef(null);
  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const els = gsap.utils.toArray(".card");
      els.forEach((card, i) => {
        ScrollTrigger.create({ trigger: card, start: "top top", pin: true, pinSpacing: false });
        if (els[i+1]) gsap.to(card, {
          scale: 0.92, opacity: 0.6, ease: "none",
          scrollTrigger: { trigger: els[i+1], start: "top bottom", end: "top top", scrub: true },
        });
      });
    }, root);
    return () => ctx.revert();          // Pflicht-Cleanup
  }, []);
  return <div ref={root}>{cards.map((c,i)=><section className="card" key={i}>{c}</section>)}</div>;
}
```
Artifact-Track: Pin/Scrub ohne Lib ist fragil — stattdessen `position: sticky` + scroll-driven CSS (`animation-timeline: view()`) verwenden, oder das Muster weglassen.

## C. Horizontal-Pan — nur Projekt-Track
Pin-Wrapper, inneren Track um `scrollWidth - innerWidth` translaten, `scrub: 1`, `invalidateOnRefresh: true`.
```jsx
gsap.to(track, {
  x: () => -(track.scrollWidth - root.clientWidth),
  ease: "none",
  scrollTrigger: { trigger: root, pin: true, scrub: 1, end: () => "+=" + track.scrollWidth, invalidateOnRefresh: true },
});
```

## D. Entrance on-mount
**Artifact/CSS (kein JS-State):**
```css
.pop { transition: opacity .2s var(--ease-out), transform .2s var(--ease-out); }
@starting-style { .pop { opacity: 0; transform: scale(.96); } }
```
**Projekt (WAAPI, framework-agnostisch):**
```js
el.animate([{ opacity:0, transform:"scale(.96)" }, { opacity:1, transform:"scale(1)" }],
  { duration:200, easing:"cubic-bezier(0.23,1,0.32,1)", fill:"both" });
```

## E. Toast (interruptible) — Transition, nicht Keyframe
```css
.toast { transform: translateY(100%); opacity: 0; transition: transform .22s var(--ease-out), opacity .22s var(--ease-out); }
.toast[data-open="true"] { transform: translateY(0); opacity: 1; }  /* retargetet vom aktuellen Wert bei schnellem Re-Trigger */
```
Exit wie Enter (nach unten). Bei echter Toast-Komponente im Projekt-Track lieber Sonner o.ä. nehmen als hand-rollen.

## F. „Liquid Glass"-Approximation (labeln als Web-Approx)
```css
.glass { background: color-mix(in oklab, canvas 70%, transparent); backdrop-filter: blur(12px) saturate(140%);
  border: 1px solid color-mix(in oklab, canvastext 12%, transparent); }
@media (prefers-reduced-transparency: reduce) { .glass { backdrop-filter: none; background: Canvas; } }
```
Glass nur als *spezifischer* Effekt, nicht als Deko-Default (→ `craft-floor.md §2`).

---
*Adaption (Prosa) aus taste-skill (MIT, GSAP/Motion-Skeletons) + emil (MIT, WAAPI/CSS-Reflexe). Siehe `../CREDITS.md`.*
