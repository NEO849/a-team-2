# `video_move` — Referenz: Shot-Grammar & KI-Video-Kamera-Regie (2026)

Faktisch, quellenbasiert. Modelle: Higgsfield (Camera-Control-Layer), Sora 2, Kling 3.0, Veo 3.1, Seedance 2.0. Kernregel über allem: **ein Kamera-Move pro Clip**, kurz und konkret statt Wall-of-Text.

---

## 1. Das 8-Layer Shot-Grammar-Framework

Baue jeden Prompt aus 8 Schichten. Reihenfolge zählt — Modelle gewichten frühe Tokens stärker, deshalb Subject/Action zuerst, Continuity zuletzt. Trenne Kamera immer sichtbar vom Rest (eigener Block/Label), damit Spatial-Anweisungen nicht in die Motiv-Beschreibung „bluten".

| # | Layer | Was reingehört | Ausgefüllte Beispiel-Zeile |
|---|-------|----------------|----------------------------|
| 1 | **Subject & Action** | Wer + konkretes, physik-plausibles Verhalten. Starke, spezifische Verben. | `Ein Dabbawala radelt durch monsun-nasse Gassen, weißer Kittel, tiefe Wasserpfützen spritzen auf` |
| 2 | **Emotion / Performance** | Ziel-Ausdruck, Mikro-Mimik, Energie. | `Micro-expressions von Erleichterung, ruhiger fokussierter Blick, leichtes Lächeln im Augenwinkel` |
| 3 | **Optics / Lens** | Brennweite, Blende, DoF, Focus-Rack. | `35 mm anamorphotisch, flache Schärfentiefe (T2.0), Bokeh-Highlights, langsamer Focus-Pull vom Vorder- auf Hintergrund` |
| 4 | **Motion / Camera** | EIN Kamera-Move + Subject-Blocking. Richtung explizit. | `langsamer Dolly-in mit Parallax, Motiv bleibt zentriert` |
| 5 | **Lighting** | Key/Fill/Rim, Farbtemperatur (Kelvin), Volumetrik. Verhältnisse statt „hell". | `Natrium-Dampf-Rimlight, weicher Key 5600 K, Fill 3200 K, leichter Dunst/Volumetrik im Gegenlicht` |
| 6 | **Style / Color Science** | Film-Stock, LUT, Genre-Look. | `Dokumentar-Realismus, Kodak-2383-Print-Look, dezente Halation, filmisches Korn` |
| 7 | **Audio** | Ambient-Bett, Foley, Dialog (in Anführungszeichen), SFX auf Beats. | `Ambient: Regen + ferner Verkehr. SFX: Fahrradklingel. Foley: quietschende Kette` |
| 8 | **Continuity** | Gelockte Wardrobe/Props/Tageszeit, exakte Descriptor-Tokens für Wiederverwendung über Clips. | `Wardrobe gelockt: weiße Gandhi-Topi + Nehru-Jacke; Blue-Hour; gleiche Narbe über linker Augenbraue` |

### Kompletter Beispiel-Prompt — cinematic Establishing Shot

```
[SUBJECT/ACTION] Ein einzelner Dabbawala radelt bei Blue Hour durch monsun-
nasse Gassen von Mumbai, Wasser spritzt unter den Reifen auf.
[EMOTION] ruhig, fokussiert, Micro-expression stiller Erleichterung.
[LENS] 35 mm anamorphotisch, flache Schärfentiefe, weiche Bokeh-Highlights.
[CAMERA] EIN Move: langsamer Dolly-in mit Parallax, Motiv bleibt zentriert.
[LIGHTING] Natrium-Dampf-Rimlight + weicher Key 5600 K, Fill 3200 K, volumetrischer Dunst.
[STYLE] Dokumentar-Realismus, filmischer Print-Look, dezente Halation, feines Korn.
[AUDIO] Ambient: leichter Regen + ferner Verkehr. SFX: Fahrradklingel. Foley: Kette.
[CONTINUITY] Wardrobe gelockt: weiße Gandhi-Topi + Nehru-Jacke, Blue Hour konstant.
```

---

## 2. Higgsfield Kamera-Preset-Katalog

