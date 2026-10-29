# `video_move` — Pipeline: Prompt → fertiger geschnittener Clip

**Zielsystem:** Linux-VPS, **CPU-only**, ffmpeg + Kokoro TTS lokal. Kein Vendor-Lock-in.

**Leitprinzip (ehrlich):** Die *Generierung* bewegter Bilder ist auf CPU-only nicht realistisch —
läuft **zwingend in der Cloud** (Higgsfield/fal.ai/Replicate). Alles ab dem generierten Clip
(Schnitt, Ton, Mix, Untertitel, Farb-/Loudness-Angleich, Export) läuft **lokal, deterministisch,
gratis** mit ffmpeg. Der Skill ist ein **Thin-Cloud-Head + Fat-Local-Post** — spart Credits, hält Kontrolle.

---

## 1. Multi-Vendor-API-Abstraktion

Alle drei Provider folgen demselben Lebenszyklus **submit → poll → download**. Nur Auth, Payload-Keys
und Statusklassen unterscheiden sich → gekapselt in `scripts/video_gen.py` (Strategy-Pattern).
Der Skill kennt nur `get_provider(name).generate(GenSpec, dest)`.

| Provider | Install | Auth (env) | Submit | Poll | Download |
|---|---|---|---|---|---|
| **Higgsfield** | `pip install higgsfield-client` | `HF_KEY="key:secret"` (oder `HF_API_KEY`+`HF_API_SECRET`) | `higgsfield_client.submit(model, arguments=…)` | `ctrl.poll_request_status()` → `Queued/InProgress/Completed/Failed/NSFW/Cancelled` | `ctrl.get()[…]["url"]` |
| **fal.ai** | `pip install fal-client` | `FAL_KEY="…"` | `fal_client.submit(model, arguments=…)` → `.request_id` | `fal_client.status(model, id)` / `.result(model, id)` | `result["video"]["url"]` |
| **Replicate** | `pip install replicate` | `REPLICATE_API_TOKEN="…"` | `replicate.predictions.create(version=…, input=…)` | `pred.wait()` → `pred.status` | `pred.output` (Liste/FileOutput) |

**Provider-Tausch = eine Zeile:**
```python
from video_gen import get_provider, GenSpec, generate_cached
from pathlib import Path
prov = get_provider("fal")          # oder env VIDEO_PROVIDER=higgsfield|replicate
generate_cached(prov, GenSpec(prompt="drone over foggy pine forest, cinematic",
                              resolution="720p", aspect_ratio="16:9"), Path("cache"))
```

**Modell-IDs:** Die exakten `arguments`-Keys (`image_url` vs. `start_image`, `duration` int vs. str)
variieren pro Endpoint → in `_submit` gekapselt, via `GenSpec.extra` überschreibbar. Bei neuem Modell
einmal das JSON-Schema der Modell-Seite (fal/Replicate zeigen es) prüfen — **nicht raten**.

---

## 2. Lokale Post-Production-Pipeline (CPU-only, ffmpeg)

Alle Befehle laufen auf CPU (x264 + Audio/Filter = CPU-Standard, kein GPU nötig).

### 2.1 Clips hart aneinanderhängen (gleiches Format)
```bash
printf "file '%s'\n" shots/shot_*.mp4 > renders/concat_list.txt
ffmpeg -f concat -safe 0 -i renders/concat_list.txt -c copy renders/rough.mp4
```
`-c copy` = verlustfrei/schnell, nur bei identischem Codec/Auflösung/FPS. Bei Mismatch → normalisieren (2.8) oder `xfade`.

### 2.2 Crossfade (xfade, Video + Audio)
`offset` = (Dauer Clip A) − (Fade-Dauer). Zwei 5-s-Clips, 1 s Blende → offset 4:
```bash
ffmpeg -i shots/shot_01.mp4 -i shots/shot_02.mp4 -filter_complex \
"[0:v][1:v]xfade=transition=fade:duration=1:offset=4,format=yuv420p[v]; \
 [0:a][1:a]acrossfade=d=1[a]" -map "[v]" -map "[a]" renders/xfade_pair.mp4
```
Weitere: `wipeleft`, `slideup`, `circleopen`, `dissolve`, `radial`. Für N Clips die xfades verketten (fortlaufende offsets aus `ffprobe`-Dauern).

### 2.3 Voiceover (Kokoro) untermischen
```bash
# VO dominant, Originalton weg:
ffmpeg -i renders/rough.mp4 -i audio/voiceover.wav \
-c:v copy -map 0:v:0 -map 1:a:0 -shortest renders/with_vo.mp4
# VO + Ambient (20%) behalten:
ffmpeg -i renders/rough.mp4 -i audio/voiceover.wav -filter_complex \
"[0:a]volume=0.2[amb];[amb][1:a]amix=inputs=2:duration=longest:dropout_transition=0[a]" \
-map 0:v -map "[a]" -c:v copy renders/with_vo.mp4
```

