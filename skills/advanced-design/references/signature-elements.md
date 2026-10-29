# Signature-Elemente — unsere Wiedererkennungs-Rezepte („der Hammer")

Diese vier Elemente sind das visuelle Marken-Kapital. Jedes hier mit *echtem* Rezept aus dem
Produktiv-Code, damit es reproduzierbar + weiterentwickelbar ist. Quelle in Klammern.

---

## 1. Das 3D-Auge (refraktiv, blickfolgend) — der stärkste Eindruck
*(Quelle: eine eigene Three.js-Komponente aus einem privaten Produktions-Repo, nicht Teil dieses Skills)*

**Was es so überzeugend macht:** Es ist KEIN transparentes Bild — es ist **echte Lichtbrechung**. Eine
refraktive Cornea aus `MeshPhysicalMaterial` biegt das Licht dahinter (wie reales Auge/Glas), darunter
eine selbstleuchtende Iris aus einem **GLSL-Shader**, obendrauf additive Catchlights = „nasser" Blick.

**Aufbau (3 Schichten + Maske + Catchlights):**
```
world (Group, uniformer Zoom scale 0.9)
└─ oval (Group, NICHT-uniform gestaucht → runde Kugel wird Oval)
   ├─ sclera : SphereGeometry(1,64,64) + MeshPhysicalMaterial{clearcoat:0.2, clearcoatRoughness:0.45, envMapIntensity:0.4}
   ├─ iris   : CircleGeometry(0.52,96) + ShaderMaterial(IRIS_FRAG)   // selbstleuchtend, z=1.08
   ├─ cornea : SphereGeometry(1.3, …, 0..PI*0.22) Kappe + MeshPhysicalMaterial (siehe unten)  // z-Kappe
   └─ socket : PlaneGeometry + SOCKET_FRAG (Lid-/Höhlenschatten, depthTest:false, renderOrder 20)
+ 2× Catchlight-Quads (CATCH_FRAG, AdditiveBlending, depthTest:false)
```

**Das Glas-Rezept (Cornea) — HIER steckt der „Wow":**
```js
new THREE.MeshPhysicalMaterial({
  transmission: 1.0,      // 1 = voll lichtdurchlässig MIT Brechung (nicht nur opacity!)
  thickness: 0.6,         // "Dicke" des Glases → wie stark gebrochen wird
  ior: 1.376,             // Brechungsindex (echtes Auge ≈ 1.376; Fensterglas 1.5)
  roughness: 0.035,       // fast spiegelglatt
  clearcoat: 1.0, clearcoatRoughness: 0.05,  // zweite Klarlack-Schicht = "nasser" Glanz
  envMapIntensity: 1.6,   // Reflexionen aus der Env-Map (PMREM) — PFLICHT, sonst wirkt Glas tot
  transparent: true, color: 0xffffff,
})
```
★ `transmission` + `ior` = echtes Glas. `opacity`/`transparent` allein ist Fake. Transmission braucht
zwingend eine **Env-Map** (`scene.environment = pmrem.fromScene(...)`), sonst spiegelt sich nichts.

**Die Iris (GLSL-Fragment-Shader, selbstleuchtend):** prozedurale Fasern über `fbm`-Noise, ein **7×7
Pixel-Veil** (die Iris wird in Zellen quantisiert = das Anonymisierungs-/Pixel-Motiv), Pupille mit
`uDil`-Dilatation, Limbus-Rand, dezente Iridescence an den Faserkanten. Selbstleuchtend (kein Licht
nötig), damit sie durch die Cornea *glüht*. Uniforms: `uTime`, `uDil`, `uGaze`, Akzentfarben.

**Blickfolge (Gaze):** Iris+Cornea in einer Group; Mausposition → `uGaze`/Group-Rotation (gedämpft).
Pupille pulsiert, im Leerlauf driftet der Blick = „lebendig ohne Kamera". Blink über `uBlink`.

**Render:** `WebGLRenderer{alpha:true, antialias:true}`, `outputColorSpace=SRGB`,
`toneMapping=ACESFilmicToneMapping`, `exposure=1.15`. (Für Neubauten: AgX statt ACES erwägen, danach nachsättigen.)

**Pflicht-Robustheit:** dynamic `import('three')` → eigener Lazy-Chunk (nicht im App-Budget); `destroy()`
baut rAF/Listener/Geometrien/Material + GL-Kontext restlos ab (`forceContextLoss`) BEVOR andere WebGL-
Kontexte starten; bei fehlendem WebGL / reduced-motion / Chunk-Fehler → **statisches SVG-Brandmark**.

**Varianten-Idee:** dasselbe Schema, andere Iris-Textur (Shader-Uniform) = beliebige „sprechende"
Signatur-Orbs; Catchlight-Position = Lichtstimmung.

---

## 2. Fadenkreuz-/Personen-Intro — die Produkt-Demo, die „klickt"
*(Quelle: eigene Produktions-Skripte `build_video.py` + `make_figures.py`, nicht Teil dieses Skills)*

Das ist eine **2D-SVG-Frame-Animation** (kein 3D), rsvg→ffmpeg — aber durch Timing + Fadenkreuz +
Zustands-Morphing wirkt sie hochwertig und erzählt sofort.

