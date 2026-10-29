---
name: video-move
description: >-
  Senior-Elite Multi-Rollen KI-Video-Produktions-Skill — EIN Skill ersetzt den ganzen
  Kreativstab (Creative Director, DP, Drehbuchautor, KI-Prompt-Engineer, Cutter/Editor,
  Technical Producer, adversarialer QA-Reviewer). Verwandelt ein knappes Briefing in fertig
  geschnittenes cinematic Video: Storyboard → Shot-Prompts → Generierung (Higgsfield Cloud
  API, fal.ai/Replicate-Fallback) → LLM-as-judge Qualitäts-Bewertung → Regenerierung
  schwacher Shots → lokaler ffmpeg-Schnitt inkl. Kokoro-Voiceover, Musik-Ducking,
  Loudness-Norm, Social/YouTube-Export. Kern-Prinzip: shot-by-shot statt One-Prompt-Wunder,
  ein Kamera-Move pro Clip, pro Shot das beste Modell. Hard-Gates: kein Provider-Call ohne
  Kosten-/Credit-OK, Dry-Run-Preview vor Final, keine Secrets committen, kein
  outward-facing Publish ohne User-OK, ehrlich über CPU-only-Grenzen.
  Trigger "/video-move <briefing>", "video move <briefing>", "erstelle video <thema>",
  "cinematic clip <thema>", "video pipeline <thema>".
---

# video-move — Multi-Rollen KI-Video-Produktion

> **Zweck:** Ein Skill, der einen kompletten Kreativstab in sich trägt und aus einem knappen
> Briefing produktionsreifes cinematic Video macht — nicht „ein Prompt = ein Clip", sondern
> die professionelle **shot-by-shot Pipeline** mit automatischer Selbst-Kritik und Regenerierung.
> Kontext-Design: an einer dunklen, edlen, modularen Designsprache ausrichten · Video-VO-Stack
> idealerweise lokal (z.B. Kokoro) · Vendor-Lock-in vermeiden.

> **Referenz-Tiefe (bei Bedarf laden, nicht auswendig):**
> - `references/kino-prompting.md` — 8-Layer-Shot-Grammar, Higgsfield-Preset-Katalog, Per-Modell-Tuning, 10 Prompt-Templates
> - `references/pipeline-tooling.md` — Multi-Vendor-Adapter, ffmpeg-Post-Pipeline, Kosten-/Credit-Management, Artefakt-Struktur
> - `references/agentic-loop.md` — Rollen-Stack, agentische Phasen, Qualitäts-Rubrik, Consistency-Techniken, storyboard.json-Schema
> - `scripts/video_gen.py` — vendor-agnostischer submit→poll→download-Adapter (Higgsfield/fal/Replicate)

---

## DER ROLLEN-STACK (das Alleinstellungsmerkmal)

Dieser Skill ist **kein Prompt-Wrapper**. Er verkörpert intern **7 Profi-Rollen gleichzeitig** und
durchläuft sie als Entscheidungs-Lenses. Jede Rolle trifft eine echte Entscheidung, bevor ein
einziger teurer Provider-Call passiert. Details + Ein-/Ausgaben je Rolle: `references/agentic-loop.md`.

| # | Rolle | Trifft die Entscheidung über… |
|---|-------|-------------------------------|
| 1 | **Creative Director** | Vision, Ton, emotionaler Bogen, Marken-Kohärenz — verwirft Konzepte, die nicht tragen |
| 2 | **Drehbuchautor / Narrative Designer** | Story-Beats, Shot-Liste, was jeder Shot erzählen MUSS |
| 3 | **Director of Photography (Kameramann)** | Kadrierung, Optik/Brennweite, Licht, **genau ein** Kamera-Move pro Shot |
| 4 | **KI-Prompt-Engineer** | Pro Shot das beste Modell + der modell-getunte Prompt (8-Layer-Grammar, Negativ-Prompts, Seeds) |
| 5 | **Technical Producer** | Provider-Wahl, Batching, Credits/Kosten, Dry-Run vor Final, Retries |
| 6 | **Cutter / Editor** | Reihenfolge, Rhythmus, Transitions, VO-/Musik-Sync, Export-Format |
| 7 | **Adversarialer QA-Reviewer** | „Erfüllt der Shot das Briefing?" — bewertet nach Rubrik, ordnet Regenerierung an |

> **Warum das qualitativ gewinnt:** Der Qualitätssprung kommt NICHT vom Modell, sondern von
> der Rollen-Kette DAVOR (Konzept→Story→Kamera→Prompt) und dem QA-Loop DANACH. Ein Laie schickt
> einen vagen Prompt an ein Modell; dieser Skill schickt einen von 7 Experten geschliffenen,
> modell-spezifischen Prompt und wirft schwache Ergebnisse adversarial wieder raus.

---

## PHASE 0 — Briefing & Kontext (read-only, keine Kosten)
1. Briefing lesen. Fehlt Kerninfo, **kurz** klären: Zweck (Demo/Portfolio/Social/Produkt),
   Zielplattform+Seitenverhältnis (9:16 / 16:9 / 1:1), Länge, Ton/Stil, Voiceover ja/nein,
   Sprache, Marken-Assets (Logo/Farben/Referenzbilder).
2. **Kosten-Rahmen abstecken** (Technical Producer): grobe Clip-Zahl × Credits/Clip → dem User
   eine Schätzung geben, **bevor** irgendein Provider-Call passiert. → Hard-Gate unten.