### 2.4 Musik mit Ducking (sidechaincompress) — der Profi-Look
Musik wird leiser sobald die Stimme spricht; VO ist der Sidechain-Trigger:
```bash
ffmpeg -i renders/rough.mp4 -i audio/music.mp3 -i audio/voiceover.wav -filter_complex \
"[1:a]volume=0.8[music]; \
 [music][2:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[ducked]; \
 [ducked][2:a]amix=inputs=2:duration=longest:normalize=0[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k renders/with_music.mp4
```
Höheres `ratio` / niedrigerer `threshold` = stärkeres Ducking; `release` = wie schnell Musik danach hochkommt.

### 2.5 Untertitel / Text-Overlay
```bash
# Burned-in aus .srt:
ffmpeg -i renders/with_music.mp4 -vf \
"subtitles=audio/vo.srt:force_style='FontName=DejaVu Sans,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,MarginV=40'" \
-c:a copy renders/subbed.mp4
# Freies Text-Overlay (nur Sek. 0–3):
ffmpeg -i in.mp4 -vf \
"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='Kapitel 1':\
fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=12:x=(w-text_w)/2:y=h-120:\
enable='between(t,0,3)'" -c:a copy out.mp4
```

### 2.6 Farbangleichung
```bash
ffmpeg -i in.mp4 -vf "eq=contrast=1.05:saturation=1.1:brightness=0.02:gamma=0.98" -c:a copy out.mp4   # global
ffmpeg -i in.mp4 -vf "colorbalance=rm=0.05:gm=0:bm=-0.05,eq=saturation=1.08" -c:a copy out.mp4          # Weißabgleich
ffmpeg -i in.mp4 -vf "lut3d=luts/teal_orange.cube" -c:a copy out.mp4                                    # LUT-Look
```
Grenze: echtes *automatisches* Shot-Matching (Histogramm-Angleich) braucht ein Python/OpenCV-Script (CPU-fine) — bei Bedarf als optionale Stufe.

### 2.7 Loudness-Normalisierung (loudnorm, EBU R128, 2-Pass) — Pflicht vor Auslieferung
Ziel **−14 LUFS** (YouTube/Social).
```bash
# Pass 1 messen:
ffmpeg -i renders/final_mix.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null -
# Pass 2 anwenden (measured_* aus Pass-1-JSON einsetzen):
ffmpeg -i renders/final_mix.mp4 -af \
"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-19.3:measured_TP=-3.1:measured_LRA=7.4:\
measured_thresh=-30.1:offset=-0.2:linear=true:print_format=summary" \
-c:v copy -c:a aac -b:a 192k renders/final_loud.mp4
```

### 2.8 Export-Presets
```bash
# Social 9:16 (Reels/Shorts/TikTok), center-crop:
ffmpeg -i renders/final_loud.mp4 -vf \
"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
-c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p \
-c:a aac -b:a 192k -movflags +faststart final/clip_9x16.mp4
# YouTube 16:9, 1080p:
ffmpeg -i renders/final_loud.mp4 -vf \
"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
-c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p \
-c:a aac -b:a 256k -movflags +faststart final/clip_16x9.mp4
```
`+faststart` = Web-Streaming; `crf 18–20` = visuell verlustarm; `preset slow` = kleiner bei mehr CPU-Zeit.

---

## 3. Quality-Enhancement — was CPU-only WIRKLICH kann (Ehrlichkeit)

| Stufe | Tool | CPU-only? | Realität |
|---|---|---|---|
| Encoding-Qualität (CRF, preset slow, 10-bit) | ffmpeg/x264/x265 | ✅ | Volle Kontrolle, gratis. Oft sichtbar mehr als „AI-Upscale". Zuerst hier optimieren. |
| Klassisches Upscaling (Lanczos) | `scale=…:flags=lanczos` | ✅ | Sekundenschnell, kein Detailgewinn, aber sauber. 720p→1080p oft genug. |
| Schärfen / Denoise | `unsharp`, `hqdn3d`, `nlmeans` | ✅ | Gute Politur ohne KI (`nlmeans` langsam). |
| **AI-Upscaling (Real-ESRGAN)** | `realesrgan-ncnn-vulkan` | ⚠️ prakt. **nein** | Ohne GPU **Sek.–Min./Frame** → 5-s-Clip = **Stunden**. Unwirtschaftlich. |
| **AI-Interpolation (RIFE)** | `rife-ncnn-vulkan` | ⚠️ prakt. **nein** | Braucht Vulkan/GPU. CPU extrem langsam. |
| Frame-Interpolation (klassisch) | `minterpolate` | ✅ langsam | `minterpolate=fps=60:mi_mode=mci` — Qualität < RIFE, gratis, GPU-frei. |

