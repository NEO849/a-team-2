---
name: advanced-design
description: >-
  Enterprise-Höchststufe für 3D-Optik, Motion, Grafik & Video — baut die beeindruckendsten,
  fortgeschrittensten visuellen Ergebnisse auf „maximal beeindruckend": echtes WebGL-3D (Glas/Metall,
  refraktive Materialien), kinoreife Kamera (Zoom/Dolly/Blickwinkel), Scroll- und Maus-Parallax,
  isometrischer Tilt, animierte Marken-Clips in Bildbearbeitungs-Qualität. Synthetisiert SOTA
  (Three.js/WebGPU-TSL, GSAP, Motion.dev, Remotion+Rive) mit unseren Signature-Rezepten (3D-Auge,
  Fadenkreuz-/Personen-Intro, Glas-Browser-Rahmen + Perspektiv-Tilt, Agenten-Konstellation) und
  dirigiert unsere Design/Motion-Skills (design-craft, motion-craft, apple-design, emil-design-eng,
  remotion-video, diagram-design …). Nutze, wenn ein visuelles Ergebnis AUSSERGEWÖHNLICH
  sein soll — Hero-Visual, 3D-Showcase, Marken-Intro, animierter (auch lustiger) Clip, Banner-Set.
  Trigger "/advanced-design", "advanced design <x>", "beeindruckendstes <3d/motion/video/banner>",
  "enterprise 3d <x>", "3d glas <x>", "mach das zum hammer <x>", "animiertes video enterprise <x>".
---

# advanced-design — die beeindruckendsten visuellen Ergebnisse, reproduzierbar

> Rolle: **Senior Creative-Technologist + 3D-Design-Engineer + Brand-Art-Director** (Award-Niveau).
> Messlatte: über einem polierten Marketing-Site-Benchmark. Ergebnisse sind *echt 3D wo es zählt*, *ruhig-teuer* in der
> Motion, *reproduzierbar* aus Code — nie zusammengeklickt. Entscheidung treffen, Grund in einer Zeile,
> bauen, adversarial härten, LIVE verifizieren. Kein Options-Buffet, kein Slop, kein Emoji.

## Die Kern-Einsicht (zuerst lesen)
Derselbe „3D-Glas"-Look wird je nach Medium mit VÖLLIG anderer Maschinerie gebaut. Erst den **Track** wählen:

| Track | Wann | Echtes 3D? | Maschinerie |
|---|---|---|---|
| **A · Realtime-Web** | Hub/Landing/Showcase, interaktiv | ja (WebGL) + CSS-Fake | Three.js/WebGPU + CSS + GSAP/Motion |
| **B · Standbild** | Banner, Social-Grafik, Poster | nein — Tiefen-Illusion | SVG → `rsvg-convert` → PNG |
| **C · Video** | Intro, Reel, erklärender/lustiger Clip | eingebacken bzw. React-3D | SVG→ffmpeg (einfach) **oder** Remotion (+Rive) für Spitze |

★ Echtes interaktives 3D (Maus dreht Objekte, Kamerafahrten) geht nur in Track A (WebGL). In B/C wird der 3D-Eindruck vorberechnet/flach eingebacken.

## Ablauf (Reihenfolge ist die halbe Miete)
1. **Design-Read + Track** (ein Satz, sichtbar): Was wird gebaut, für wen, welcher Track, welche Signatur.
2. **Ästhetik committen** über `design-craft` (Welt + Dials + Token-System). Default-Welt hier = **Machined Graphite** (siehe `references/design-system.md`). Kein Emoji, EIN Steel-Akzent, Tiefe durch Layering.
3. **Signatur wählen** (`references/signature-elements.md`): 3D-Auge · Agenten-Konstellation · Fadenkreuz-/Personen-Intro · Glas-Browser-Rahmen. Diese sind unser Wiedererkennungs-Kapital.
4. **Bauen** mit den Track-Rezepten:
   - Track A → `references/recipes-3d.md` + `references/recipes-motion.md`
   - Track B → `references/recipes-graphics-video.md` (§ Standbild)
   - Track C → `references/recipes-graphics-video.md` (§ Video; Spitze = Remotion+Rive)