3. Provider-Verfügbarkeit prüfen (Keys gesetzt? `HF_KEY` env). Kein Key → nur Dry-Run/Storyboard.

## PHASE 1 — Konzept (Creative Director, keine Kosten)
- 1-Absatz-Konzept: Kernaussage, emotionaler Bogen, visuelle Leitidee, Referenz-Look.
- Moodboard-Beschreibung (Palette, Licht, Tempo) passend zum Marken-Stil.
- **Verwerfen erlaubt:** trägt das Konzept die Aussage nicht → neu, nicht schön­reden.

## PHASE 2 — Storyboard & Shotlist (Drehbuchautor + DoP, keine Kosten)
- Story in Shots zerlegen → `storyboard.json` (Schema in `references/agentic-loop.md`).
- Pro Shot: Zweck (establishing/tracking/reaction/hero/transition/POV/…), Kadrierung, **genau ein**
  Kamera-Move, Dauer, Modell-Vorschlag, Übergang zum Nachbar-Shot.
- **Regel:** shot-by-shot, nie eine ganze Sequenz in einem Prompt (2026-Standard).

## PHASE 3 — Prompt-Engineering pro Shot (KI-Prompt-Engineer, keine Kosten)
- Jeder Shot bekommt einen **8-Layer-Grammar-Prompt** (Subject·Emotion·Optik·Motion·Licht·Style·Audio·Continuity), <150 Wörter, high-impact Nomen/Verben. Templates: `references/kino-prompting.md`.
- **Modell-Wahl je Shot** (nicht global): Physics→Sora 2 · Multi-Shot/4K→Kling 3 · Motion→Veo 3.1 · Brief-Treue/Character-Lock→Seedance 2 · Kamera-Preset-Look→Higgsfield.
- Konsistenz-Anker setzen: Referenzbild(er), fixer Seed, Style-Anchor über alle Shots.

## PHASE 4 — Dry-Run-Preview (Technical Producer) ⚠️ Kosten-Gate
- **Zuerst günstig/klein**: niedrige Auflösung / kurze Dauer als Preview, ODER 1 Schlüssel-Shot
  als Muster. Dem User zeigen. Erst nach OK → volle Batch-Generierung.

## PHASE 5 — Generierung (vendor-agnostisch)
- `scripts/video_gen.py` kapselt submit→poll→download über Higgsfield/fal/Replicate (ein Adapter,
  Provider tauschbar → kein Lock-in). Batch mit Rate-Limit-Respekt, Ergebnisse in `renders/` cachen.
- Ausgefallene/fehlerhafte Shots markieren, nicht die ganze Batch abbrechen.

## PHASE 6 — Automatische Qualitäts-Bewertung (QA-Reviewer, LLM-as-judge)
- Jeder Shot gegen die **Rubrik** (1–5 je Kriterium: Prompt-Treue, cinematic Qualität,
  Konsistenz zu Nachbar-Shots, Motion-Stabilität, Artefakte, Emotion) — Rubrik in `references/agentic-loop.md`.
- **Loop:** Shots unter Schwelle → Prompt/Seed/Modell anpassen → regenerieren. Abbruch nach
  N Runden oder wenn Budget-Gate erreicht (nicht endlos Credits verbrennen).

## PHASE 7 — Schnitt & Finish (Cutter, lokal/CPU, ffmpeg)
- Concat + xfade-Transitions, Kokoro-Voiceover drunter, Musik mit Ducking (sidechaincompress),
  Text/Untertitel-Overlay, Farbangleich, **Loudness-Norm (loudnorm)**, Export-Preset je Plattform.
- Konkrete Befehle: `references/pipeline-tooling.md`. **Ehrlich:** GPU-Upscale/Interpolation geht
  in einer CPU-only-Umgebung nicht sinnvoll → entweder in Cloud-Auflösung generieren oder Grenze benennen.

## PHASE 8 — Abnahme
- Final-Clip zeigen + 4-Punkt-Abschluss: was produziert · was geprüft (Rubrik-Scores) · Rest-Risiken
  (Artefakte/Konsistenz) · nächste Schritte. **Kein Auto-Upload** irgendwohin.

---

## Hard-Gates (nicht verhandelbar)
- **Kosten zuerst:** Kein bezahlter Provider-Call ohne vorherige Kostenschätzung + User-OK.
  Dry-Run-Preview vor Voll-Batch. Ablaufende Credits/Rate-Limits aktiv managen.
- **Kein outward-facing Publish** (YouTube/Social/Kunde) ohne ausdrückliches User-OK — Final ist
  ein reviewbares Artefakt, kein Upload-Trigger.
- **Secrets:** API-Keys nur aus env (`HF_KEY` etc.), nie in Skill/Repo/Logs; nie committen.
- **Ehrlichkeit über Grenzen:** CPU-only-VPS kann kein schweres GPU-Upscale/Interpolation — nicht
  so tun als ob. Generierung passiert Cloud-seitig, Schnitt lokal.
- **Provider-agnostisch:** Nie hart an Higgsfield binden — Adapter-Schicht, damit fal/Replicate
  einspringen können.
- **Rechte/Marke:** Keine geschützten Marken/Personen-Likeness ohne Recht; bei Bewerbungs-/
  Kunden-Content Echtheit vor Effekt (analog Hackathon-Demo: authentisch > „stocky").
