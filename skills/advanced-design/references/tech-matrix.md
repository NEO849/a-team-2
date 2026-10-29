# Technologie-Matrix — SOTA-Recherche (verdichtet)

> Quelle: drei parallele Web-Recherchen (2026-10-11). VOLLE Quelllinks + Belege in den Dossiers:
> `orchestration/research-3d-web.md` · `research-motion.md` · `research-claude-motion.md`.
> Confidence pro Block angegeben; Zahlen aus Sekundärquellen sind markiert — vor Festlegung gegenprüfen.

## A · Echtzeit-3D-Web (Confidence ~80 %)
Gerankt nach Look-Hebel:
1. **IBL/Env-Map via PMREM** (`scene.environment`, drei `<Environment>`): größter Hebel — eine gute Env, alle PBR-Materialien wirken teuer.
2. **Echtes Glas:** drei `MeshTransmissionMaterial` bzw. `MeshPhysicalMaterial` (`transmission`+`ior`+`thickness`+`clearcoat`); Env-Map Pflicht. Metall: `metalness:1` + niedrige `roughness` + IBL.
3. **Film-Look:** **AgX**-Tonemapping (neutraler als ACES, danach nachsättigen) + Post: **Bloom + DepthOfField + N8AO**.
4. **Kamera:** `MathUtils.damp()` statt `lerp`; **Dolly=Zoom (Position)**, FOV nur für Vertigo; drei `CameraControls`/`fitToBox`.
5. **Theatre.js** für choreografierte Kamerafahrten / Scroll-Flythroughs (visueller Keyframe-Editor).
6. **WebGPURenderer + TSL** — ein Shader-Graph, WebGL-Fallback; prod-tauglich ab r171 (stable später). REIF für Langzeit.
7. **GPU-Compute-Partikel (TSL)** — 1M+ Partikel GPU-seitig für Hero-Effekte.
8. **Instancing/BatchedMesh** (Perf-Pflicht, 1 Draw-Call/10k) · **Gaussian Splatting** (three r186 + Spark) für gescannte Fotorealistik.
RAND DER REIFE (auf Zielgerät testen): SSGI/SSR (0beqz realism-effects v2 WIP, nicht sauber in @react-three/postprocessing).
⚠ Versionsnummern (r171/r186) + Support-% aus Sekundärquellen — gegen offizielles three-Changelog/caniuse prüfen.

## B · Web-Motion (Confidence ~86 %)
1. **GSAP** — seit April 2025 **komplett gratis** (ScrollTrigger/SplitText/Flip/MotionPath). Arbeitspferd für Pin+Scrub+Zoom, Text-Reveals, Szenenwechsel. Browser-identisch.
2. **CSS Scroll-Driven Animations** (`animation-timeline: scroll()/view()`) — 0 JS, Compositor, ~84 % Support mid-2026, `@supports`-Fallback.
3. **Motion (motion.dev)** — Spring-Physik; **`bounce ≤ 0` = ruhig/teuer**; `variants`/`staggerChildren`-Choreografie. (Nachfolger/Rebrand von Framer Motion, framework-agnostisch.)
4. **Lenis** (~3KB) — Smooth-Scroll-Fundament unter GSAP/Motion, reduced-motion-safe.
5. **View Transitions API + `@starting-style`** — native Zustands-/Routenwechsel (cross-doc Chrome/Safari 18.2+; Firefox teils offen).
Dauern: UI 100–400ms, `ease-out` auf Enter, ab ~500ms träge. **`prefers-reduced-motion` PFLICHT** (Scroll-Jacking/Parallax → Schwindel bei ~35 % der 40+).
⚠ Support-% / Motion-14-Breaking-Changes vor Festlegung gegen caniuse/Changelog prüfen.

## C · Claude-Design/-Motion + Code-Video (Confidence A~90 % · B~85 %)
**WIDERSPRUCH offen halten:** 
- Track-3-Recherche: „**Claude Motion**" + „**Claude Design**" sind **echte Anthropic-Produkte** (Launch 8. Okt 2026; Claude Motion = Text/Charts/Shapes → animiertes MP4, **code-getrieben, kein Diffusionsmodell**, `/motion`, Beta Team/Enterprise). Brand: dark #141413/light #faf9f5, Akzente Orange/Blue/Green, Poppins+Lora.
- Track-2-Recherche: „Claude motion" = **motion.dev** (keine Anthropic-Produkt-Zuordnung).
→ Beide mit Quellen; mein Wissensstand endet Jan 2026 → **VERIFIZIEREN** vor jeder Abhängigkeit. Wichtig: die Code→Video-Philosophie (kein Video-Modell) **bestätigt unseren Ansatz** unabhängig vom Namen.

**Code-Video-Pipelines (SOTA-Ranking für hochwertige/lustige Charakter-Clips):**
1. **Remotion** (React→MP4) — Backbone: ProRes 4444/hq, 4K, bt601/709/2020, Alpha, HW-Encoding, deterministisch, CI. ⚠ Company-Lizenz vor kommerziell.
2. **Rive** — Charaktere + State-Machines + Bones (60fps, ~30–50KB, effizienter als Lottie); kein Video-Export → **in Remotion einbetten**.
3. **Lottie/dotLottie** — nur Vektor-Micro (keine Expressions/Effects/Blur).
4. **Motion Canvas** — TS-Generator für erklärende Shape/Diagramm-Clips.
5. **SVG+ffmpeg** (unser Weg) — max. Kontrolle, Fallback, nicht Spitze für Charaktere.
FAZIT: **Remotion (Backbone) + Rive (Charaktere)** = Enterprise-Pfad für animierte, auch humorvolle Clips.
⚠ Download-/CPU-Zahlen indikativ (Sekundärquellen); Remotion-Lizenz + Claude-Motion-Zugang offen.

## Adoptions-Empfehlung (für uns, priorisiert)
- **Sofort/günstig:** AgX+Bloom/DoF/N8AO auf die bestehenden Three.js-Szenen; `damp()`-Kamera; GSAP ScrollTrigger für Scroll-Zoom im Hub; Lenis.
- **Mittelfristig:** `MeshTransmissionMaterial`-Glas-Akzente; CameraControls/Theatre.js für Blickwinkel-Fahrten; CSS-SDA-Reveals.
- **Für Charakter-/lustige Videos:** PoC **Rive-Figur in Remotion** (1 Baseline-Clip ProRes hq 4K bt709), DANN Entscheidung SVG+ffmpeg→Remotion (Blast-Radius via strategie-analyst prüfen).
- **Langfrist:** WebGPU+TSL-Migration planen (Fallback behalten).
