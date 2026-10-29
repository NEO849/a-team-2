# Design-System „Machined Graphite" + Skill-Dirigat + Produktiv-Dateien

## Token-System (EINE Quelle der Wahrheit)
Dunkel, metallisch, EIN zurückhaltender Steel-Akzent, kein Emoji. Tiefe durch Layering (Verläufe + Grain +
Schatten + Kanten), nicht durch Buntheit. Tokens als CSS-Variablen / SVG-`defs` / Three-Konstanten:
```
Farben     bg #090b0e · bg2 #06070a · text #eef1f4 · muted rgba(255,255,255,.56) · faint .34
Akzent     steel #5f9bb0  (hell #8fbecd · glow #bfe3ef) — NUR dieser eine Akzent
Metall     panel linear(#2a2e34→#15181c) · text-platin linear(#fff→#cdd2d9 55%→#a6adb7)
Kanten     edge  inset 0 0 0 1px rgba(255,255,255,.09)   (feine Metall-Lichtkante)
           sheen inset 0 1px 0 rgba(255,255,255,.16)     (Glanzlicht oben)
Schatten   float 0 24px 60px rgba(0,0,0,.5) · float2 0 40px 110px rgba(0,0,0,.62)
Glas       backdrop-filter: blur(18px) saturate(1.2)  +  edge + sheen + float
Raster     32–34px, rgba(255,255,255,.04–.05), per radial-mask zum Rand ausblendend
Grain      feTurbulence fractalNoise baseFreq 0.8, opacity ~0.035 (Material/Tiefe)
Radius     r 16 · r-lg 20 · chip 7–8
Motion     ease cubic-bezier(.16,1,.3,1) (Reveal) · UI 100–300ms ease-out · Spring bounce≤0
Tilt       Ruhe rotateX(2.5deg) rotateY(-3deg), perspective 1400–1700px
```
**Anthropic-Brand (falls Claude-/Anthropic-Kontext gefragt):** dark #141413 / light #faf9f5; Akzente Orange
#d97757 · Blue #6a9bcc · Green #788c5d; Typo Poppins (Headings) + Lora (Body). *(Nicht mit Machined-Graphite mischen — bewusst wählen.)*

## Signatur-Pflicht
Jedes Hero-Visual trägt mindestens EIN Signatur-Element (`signature-elements.md`): 3D-Auge · Konstellation ·
Fadenkreuz-Intro · Glas-Browser-Rahmen. Das ist Wiedererkennung, nicht Deko.

## Skill-Dirigat (welcher Skill wofür)
| Phase | Lead | Ergänzend |
|---|---|---|
| Welt/Ästhetik/Tokens | `design-craft` | `design-intel` (Paletten/Fonts/Motion-Presets abfragbar), `apple-design` (Material/Physik) |
| Web-Motion | `motion-craft` | `emil-design-eng` (Detail-Politur), `animate` (Entscheidungs-Reihenfolge), `animation-vocabulary` |
| Motion-Audit | `find-animation-opportunities` | `improve-animations` |
| Diagramme/Daten | `diagram-design` | `dataviz` |
| Video | `remotion-video` (deterministisch) | ein Regie+QC-Gate, `video-move` (generativ) |
| claude.ai-Artifact | `artifact-design` (CSP: keine externen Libs/Fonts!) | — |
| HÄRTEN | `design-review` | ein adversarial reviewer, `slop-check` (Text), `humanize` (Copy) |
Regel: nicht alles selbst — den passenden Skill laden, Entscheidung begründen, bauen, härten.

## Produktiv-Dateien (Prinzip: an bestehenden Generatoren anknüpfen, nicht neu erfinden)
Wenn du bereits eigene Generator-Skripte für Hub/Grafiken/Video hast (Three.js-Hub, SVG→PNG-Grafik-Pipeline,
SVG-Frames→ffmpeg-Video), knüpfe an diese an statt sie neu zu bauen. Die konkreten Datei- und Serverpfade
sind projektspezifisch und gehören in dein eigenes Projekt-Memory, nicht in diesen Skill.

## Live-Verify (Pflicht)
Track A/B über die Chrome-Bridge rendern + Screenshot ANSEHEN (bei WebGL `preserveDrawingBuffer:true`;
Full-Page-Shots zeigen Off-Screen-WebGL/Lazy-Images evtl. leer → in den Viewport scrollen). Track C: Frames ansehen.
Bewegung/Feel beurteilt der Mensch am echten Gerät — ehrlich benennen, was ein Standbild nicht zeigt.