5. **Motion-Disziplin** immer über `motion-craft` (7-Schritt-Gate: soll es überhaupt animieren → Zweck → billigstes Tool → nur transform/opacity → Easing/Spring → Interruption → reduced-motion).
6. **HÄRTEN (Pflicht, nicht optional):** `design-review` (adversariale visuelle Kritik + Batched-Screenshot-Verify) + ein adversarial reviewer für Behauptungen.
7. **LIVE verifizieren:** über die Chrome-Bridge rendern + Screenshot ansehen (Track A), bei WebGL `preserveDrawingBuffer:true` für Screenshots; bei Video Frames ansehen (nie nur „fertig" glauben). Bewegung/Feel beurteilt der User am echten Gerät — ehrlich sagen, was ein Standbild nicht zeigt.

## Technologie-Matrix (SOTA, recherchiert — Belege in `references/tech-matrix.md`)
- **3D-Look:** IBL/Env-Map via PMREM = größter Hebel · `MeshPhysicalMaterial`/drei `MeshTransmissionMaterial` (`transmission`+`ior`+`thickness`+`clearcoat`) = *echtes* Glas · `metalness:1` + niedrige `roughness` + IBL = Metall · **AgX**-Tonemapping (neutraler als ACES, danach nachsättigen) + Post (Bloom + DoF + N8AO) = Film-Look.
- **Kamera/Zoom/Blickwinkel:** `MathUtils.damp()` statt `lerp` (weich, interruptible) · **Dolly = Position** (sauberer Zoom), **FOV nur für Vertigo** · drei `CameraControls`/`fitToBox` · `Theatre.js` für choreografierte Fahrten.
- **Motion:** **GSAP** (seit 2025 gratis — ScrollTrigger Pin/Scrub/Zoom, SplitText-Reveals, Flip-Szenenwechsel) · CSS Scroll-Driven (`animation-timeline: scroll()/view()`, 0 JS) · **Motion (motion.dev)** Springs mit `bounce ≤ 0` = ruhig/teuer · **Lenis** Smooth-Scroll · View Transitions + `@starting-style`.
- **Zukunft (reif genug):** **WebGPURenderer + TSL** (ein Shader, WebGL-Fallback, r171+) · GPU-Compute-Partikel · Gaussian Splatting (r186 + Spark) für gescannte Fotorealistik.
- **Video-Spitze:** **Remotion** (React→MP4, ProRes 4444/4K, deterministisch, CI) als Backbone + **Rive** (interaktive Charaktere, State-Machines, Bones) eingebettet — der Pfad für hochwertige, auch *lustige* Charakter-Clips. Lottie nur für Vektor-Micro. Unser SVG→ffmpeg = solider Fallback.

## Unsere Skills kombinieren (Dirigat — nicht alles selbst)
| Aufgabe | Lead-Skill | + ergänzend |
|---|---|---|
| Ästhetik/Welt/Tokens | `design-craft` | `design-intel` (Paletten/Fonts), `apple-design` (Physik/Material) |
| Web-Motion/Micro-Interaction | `motion-craft` | `emil-design-eng` (Politur), `animate` (Entscheidungs-Reihenfolge) |
| Animations-Audit/Lücken | `find-animation-opportunities` | `improve-animations`, `animation-vocabulary` (Begriff finden) |
| Diagramme/Daten | `diagram-design`, `dataviz` | — |
| Deterministisches Video | `remotion-video` | ein Regie/QC-Gate, `video-move` (generativ) |
| Härten vor Auslieferung | `design-review` | ein adversarial reviewer, `slop-check` (Text) |
Für claude.ai-Artifacts gilt `artifact-design` (CSP: keine externen Libs/Fonts/CDN) — dann nur Vanilla-CSS+WAAPI+inline-SVG.

## Hard-Gates (Abschluss — ohne diese kein „fertig")
- **reduced-motion Pflicht** (`prefers-reduced-motion`): Parallax/Scroll-Jacking löst bei ~1/3 der Empfindlichen Schwindel aus → Bewegung abschaltbar, Inhalt ohne JS/WebGL voll sichtbar (Progressive Enhancement).
- **WebGL sauber:** Teardown (`dispose`/`forceContextLoss`), Off-Screen-Pause (IntersectionObserver), Draw-Call-Budget < 100 mobile (Instancing), SVG/PNG-Fallback bei fehlendem WebGL.
- **Lizenzen prüfen vor kommerziell:** Remotion-Company-Lizenz, GSAP-Business-Plugins-Status, Musik (lizenzrein — Research-music.md), Env-/HDRI-Lizenz.
- **Enterprise-Ton:** kein Emoji, EIN Akzent, Zurückhaltung; AgX nachsättigen statt übertreiben.
- **LIVE verifiziert, nicht behauptet** (Screenshot/Frames angesehen); ehrlich, was Standbild/Feel nicht zeigt.

## Referenzen (Tiefe)
- `references/signature-elements.md` — **3D-Auge · Fadenkreuz-/Personen-Intro · Agenten-Konstellation · Glas-Browser-Rahmen** (die „Hammer"-Rezepte, mit Code).
- `references/recipes-3d.md` — Three.js/WebGPU: Glas, Metall, IBL, Kamera/Zoom, Post, Tilt, Parallax, Perf.
- `references/recipes-motion.md` — GSAP/CSS-SDA/Motion/Lenis/View-Transitions, ruhig-teure Choreografie.
- `references/recipes-graphics-video.md` — SVG→rsvg→ffmpeg-Pipeline (Standbild + Video + Perspektiv-Tilt + Musik) UND der Remotion+Rive-Upgrade-Pfad für Charakter-/lustige Clips.
- `references/design-system.md` — Machined-Graphite-Tokens + Skill-Kombinations-Logik + Dateipfade unserer bestehenden Generatoren.
- `references/tech-matrix.md` — die volle SOTA-Recherche mit Quelllinks + Reife/Unsicherheiten (3 Research-Dossiers verdichtet).
