# Recipes — Web-Motion (Scroll, Zoom, Parallax, ruhig-teure Choreografie)

Immer durch das `motion-craft`-Gate (soll es überhaupt animieren → Zweck → billigstes Tool → nur
transform/opacity → Easing/Spring → Interruption → reduced-motion). Hier die konkreten Werkzeuge/Rezepte.

## Tool-Wahl (billigstes zuerst)
1. **CSS Transition / `@starting-style`** — Enter/Hover/State. Null Abhängigkeit.
2. **CSS Scroll-Driven Animations** (`animation-timeline: scroll()` / `view()`) — Reveals, Parallax, Progress, Zoom-on-scroll. Läuft auf dem Compositor (flüssig), 0 JS. ~84% Support (mid-2026) → `@supports (animation-timeline: view())` Fallback.
3. **WAAPI** (`element.animate([...], {...})`) — imperativ, CSP-sicher (unser Reveal/Live-Tilt nutzt das).
4. **GSAP** — für Scroll-*Choreografie* (Pin + Scrub + Timeline), SplitText-Reveals, Flip-Szenenwechsel.
5. **Motion (motion.dev)** — React-Komponenten-Motion mit Spring-Physik + Choreografie.

## Scroll-Zoom / Pin / Reveal
**Einfach, CSS-nativ (bevorzugt):**
```css
@keyframes zoomIn { from { transform: scale(.9); opacity:0 } to { transform:none; opacity:1 } }
.hero { animation: zoomIn linear both; animation-timeline: view(); animation-range: entry 0% cover 40%; }
@supports not (animation-timeline: view()) { .hero { opacity:1 } }  /* Fallback: sichtbar */
```
**Komplex (Pin + Scrub + Kamera-ähnlicher Zoom) → GSAP ScrollTrigger:**
```js
gsap.registerPlugin(ScrollTrigger);
gsap.timeline({ scrollTrigger: { trigger:'.stage', start:'top top', end:'+=1500',
  pin:true, scrub:1 } })
  .to('.scene', { scale:1.4, ease:'none' })      // "rein-zoomen" beim Scrollen
  .to('.layer-bg', { yPercent:-20, ease:'none' }, 0);  // Parallax-Ebene, parallel
```
GSAP ist seit 2025 komplett gratis (inkl. ScrollTrigger/SplitText/Flip/MotionPath).

## Kinoreife Text-Reveals
GSAP **SplitText** (Zeilen/Wörter/Zeichen splitten) + `stagger`:
```js
const s = new SplitText('.title', { type:'chars' });
gsap.from(s.chars, { yPercent:120, opacity:0, duration:.6, ease:'power3.out', stagger:0.02 });
```

## „Ruhig, teuer" — Spring statt Bounce
Motion-Springs mit **`bounce: 0` oder negativ** (überdämpft) = kein Nachwippen = Enterprise-Ton.
```jsx
<motion.div animate={{ y:0, opacity:1 }} transition={{ type:'spring', bounce:0, duration:0.5 }} />
```
Dauern: UI-Mikro 100–300ms, größere Übergänge bis ~400ms. **`ease-out`** für Enter; `ease-in` auf UI meiden. Ab ~500ms wirkt es träge.

## Choreografie (mehrere Elemente)
Motion `variants` + `staggerChildren`; GSAP-Timeline mit Positions-Parametern (`"<"`, `"-=0.2"`).
Prinzip: nicht alles gleichzeitig — gestaffelt = „durchdacht", gleichzeitig = „billig".

## Smooth-Scroll-Fundament
**Lenis** (~3KB) unter GSAP/Motion legen (sanftes Scrollen, synchronisiert mit ScrollTrigger). reduced-motion-safe konfigurieren.

## Zustands-/Seitenwechsel
**View Transitions API** (`document.startViewTransition(() => updateDOM())`) + `@starting-style` → native, flüssige Übergänge, progressive enhancement (cross-doc Chrome/Safari 18.2+; Firefox teils offen).

## Maus-Parallax (unser Hub-Rezept)
JS rechnet Winkel → CSS-Variablen; CSS dreht (GPU). Begrenzen (±~7°), damit Text lesbar bleibt:
```js
el.onmousemove = e => { const r=el.getBoundingClientRect();
  el.style.setProperty('--ry', ((e.clientX-r.left)/r.width-.5)*7 +'deg');
  el.style.setProperty('--rx', (-((e.clientY-r.top)/r.height-.5)*7)+'deg'); };
```
```css
.card{ transform: rotateX(var(--rx,0)) rotateY(var(--ry,0)); transition: transform .2s } /* Eltern: perspective */
```

## Hard-Gates Motion
- **`prefers-reduced-motion: reduce` IMMER mitshippen** — Animationen aus, Endzustand sofort. Scroll-Jacking/Parallax löst bei ~35% der Empfindlichen (40+) Schwindel aus.
- Nur transform/opacity animieren (GPU; kein Layout-Thrash). Kein `scale(0)`. `transform-origin` am Trigger.
- Vor „fertig": `motion-craft/forbidden.md`-Selbstkontrolle + `design-review`.
> Unsicherheit: Support-%/Breaking-Changes (Motion 14.x) vor Festlegung gegen caniuse/Changelog prüfen.