Higgsfield ist kein Generator, sondern eine **Camera-Control-Schicht** über WAN/Veo/Sora — Stärke = deterministische, benannte Kamerafahrten. 50+ Presets. **Regel: genau ein Move pro Clip.** Kurze, einfache Motion rendert sauberer als Multi-Move-Sequenzen. Input-Bild-Logik: für **Orbit/Dolly/Zoom → zentriertes Motiv** ins Keyframe; für Raum-Moves → weites/szenisches Bild; für Push-in-Emotion → Close-up-Gesicht.

| Preset(s) | Dramaturgisch gut für | Passendes Input-Bild |
|-----------|----------------------|----------------------|
| **Crash Zoom In / Out** | Schock, Betonung, Meme-Beat, plötzliche Enthüllung | Zentriertes Motiv, klarer Fokuspunkt |
| **Rapid Zoom In/Out, YoYo Zoom** | Energie, Comedy-Timing, Hooks für Social | Zentriertes Motiv |
| **Dolly In / Out, Super Dolly** | Emotionale Annäherung/Distanzierung, ruhiges Establishing | Zentriertes Motiv, mittlere Distanz |
| **Dolly Zoom In/Out (Vertigo)** | Unbehagen, Realitätsbruch, psychologische Spannung | Zentriertes Motiv vor tiefem Hintergrund |
| **Dolly Left/Right, Double Dolly** | Laterale Enthüllung, Parallax, Character-Reveal | Motiv mit Raum seitlich |
| **Pan Left/Right, Tilt Up/Down** | Umgebung offenbaren, Größe/Höhe zeigen | Weites/szenisches Bild |
| **Whip Pan** | Harter Cut/Transition zwischen Szenen | Zwei Motive / Übergangspunkt |
| **Crane Up/Down, Jib Up/Down, Crane Over The Head** | Establishing, Abschieds-/Ankunfts-Gefühl, Epik | Weites Bild, Motiv im unteren Drittel |
| **Aerial Pullback** | Kontext-Reveal, „Held im Universum", Schluss-Beat | Motiv zentriert in weiter Landschaft |
| **360 Orbit / Lazy Susan / 3D Rotation** | Produkt-Hero, Character-Showcase, „Held-Moment" | Streng zentriertes Motiv/Objekt |
| **Arc Left/Right** | Dynamische Umkreisung mit Vorwärtsdrang | Zentriertes Motiv |
| **FPV Drone** | Immersive Speed, durch enge Räume fliegen, Action | Weites/szenisches Bild mit Tiefenpfad |
| **Handheld** | Doku-Realismus, Tension, Nähe, „echt" | Close-up / Medium |
| **Snorricam** | Desorientierung, subjektiver Rausch (Kamera am Körper fixiert) | Close-up Gesicht, Motiv zentral |
| **Dutch Angle** | Unruhe, Bedrohung, Stilbruch | Beliebig, Motiv zentriert |
| **Fisheye** | Skate/Street-Ästhetik, Verzerrung, Nähe-Übertreibung | Zentriertes Nah-Motiv |
| **Bullet Time** | Eingefrorene Zeit, surreal, Action-Peak | Zentriertes Motiv, freier Raum ringsum |
| **Object POV / Through Object In/Out** | Kreative Transition, POV-Immersion | Objekt im Vordergrund als „Tor" |
| **Car Chasing, Car Grip, Road Rush, Buckle Up** | Automotive-Action, Verfolgung, Speed | Fahrzeug / Straßen-Szene |
| **Head Tracking, Hero Cam, Robo Arm** | Tech/Beauty-Reels, präzises Verfolgen | Zentriertes Gesicht/Objekt |
| **Overhead / Object POV** | Flat-Lay, Food, Tutorials, Ordnungs-Look | Top-down-fähiges Motiv |
| **Hyperlapse, Timelapse (Landscape/Human/Glam)** | Zeit-Kompression, Transformation, Establishing | Statisches weites Bild |
| **Low Shutter, Wiggle, Focus Change** | Stil-Akzent, Motion-Blur-Vibe, Aufmerksamkeits-Lenkung | Je nach Effekt |
| **Static / General** | Dialog, Talking-Head, ruhiger Anker-Shot | Beliebig, sauber komponiert |
| **Mouth In / Eyes In / Eating Zoom** | Extreme Close-up-Beats, ASMR/Food-Hooks | Close-up Gesicht/Mund |