**Personen-Figuren (`make_figures.py`):** reine SVG, Paletten `SKIN/HAIR/CLOTH`, `figure(cx,cy,R,state,…)`
mit **vier Zuständen**, zwischen denen weich übergeblendet wird (Crossfade `xf≈0.38s`):
```
sharp   → Gesicht klar sichtbar
track   → Tracking-Rahmen/Marker erscheint
mosaic  → Gesicht VERPIXELT (das Produkt-Versprechen, als Mosaik-Kacheln)
named   → eine Person wird benannt ("Anna") & bleibt sichtbar
```
★ Die ganze Story steckt im Zustands-Morph: `sharp → track → mosaic` zeigt „erkannt → verpixelt" ohne ein Wort.

**Das Fadenkreuz (`reticle`)** — der Enterprise-Reiz:
- fährt per Easing über eine Keyframe-Bahn (`crosshair_pos(t)`: von Person zu Person, zurück zu einer),
- Farbe interpoliert **steel → grün beim LOCK** (`mix(ACC_L, GREEN, …)`),
- beim Lock: zusätzlicher **rotierender gestrichelter Ring** (`stroke-dasharray="10 8"` + `rotate(t*90)`),
- Label wechselt `SCAN` → `LOCK`.

**Radar/Grid-Hintergrund (`radar`):** Raster aus Linien + Kreuzungs-Punkten + ein **Sweep** (vertikaler
Gradient-Balken, der einmal durchläuft) = „Scanner"-Gefühl. Füllt den „leeren" Raum mit Dichte.

**Brand-Lockup + Captions:** Logo+Wordmark oben; untertitel-artige Captions blenden pro Beat ein/aus
(`ease` in/out, kleiner `dy`-Versatz von unten) mit nummerierten Step-Chips (`1 · VERPIXELN` …).

**Intro/Outro:** Logo + kreisender Draw-In-Ring (`stroke-dashoffset`-Animation), Outro mit expandierenden
grünen Ringen + Häkchen (Check-Pfad per `stroke-dashoffset`) + CTA.

**Für LUSTIGE/animierte Clips (dein späteres Ziel):** dieses SVG-Frame-Prinzip skaliert für simple
Figuren. Für *charaktergetriebene, humorvolle* Qualität → Upgrade auf **Rive** (Figur mit State-Machine:
idle/reagiert/spricht, Bones) eingebettet in **Remotion** (rendert nach MP4 ProRes/4K). Siehe
`recipes-graphics-video.md`.

---

## 3. Agenten-Konstellation — unser abstraktes KI-Signet
*(Quelle: eigene `createHeroCore`-Komponente [echt-3D] · eigene SVG-Generator-Skripte, nicht Teil dieses Skills)*

Ein **Metall-Kern** (Ikosaeder bzw. Hex-Ring) + **Orbit-Knoten** auf einer Kugel (Fibonacci-Verteilung)
+ glühende Verbindungen (additiv) + **wandernde Daten-Pulse** (kleine Kugel + Glow-Halo, `lerp` entlang
der Kante) + langsame Rotation. Steht für „Agenten-Orchestrierung".
- **Track A (echt 3D):** `IcosahedronGeometry` metal + `WireframeGeometry`-Hülle (additiv) + `OctahedronGeometry`-Satelliten; Env-Map für Glanz; rAF-Rotation.
- **Track B/C (SVG):** gezeichnete Knoten/Linien/Polygone, Rotation via `transform="rotate()"`, Pulse via `lerp`.

Verwendung: Hero-Centerpiece, Banner-Akzent rechts, Intro-Kern. Nie mit Text überladen — Lesbarkeit first.

---

## 4. Glas-Browser-Rahmen + echter 3D-Tilt — der „Enterprise-Showcase"-Rahmen
*(Quelle: eigene SVG-/CSS-Generator-Skripte, nicht Teil dieses Skills)*

Ein macOS-artiges Fenster (Chrome-Leiste: 3 Dots + URL-Pille + Status-Badge), gerundeter Korpus, weicher
Schlagschatten → rahmt jede Bühne „wie ein Produkt".
- **Track A (CSS, interaktiv):** `perspective:1700px` auf dem Eltern-Element, Kind `transform:rotateX(2.5deg) rotateY(-3deg)` (Ruhe-Neigung) + `@keyframes livetilt` (fortlaufend sanft) + WAAPI-Reveal (`scale .92→1`, `cubic-bezier(.16,1,.3,1)`). Glas via `backdrop-filter:blur(18px) saturate(1.2)` + Metall-Kante (`inset 0 0 0 1px rgba(255,255,255,.09)`) + Sheen (`inset 0 1px 0 rgba(255,255,255,.16)`) + Float-Schatten.
- **Track B/C (SVG→PNG/Video):** rsvg kann KEINE Perspektive → Rahmen flach rendern, dann **ffmpeg `perspective`-Filter** kippt das fertige Bild (`perspective=x0=…:sense=destination`). Das ist der Trick für den „schrägen" Look in Standbild/Video.

★ Ruhe-Neigung klein halten (2–3°). Großer Tilt wirkt wie Gimmick; kleiner wirkt teuer.
