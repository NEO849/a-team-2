# Recipes — Track B (Standbild) & Track C (Video)

## TRACK B — Standbild (Banner, Social-Grafik, Poster)
**Pipeline:** Python schreibt SVG → `rsvg-convert -w W -h H in.svg -o out.png`. Vektor = scharf in jeder Größe,
Tiefe wird *gemalt* (Verläufe/Schatten), nicht berechnet. Reproduzierbar, versionierbar.
*(Produktiv-Vorbild: eigenes `brand_graphics.py`, nicht Teil dieses Skills)*

Rezept pro Asset: `DEFS` (Verläufe: Platin-Text, Metall-Panel, Glow; Filter: Drop-Shadow, Grain via
`feTurbulence`) → `bg` (Graphit-Radial + 32px-Raster + Grain-Overlay) → Konstellation/Signatur → Wordmark
(Platin `fill="url(#plat)"`) → Chips/Panels (Metall + Sheen-Linie) → Footer. Dann rsvg bei EXAKTEN Maßen.

**Plattform-Maße (merken):** YouTube-Banner 2560×1440 (Safe-Area-Mitte 1546×423!), X-Header 1500×500,
LinkedIn-Cover 1584×396, Facebook-Cover 1640×624, GitHub-Social 1280×640, IG-Post 1080×1350/1080×1080, Story 1080×1920.
Wichtige Inhalte in die Safe-Area; Deko darf bluten.

**Tiefe ohne 3D:** linear/radial-Verläufe (hell→dunkel = Volumen), Sheen-Linie oben (`inset`-Lichtkante
als dünne `<path>`-Linie weiß 12 %), Drop-Shadow-Filter, Grain-Overlay (`feTurbulence`, opacity ~0.035) = Material.

**Cache-Busting:** wenn gleichnamige PNGs ersetzt werden, im HTML `?v=<ts>` anhängen (Browser cacht sonst Alte).

## TRACK C — Video

### C1 · Unser Weg (SVG-Frames → ffmpeg) — solide, maximale Kontrolle
*(Produktiv-Vorbild: eigenes `brand_video.py`, nicht Teil dieses Skills)*
1. Pro Frame ein SVG `frame_svg(cfg, t)` mit Easing (`ease=smoothstep`, `lerp`, `mix`) → `rsvg-convert` → PNG (ThreadPool).
2. `ffmpeg -framerate 30 -i f%04d.png -c:v libx264 -pix_fmt yuv420p silent.mp4`
3. **Glas-Rahmen + echter Tilt:** Rahmen-SVG (`frame_shell`) als PNG; Animation in den Viewport **overlayen**, dann das Ganze mit dem **`perspective`-Filter** kippen (rsvg kann keine Perspektive):
   ```
   [1:v]scale=VW:VH[v];[0:v][v]overlay=VX:VY:shortest=1[c];
   [c]perspective=x0=..:y0=..:x1=..:y1=..:x2=..:y2=..:x3=..:y3=..:sense=destination[o]
   ```
4. **Musik:** `loudnorm=I=-16:TP=-1.5:LRA=11` (Broadcast-Lautheit) + `afade` in/out. Synth-Bett = lizenzsicher als Platzhalter; echter Track lizenzrein (Pixabay/Epidemic — `research-music.md`).
5. **Poster:** `ffmpeg -ss <t> -i wrapped.mp4 -frames:v 1 poster.png` → als `<video poster="…">`.
Gut für: abstrakte Marken-Intros, Scanner-/Fadenkreuz-Demos, Daten-Visuals. Grenze: echte Charaktere/Humor.

### C2 · SOTA für hochwertige & LUSTIGE Charakter-Clips → Remotion + Rive
*(Recherche-Empfehlung, Belege in `tech-matrix.md`)*
- **Remotion** = React → MP4/Video. Backbone: deterministisch, CI-renderbar, **ProRes 4444/hq, 4K,
  Farbräume bt601/709/2020, Alpha, HW-Encoding**. Komposition in React-Komponenten, Zeit = `useCurrentFrame()`.
- **Rive** = interaktive Charakter-Animation mit **State Machines** (idle → reagiert → spricht …) + Bones/Mesh.
  60fps, ~30–50KB, deutlich effizienter als Lottie. KEIN direkter Video-Export → als `.riv`-Runtime **in
  Remotion einbetten** und dort zu MP4 rendern = Best-of-both (Charakter-Interaktivität + Pro-Render).
- **Lottie/dotLottie** = nur Vektor-Microanimation (AE→bodymovin); harte Grenzen (keine Expressions/Blur/Effects). Als Asset in Remotion nutzbar.
- **Motion Canvas** = TS-Generator für erklärende Shape/Diagramm-Clips (Code-first, präzise Timing).

**Enterprise-Produktions-Pfad für animierte/lustige Clips (empfohlen):**
1. Figur/Charakter in **Rive** (State-Machine: idle/talk/react; Bones). 2. Szene/Komposition in **Remotion**
(React): Rive-Figur + unsere Machined-Graphite-Welt + Text/Captions + Musik. 3. Render `--codec=prores
--prores-profile=hq` (Schnitt) bzw. H.264 4K (Social). 4. QC über ein 9-Checks-Gate (Frames ansehen).

**Harte Gates Video:** **Remotion-Company-Lizenz vor kommerzieller Nutzung prüfen.** Musik lizenzrein.
KI-Inhalte kennzeichnen (EU-AI-Act). Frames IMMER selbst ansehen (nie nur „QC_PASS" glauben).
> Unsicherheit: „Claude Motion" (Anthropic, code→MP4) laut Recherche real seit Okt 2026 (Team/Enterprise-Beta) —
> aber Wissensstand endet Jan 2026; VERIFIZIEREN, ob Zugang/Feature besteht, bevor darauf gebaut wird.

## Entscheidungs-Kürzel
- Banner/Still → **Track B** (SVG→rsvg).
- Abstraktes Marken-Intro/Scanner/Daten → **Track C1** (SVG→ffmpeg, schnell, voll kontrolliert).
- Charakter/erzählend/lustig/höchste Qualität → **Track C2** (Remotion + Rive).
- Interaktiv/im Browser erlebbar → **Track A** (Three.js, kein Video).