Higgsfield-Prompt-Struktur (3-Layer-System, „ein Scene = drei Jobs"): **Keyframe-Layer** (Framing/Lens/Licht/Umgebung locken — „das erste Frame steuert alles danach") → **Identity-Layer** (Gesicht/Alter/Kostüm) → **Video-Layer** (Motion/Acting/EIN Kamera-Move). Clip-Länge typ. **3–5 s**.

---

## 3. Per-Modell Prompt-Tuning-Matrix

| Modell | Stärke | Schwäche | Ideale Clip-Länge | Prompt-Tuning | Wann wählen |
|--------|--------|----------|-------------------|---------------|-------------|
| **Higgsfield** (Control-Layer) | Deterministische, benannte Kamerafahrten; VFX-Presets; Reframe über Aspect-Ratios | Selbst kein Generator — Output-Qualität hängt am Backbone (WAN/Veo/Sora); komplexe Multi-Moves brechen | 3–5 s | Keyframe locken, dann GENAU ein Preset + eine Subject-Action + starkes Verb; zentriertes Motiv für Orbit/Dolly/Zoom | **Motion/Kamera-Kontrolle** — wenn der exakte Kamera-Move das Erzählmittel ist |
| **Sora 2** (OpenAI) | Beste **Physik/Weight/Momentum**; starke Character-Consistency über Cuts; native Audio; lange Clips | Teuer, langsamere Iteration; API-Zugang restriktiv; Lip-Sync < Seedance | bis ~15 s (teils 25 s zitiert) | Reihenfolge **Subject → Action → Camera → Environment → Lighting → Mood → Style**; Prosa, nicht JSON; Dialog kurz (3–5 s/Zeile) in Anführungszeichen | **Physics & Storytelling** — Flüssigkeiten, Stoff, Kollisionen, längere kohärente Szenen |
| **Kling 3.0** (Kuaishou) | Bestes Preis/Leistung; **Character-driven Storytelling**; 4K/60fps → sehr natürlicher Lip-Sync | **Folgt Kamera-Prompts schwach** (ignoriert komplexe Moves); nur ~10 s max | ≤ 10 s | Professional-Mode-Slider nutzen (H/V/Zoom **1–3** für smooth); Kamera simpel halten; gegen Blur „crisp motion" + Motion-Brush runter | **Character-Consistency / Volumen-Prototyping** bei knappem Budget; nicht für anspruchsvolle Kamerafahrten |
| **Veo 3.1** (Google) | Broadcast-ready Color-Science; **beste natürliche Audio** (getimte Ambient/SFX); Fast-Tier top Preis/Qualität | Nur ~8 s max → mehr Generierungen/Schnitt; teurer als Kling teils | ~8 s | **JSON-Prompting** — Felder: `shot{type,lens,framing,movement}`, `subject`, `action`, `scene`, `lighting`, `style`, `audio{dialogue,sfx,ambient}`, `color_palette`, `negative_prompt`. Verhindert Concept-Bleed. Dialog `"..."`, `SFX:`, `Ambient noise:` trennen | **Multi-Shot-Präzision & Audio** — wenn Farbtreue, sauberer Ton und exakte Feld-Kontrolle zählen |
| **Seedance 2.0** (ByteDance) | Multimodale Inputs (Bild/Video/Audio/Text); **@-Referenz-System** für Kompositions-Kontrolle; unified Audio-Video-Joint-Gen (bester Lip-Sync); günstigster Scale-Preis | Steilere Lernkurve (Multimodal-Workflow) statt simplem Text | bis ~12 s (1.5 Pro) | @-Referenzen für Charaktere/Assets setzen; Audio als Input beilegen für Sync; Kompositions-Anker statt reiner Prosa | **Referenz-getriebene Konsistenz & Remix** — Template-Arbeit, Volumen, exakte Asset-Wiederverwendung |

Höchste-Hebel-Gewohnheit 2026: **Prompt pro Modell standardisieren**, nicht einen Prompt copy-pasten. JSON für Veo, Prosa für Sora, Slider für Kling, @-Refs für Seedance, Preset für Higgsfield.