**Klartext:** Bei der Cloud-Generierung **direkt in Zielauflösung** rendern (billiger als lokales CPU-Upscale).
Lokal nur ffmpeg-Politur. Echtes Real-ESRGAN/RIFE → **Mac-GPU** oder **Cloud-Job über denselben Adapter**
(Replicate hat Real-ESRGAN/RIFE). Topaz = proprietär/GPU-only, kein VPS-Kandidat.

```bash
# Empfohlene CPU-Politur statt AI-Upscale:
ffmpeg -i in_720p.mp4 -vf \
"hqdn3d=1.5:1.5:6:6,scale=1920:1080:flags=lanczos,unsharp=5:5:0.6:5:5:0.0" \
-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy out_1080p.mp4
```

---

## 4. Kosten- / Credit-Management

Teuerste Ressource = die *misslungene Generierung in Zielauflösung*. Vier Hebel (in `video_gen.py` vorbereitet):

- **a) Dry-Run / Preview-first (wichtigster Hebel):** jede Prompt-Iteration zuerst `resolution="480p"`, kurz,
  billigster Provider. Erst wenn's sitzt → 1080p Final.
- **b) Prompt-Hash-Cache:** `generate_cached()` → SHA256 über (provider, model, prompt, params); existiert die
  Datei → **0 Credits**. Nie denselben Prompt zweimal zahlen.
- **c) Batch mit Budget-Guard:** `BudgetGuard(budget.json)` stoppt, bevor Credits (verfallbar!) trocken laufen.
  Alle Shots async submitten, dann gesammelt pollen (spart Wall-Clock + Timeout-Retries).
- **d) Schnitt kostet nie Credits:** Trim, Reihenfolge, Transition, Ton = **rein ffmpeg-lokal**. Nur ein
  *inhaltlich anderer Shot* kostet neu. Das ist der Kern der Ersparnis.
- Rate-Limit (429) → `Retry-After` respektieren, nicht blind neu submitten (jeder Submit kann kosten).
  Provider-Fallback (Higgsfield→fal/Replicate) über die Adapter-Schicht als Verfügbarkeits-/Kostenhebel.

---

## 5. Verzeichnis- / Artefakt-Struktur (wiederholbar)

```
projects/<projekt-name>/
├── storyboard.json     # Single Source of Truth: Shots, Prompts, Provider, Params, Timing, QA
├── budget.json         # Credits übrig, Kosten/Shot, Verbrauchs-Log
├── shots/              # roh generierte Clips (Cloud-Output), 1 Datei je Shot
├── cache/              # prompt-hash-benannte Generate-Cache (Dry-Runs + Finals)
├── audio/              # voiceover.wav (Kokoro), vo.srt, music.mp3
├── luts/               # optionale .cube-LUTs
├── renders/            # Zwischenstufen der Post-Kette (concat_list.txt, rough, with_music, final_loud)
├── final/              # Auslieferung je Export-Preset (clip_16x9.mp4, clip_9x16.mp4)
└── logs/               # run.log (Credits/Provider/Fehler pro Lauf)
```

**Deterministischer Ablauf:** `storyboard.json` lesen → (Dry-Run 480p → Freigabe) → Shots via Adapter+Cache →
concat/xfade → VO+Musik+Ducking → Farbe/Untertitel → loudnorm 2-Pass → Export → `final/`.
Erneuter Lauf mit unveränderten Prompts = 0 Credits (Cache-Hit) + bit-identische Post-Ergebnisse.

---

## Quellen
- [higgsfield-ai/higgsfield-client (offiz. SDK)](https://github.com/higgsfield-ai/higgsfield-client) · [Higgsfield Cloud](https://cloud.higgsfield.ai/) · [CLI/Skills](https://higgsfield.ai/cli)
- [fal-client (PyPI)](https://pypi.org/project/fal-client/) · [fal Python-Docs](https://fal.ai/docs/reference/client-libraries/python)
- [replicate-python](https://github.com/replicate/replicate-python/blob/main/README.md) · [Predictions/Polling](https://replicate.com/docs/topics/predictions/create-a-prediction)
- [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) · [rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan)
- ffmpeg-Filter (offiziell): `xfade` · `sidechaincompress` · `loudnorm` · `subtitles` · `drawtext` · `minterpolate` — [ffmpeg.org/ffmpeg-filters](https://ffmpeg.org/ffmpeg-filters.html)