---

## 4. 10 Copy-Paste Prompt-Templates

Platzhalter in `{...}`. Immer nur **ein** Kamera-Move pro Template.

**1 — Establishing Shot**
```
{Subjekt} in {Ort} bei {Tageszeit}. {Weitwinkel/24mm}, tiefe Schärfe.
CAMERA: langsamer Crane-Up (ein Move), Motiv im unteren Drittel.
LIGHT: {Key-Kelvin} + volumetrischer Dunst. STYLE: {Film-Look}.
AUDIO: Ambient {Umgebung}. CONTINUITY: {gelockte Tageszeit/Wardrobe}.
```

**2 — Tracking Shot**
```
{Subjekt} bewegt sich {Richtung} durch {Umgebung}, {starkes Verb}.
50mm, mittlere Schärfentiefe. CAMERA: Dolly-Right parallel zum Motiv, konstanter Abstand.
LIGHT: {Rim + Key}. STYLE: {Look}. AUDIO: Foley {Schritte}, Ambient {Bett}.
```

**3 — Reaction Shot**
```
Close-up von {Person}, Micro-expression {Emotion}, {kleine Kopf-/Augenbewegung}.
85mm, sehr flache Schärfentiefe, Bokeh. CAMERA: Static (Talking-Head-Anker).
LIGHT: weicher Key 5600K, sanfter Fill. AUDIO: leises Ambient, kein Dialog.
```

**4 — Product Hero**
```
{Produkt} zentriert auf {Oberfläche/BG}, Reflexionen, saubere Kanten.
Makro, scharfer Fokus. CAMERA: 360 Orbit, Objekt bleibt zentriert.
LIGHT: Studio-Softbox, {Rim} für Kanten-Trennung. STYLE: hochglanz Werbe-Look. AUDIO: dezenter Whoosh-SFX.
```

**5 — Portrait Push-In**
```
{Person}, {Ausdruck/Emotion}, minimale Bewegung. 85mm, flache Schärfentiefe.
CAMERA: langsamer Dolly-In, Motiv zentriert, endet in Close-up.
LIGHT: {Key-Kelvin}, Rim für Kontur. STYLE: {Film-Stock}. CONTINUITY: {gelockte Merkmale}.
```

**6 — Transition (Clip → Clip)**
```
{Motiv A} im Vordergrund. CAMERA: Whip-Pan (oder Through-Object-In durch {Objekt}).
LIGHT: Motion-Blur beim Move. Endframe: sauber auf {Motiv B des nächsten Clips} matchen.
STYLE: {Look konstant zum Nachbar-Clip}. AUDIO: SFX Whoosh auf dem Beat.
```

**7 — POV**
```
First-Person-Sicht von {Handelnder}, {Aktion mit Händen/Blickrichtung}.
Weitwinkel, leichte Verzerrung. CAMERA: Handheld POV, natürliches Wackeln.
LIGHT: {motiviertes Licht}. AUDIO: Atem + Foley {Interaktion}. STYLE: immersiv, roh.
```

**8 — B-Roll / Detail**
```
Detail von {Objekt/Textur/Geste}, {kleine sichtbare Bewegung: Dampf steigt / Stoff weht}.
Makro/50mm, flache Schärfentiefe. CAMERA: langsamer Dolly-In (ein Move).
LIGHT: {weich, gerichtet}. STYLE: {Look}. AUDIO: leises Ambient/Foley.
```

**9 — Logo Reveal**
```
{Logo} erscheint aus {Partikel/Licht/Nebel} auf {BG}. Zentriert.
CAMERA: langsamer Dolly-Out (oder Crash-Zoom-Out) enthüllt volles Logo.
LIGHT: Rim + Glow um Logo, {Marken-Farbe}. STYLE: clean, {Marken-Ästhetik}. AUDIO: Riser + Impact-SFX am Reveal.
```

**10 — Talking-Head / Avatar**
```
{Avatar/Person} spricht in Kamera: "{kurze Zeile, 3–5 s}". Natürliche Mimik, Lip-Sync.
85mm, weicher Hintergrund. CAMERA: Static (leichter unmerklicher Drift ok).
LIGHT: 3-Punkt, weicher Key 5600K. AUDIO: Dialogue "{...}"; Ambient noise: {leise}. CONTINUITY: {gelockte Wardrobe/BG}.
```

---

## 5. Häufige Fehler & Fixes

| Fehler | Warum es bricht | Fix |
|--------|-----------------|-----|
| **Wall of Text** | Modell verliert Gewichtung; frühe Tokens dominieren, Rest verwässert | In 8 gelabelte Layer gliedern; Kamera in eigenen Block; kurz + konkret |
| **Zwei Kamera-Moves pro Clip** | Widersprüchliche Spatial-Direktiven → Warp/Ignorieren | GENAU ein Move pro Clip; zweiten Move als eigenen Clip mit Match-Cut |
| **Vage Motion** („bewegt sich", „hell") | Modell rät, Ergebnis flau/plastisch | Richtung + Verb spezifizieren („slow dolly-in", „180°-Arc"); Licht als Kelvin/Ratios, nicht „hell" |
| **Inkonsistenz über Clips** | Identity-/Wardrobe-Drift | Continuity-Layer: exakte Descriptor-Tokens wortgleich wiederverwenden (Narbe, Accessoire, Kelvin, Tageszeit); bei Higgsfield/Seedance Keyframe bzw. @-Referenz locken |
| **Concept-Bleed** (Mood färbt Objekt um) | Prosa vermischt Attribute | Bei Veo JSON-Felder trennen; sonst Motiv, Licht, Style in getrennte Blöcke |
| **Dialog desynct** | Zu lange Zeilen | Max 3–5 s/Zeile, in Anführungszeichen; `SFX:` und `Ambient noise:` separat halten |
| **Kamera-Move ignoriert (Kling)** | Kling folgt Text-Kamera schwach | Professional-Mode-Slider 1–3 nutzen ODER für den Move zu Higgsfield/Veo wechseln |
| **Off-center Motiv bei Orbit/Zoom** | Tracking verliert Zentrum → Wobble | Für Orbit/Dolly/Zoom zentriertes Motiv ins Input-Keyframe |

---

## Quellen

- Higgsfield Camera Controls (50+ Presets): https://higgsfield.ai/camera-controls
- Higgsfield WAN Camera Control Guide: https://higgsfield.ai/blog/WAN-AI-Camera-Control-Your-Guide-to-Cinematic-Motion
- Higgsfield Cinema Studio Prompt Guide (100+): https://higgsfield.ai/blog/cinema-studio-3.0
- Higgsfield Sora 2 Prompt Guide: https://higgsfield.ai/sora-2-prompt-guide
- Segmind — Higgsfield Prompt Format Guide: https://blog.segmind.com/higgsfield-ai-prompt-guide-video-creation/
- Kolbo.AI — Higgsfield 100+ Camera Presets: https://kolbo.ai/blog/higgsfield-suite-100-camera-presets
- TrueFan — Cinematic AI Video Prompts 2026: https://www.truefan.ai/blogs/cinematic-ai-video-prompts-2026
- MagicHour — Cinematic AI Video Prompt Cookbook 2026: https://magichour.ai/blog/cinematic-ai-video-prompt-cookbook
- Imagine.art — Veo 3.1 JSON Prompting Guide: https://www.imagine.art/blogs/veo-3-json-prompting-guide
- Kling AI — Prompt Guide: https://kling.ai/blog/kling-ai-prompt-guide
- WaveSpeed — Seedance 2.0 vs Kling 3.0 vs Sora 2 vs Veo 3.1: https://wavespeed.ai/blog/posts/seedance-2-0-vs-kling-3-0-sora-2-veo-3-1-video-generation-comparison-2026/
- AI/ML API — Best AI Video Generators 2026: https://aimlapi.com/blog/best-ai-video-generators-2026-veo-3-1-kling-sora-2-seedance-more-compared

> Hinweis: Modell-Specs (Clip-Längen, Preise, Sora-2-Verfügbarkeit) sind Momentaufnahme Mitte 2026 und ändern sich schnell — vor Einsatz gegen die aktuelle Anbieter-Seite re-verifizieren.
