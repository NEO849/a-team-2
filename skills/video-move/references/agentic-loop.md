# `video_move` — Agentischer Kern: Selbst-kritisierende Multi-Rollen-Pipeline

Der Skill verkörpert **intern gleichzeitig ein komplettes Produktionsteam** und schließt eine echte
Kritik-Regenerier-Schleife (LLM-as-judge → Regenerate). Der Sprung von „Prompt-rein, Clip-raus" zu
„Team-produziert, selbst-geprüft". Grounding: MovieAgent/StoryAgent (Multi-Agent-Rollen), VideoScore2
(interpretierbares 1–5-Scoring mit CoT), Reference-Image/Character-ID-Konsistenz (Veo/Kling/Seedance).

---

## Leit-Prinzip: Ein Skill, sieben Köpfe, ein Loop

```
   BRIEFING ─▶ CREATIVE DIRECTOR (Nordstern / Veto)
                    │ Creative Bible + Style-DNA
      ┌─────────────┼───────────────────────────┐
      ▼             ▼                            ▼
  SCREENWRITER   DIR. OF PHOTOGRAPHY      TECHNICAL PRODUCER
  (Beats/VO)     (Shots/Licht/Kamera)     (Modell/Budget/Format)
      └─────────────┼───────────────────────────┘
                    ▼
             PROMPT-ENGINEER ── pro Shot ──▶ GENERATION
                    ┌───────────────────────────┘
                    ▼
         ADVERSARIAL QA-REVIEWER (LLM-as-judge, 1–5)
                    │ ACCEPT / REGEN / ESCALATE
                    ▼
             FILM-EDITOR (Schnitt, Ton, Final)
```

**Implementierung:** R1–R5 + R7 als **interne Lenses** im Haupt-Thread (geteilter Kontext = Kohärenz).
**R6 (QA) als eigener Subagent mit FRISCHEM Kontext** — nicht-verhandelbar; adversariell heißt, er darf das
kreative Wunschdenken nicht kennen, sonst bewertet er wohlwollend. Spiegelt das Muster eines adversarial reviewers.

---

## 1. Rollen-Stack (7 Rollen)

### R1 — Creative Director (Opus-Lens · Nordstern & Veto)
- **Verantwortung:** Briefing → verbindliche **Creative Bible** (Kernbotschaft, Zielemotion, Zielgruppe, Ton, Referenzen, Do/Don't). Hält Kohärenz über alle Shots. Einziges **Veto** im Final-Gate.
- **Input:** User-Briefing (Zweck, Dauer, Plattform, Stimmung, Marke, ggf. Referenzbilder).
- **Output:** `creative_bible.md` + **Style-DNA** (Palette, Grain/Look, Objektiv-Charakter, Bewegungsphilosophie, Character-Sheets).
- **Entscheidet:** Die *eine* Botschaft? Emotionale Kurve? Tabus? → definiert die Zielfunktion, gegen die QA misst.

### R2 — Screenwriter / Story-Architekt (Sonnet-Lens · Narrativ)
- **Verantwortung:** Botschaft → **Beat-Struktur** (Hook → Aufbau → Peak → Resolve), timing-bewusst. Schreibt VO/On-Screen-Text, sorgt für Sog und Cut-Rhythmus.
- **Output:** `beatsheet.json` — Beats mit Dauer-Budget, VO-Text, emotionalem Ziel je Beat.
- **Entscheidet:** Reihenfolge & Timing; wo der Hook sitzt; wo geschnitten wird.

### R3 — Director of Photography (Sonnet-Lens · Bild)
- **Verantwortung:** Jeden Beat → **konkrete Shots** (Einstellungsgröße, Kamerabewegung, Objektiv, Licht, Komposition, Mood). Sichert visuelle Kontinuität (Licht-/Farbanschluss Nachbar-Shots).
- **Output:** `shotlist` → speist `storyboard.json`.
- **Entscheidet:** Wie sieht jeder Moment aus? Stärkster Qualitätshebel (Dolly-in vs. Static, 35mm vs. 85mm, Golden-Hour vs. Neon).

### R4 — Technical Producer (Sonnet-Lens · Machbarkeit & Budget)
- **Verantwortung:** Pro Shot das **richtige Modell** (Matrix §4), Auflösung, Aspect, Länge, Seed-Strategie, t2v vs. i2v. Verwaltet **Kosten-Budget** + Regenerier-Kontingent.
- **Output:** `render_plan` je Shot: engine, mode, resolution, aspect, seed, max_regen, cost_estimate.
- **Entscheidet:** Was ist bezahlbar/machbar? Wo lohnt ein teureres Modell (Hero-Shot)? Wann „ship best-of".

### R5 — Prompt-Engineer (Sonnet-Lens · Übersetzer Mensch→Modell)
- **Verantwortung:** Shot + Style-DNA + Modell-Eigenheiten → **finaler modell-spezifischer Prompt** (+ Negative-Prompt, Ref-Images, Seed, Motion-Strength). Kennt die Dialekte (Veo=Prosa/JSON, Kling=Kamera-Verben, Seedance=@-Refs).
- **Input:** Ein Shot, Style-DNA, `render_plan`, **QA-Feedback der Vorrunde** (bei Regen).
- **Entscheidet:** Exakte Wortwahl, Negative-Prompt-Inhalt, welche Referenz, Seed halten/variieren.

### R6 — Adversarial QA-Reviewer (Opus-Subagent · frischer Kontext)
- **Verantwortung:** Bewertet **jeden Shot** gegen Prompt-Adherence, Style-DNA, Cinematik, Technik (Rubrik §3) + **Anschluss zum Nachbar-Shot**. Liefert **umsetzbares** Feedback, keine Gefälligkeits-5.
- **Input:** Clip + Shot + Prompt + Vorgänger-Shot. **Nicht** das kreative Wunschdenken.
- **Output:** `qa[shot]` — Score je Achse (1–5), Verdikt `ACCEPT`/`REGEN`/`ESCALATE`, Mängel + **Fix-Hinweis**.
- **Entscheidet:** Gut genug? Wenn nein: *warum genau* und *was ändern*. Herz der Selbst-Kritik.

### R7 — Film-Editor (Sonnet-Lens · Schnitt & Final)
- **Verantwortung:** Akzeptierte Shots → Film: Cut-Timing/Rhythmus, Transitions, Farb-Match, Musik/SFX/VO-Sync, Titel, Export. Letzter Gesamteindruck vor Director-Veto.
- **Output:** `final.mp4` (+ Plattform-Varianten), `edit_decision_list.json`.
- **Entscheidet:** Cut-Punkte, Übergänge, Ton-Mix, ob das *Ganze* rund ist.

> **Warum getrennt?** Ein Ein-Prompt-Tool kollabiert R2–R5 und hat kein R6. Genau die Trennung
> DP↔Prompt-Engineer↔Kritiker erzeugt Qualität: drei verschiedene Optimierungsziele (Cinematik /
> Modell-Dialekt / Fehler), die sich gegenseitig korrigieren.

---

## 2. Pipeline (Phasen + Loop)

```
PHASE 0  BRIEF INTAKE   Director: Briefing → creative_bible.md + Style-DNA
                        (Rückfragen NUR wenn Zweck/Dauer/Plattform fehlen — sonst annehmen + dokumentieren)
PHASE 1  KONZEPT/MOODBOARD  "Konzept-Konferenz" (Lenses R1+R2+R3):
         Screenwriter→beatsheet.json · DP→Moodboard (1 Standbild/Beat, günstig)
         GATE A: Director-Approval des Moodboards. Billig scheitern BEVOR teuer generiert.
PHASE 2  STORYBOARD  DP+Producer → storyboard.json (Schema §5): Shots, Kontinuität, Seed-Plan, Modell, Regen-Budget.
PHASE 3  PROMPT-GEN  Prompt-Engineer → prompt + negative_prompt + Ref-Attachments je Shot.

┌─── PHASE 4  GENERATE→JUDGE→REGEN  (Kern-Loop, pro Shot) ───────────────────────────┐
│ 4a GENERATE  Backend rendert Shot (Seed aus Plan)                                  │
│ 4b JUDGE     QA-Reviewer (frischer Subagent) → Scores + Verdikt (§3)               │
│ 4c DECIDE    ACCEPT → einfrieren, nächster Shot                                    │
│              REGEN  → Prompt-Engineer bekommt QA-Fix-Hinweis → gezielter Prompt/Seed → 4a │
│              ESCALATE → Producer wechselt Modell/Mode ODER DP überarbeitet Shot → 4a │
└────────────────────────────────────────────────────────────────────────────────────┘

PHASE 5  ASSEMBLY  Editor: Schnitt, Color-Continuity-Pass, VO/Musik-Sync, Captions.
PHASE 6  FINAL GATE  QA bewertet GESAMTFILM (Kohärenz/Fluss/Emotion-Kurve) + Director-Veto → Export.
```

### Abbruch-/Terminierung Kern-Loop (Pflicht — erstes Zutreffende gewinnt)
| Kriterium | Aktion |
|---|---|
| Verdikt `ACCEPT` (weighted ≥ Schwelle, kein K.O.) | akzeptiert, Loop-Ende |
| `attempt == max_regen` (Default 3) | **best-of** (höchster QA-Score), `accepted_with_caveat`, weiter |
| Score-Delta zweier Folgeversuche < 0.3 (Plateau) | Regen bringt nichts → best-of, weiter (spart Budget) |
| `ESCALATE` 2× am selben Shot | Producer-Downgrade: einfacherer/robuster Shot (statisch statt komplexe Bewegung) |
| Globales Budget-Cap erreicht | laufenden Shot mit best-of abschließen, Rest einfrieren, → Phase 5 |

Phase 6: max. 1 globale Re-Cut-Runde + max. 2 gezielte Shot-Regens, dann Auslieferung mit
`known_limitations`. **Kein Endlos-Polieren** — 45%-Disziplin auf Video: Restschwächen ehrlich ausweisen.

---

## 3. Qualitäts-Rubrik (LLM-as-judge, angelehnt an VideoScore2)

QA bewertet jeden Shot auf **6 Achsen** (Score 1–5 + Begründung + Fix-Hinweis). Zwei sind **K.O.-fähig**.

| # | Kriterium | 1 (K.O.) | 3 | 5 | Gewicht |
|---|---|---|---|---|---|
| C1 | **Prompt-Adherence** (Subjekt/Aktion/Framing wie spezifiziert) | Motiv falsch/fehlt | Kern da, Details daneben | exakt | ×2 |
| C2 | **Cinematic Quality** (Komposition/Licht/Look, „sieht teuer aus") | flach/amateurhaft | solide, generisch | preisverdächtig | ×1.5 |
| C3 | **Konsistenz zu Nachbar-Shots** (Character-ID/Palette/Licht/Set) | Bruch (anderes Gesicht) | leichte Drift | nahtlos | ×2 (K.O.) |
| C4 | **Motion-Stabilität** (flüssig, physikplausibel) | Warping/Teleport/Morph | leichtes Ruckeln | butterweich | ×1.5 |
| C5 | **Artefakt-Freiheit** (Hände/Gesichter/Text/Flackern) | grobe Artefakte (6 Finger) | klein, wegschneidbar | sauber | ×1.5 (K.O.) |
| C6 | **Emotion / Intent** (trifft die Beat-Gefühlslage) | tot/falsch | neutral | genau Zielemotion | ×1 |

**Entscheidungsregel:**
```
weighted = Σ(score_i × weight_i) / Σ(weight_i)          # 1.0 – 5.0
if C1==1 or C3==1 or C5==1:            → ESCALATE   # harter Bruch, kein Reroll heilt das
elif weighted >= 4.0 and min(scores) >= 3: → ACCEPT
elif weighted >= 3.0:                  → REGEN      # gezielt: schwächste Achse fixen
else:                                  → ESCALATE   # strukturell zu schlecht
```
- **REGEN ist gezielt, nicht Zufall:** schwache Achse → genau das ändern (C4 schwach → Motion-Strength runter / „subtle slow move"; C5 Hände → Hände ins Negative-Prompt / enger framen). **Blindes Seed-Neuwürfeln ist verboten** — Unterschied zwischen „Slot-Machine" und „Regie".
- **ESCALATE** = Storyboard/Modell schuld → Producer/DP greifen ein (Modellwechsel, Keyframe-first, Shot vereinfachen).
- **Anti-Gefälligkeit:** QA-Subagent startet frisch mit Auftrag „finde die drei größten Schwächen zuerst". Optional Selbst-Konsistenz (2 Judgings, bei Divergenz >1 ein drittes als Tiebreak).

---

## 4. Character/Style-Consistency (stark → ergänzend)

1. **Reference-Image / Character-ID (stärkster Hebel):** Veo 3.1 „Ingredients" (bis 3 Refs), Kling 3.0 „Character ID"/Elements, Seedance 2.0 „Face Lock". → DP generiert in Phase 1 ein **Character-Sheet** (1–2 Turnaround-Frames/Figur) + **Style-Frame**; diese werden an *jeden* Shot mit der Figur angehängt.
2. **Keyframe-first / i2v statt reinem t2v:** erst Standbild → per First-Frame-Conditioning animieren. Für Cuts: **Last-Frame des Vorgänger-Shots als First-Frame des Folge-Shots** (Frame-Chaining) → nahtloser Anschluss.
3. **Seed-Disziplin:** gleicher Seed für einen Batch verwandter Shots (`seed_group` je Szene). Bei REGEN einer Achse Seed **halten**, nur Prompt justieren (Änderung isolieren); nur bei Total-Fehlschlag Seed variieren.
4. **Style-Anchors + Negative-Prompt:** fixer, wortgleicher Stil-Block (Palette/Grain/Objektiv/Licht) vor *jeden* Prompt; globales Negative-Prompt („inconsistent face, extra fingers, warped hands, text artifacts, style shift, oversaturated") läuft überall mit.
5. **Modell-Wahl-Matrix (Producer entscheidet pro Shot):**

| Bedarf | Bevorzugt | Grund |
|---|---|---|
| Wiederkehrende Figur über viele Shots | Kling Character-ID/Elements | stärkstes Identitäts-Tracking |
| Ein Primär-Gesicht, Nahaufnahme | Seedance Face-Lock | geometrische Gesichts-Constraints |
| Hero-Shot, max. Cinematik + 3 Refs | Veo 3.1 (Ingredients) | reiche Prosa + Multi-Ref |
| Exakter Anschluss-Cut | Keyframe-first (i2v, Frame-Chaining) | fixiert First-Frame |
| Günstiger/statischer Füller | robustestes/billigstes t2v | Budget schonen |

6. **Consistency als eigene QA-Achse (C3):** Reviewer bekommt Vorgänger + aktuellen Shot → Konsistenz wird nicht nur *erzeugt*, sondern *gemessen und erzwungen*.

---

## 5. `storyboard.json` — vollständiges Schema (3 Shots)

Zentrales Artefakt, das DP + Producer + Prompt-Engineer + QA + Editor teilen. **State = das JSON** →
jede Phase liest/schreibt es, der Loop bleibt resumierbar und auditierbar.

```json
{
  "project": {
    "id": "vm-2026-0709-brandhook",
    "brief": "30s Vertical-Ad: Handwerker-Startup, Vertrauen + Moderne, Zielgruppe 30-50, warm-premium.",
    "target_duration_s": 30,
    "aspect_ratio": "9:16",
    "platform": "instagram_reels",
    "emotional_arc": ["Neugier", "Vertrauen", "Stolz", "Call-to-Action"]
  },
  "style_dna": {
    "palette": ["#1A2238 deep-navy", "#F4A259 warm-amber", "#F6F4F1 bone-white"],
    "look": "cinematic, soft film grain, gentle halation, shallow depth of field",
    "lens_character": "35mm anamorphic feel, subtle bokeh",
    "lighting": "golden-hour warmth, soft key from window-left",
    "motion_philosophy": "slow, deliberate camera moves; no whip pans",
    "global_negative_prompt": "extra fingers, warped hands, deformed face, text artifacts, style shift, oversaturation, jitter, morphing",
    "reference_images": {
      "character_lena": ["refs/lena_sheet_front.png", "refs/lena_sheet_3q.png"],
      "style_frame": ["refs/style_anchor_golden.png"]
    },
    "seed_master": 730294
  },
  "shots": [
    {
      "id": "S01", "beat": "Hook", "duration_s": 4,
      "intent": "Neugier wecken: Hände formen Holz, Staub tanzt im Gegenlicht.",
      "target_emotion": "Neugier",
      "photography": { "framing": "extreme close-up", "camera_move": "slow dolly-in",
        "lens": "85mm", "lighting": "backlit golden hour, floating dust",
        "composition": "hands lower-third, rim light on wood grain" },
      "continuity": { "prev": null, "next": "S02", "carry_first_frame": false },
      "consistency": { "characters": [], "reference_images": ["refs/style_anchor_golden.png"], "hold_seed": true },
      "render_plan": { "engine": "veo-3.1", "mode": "t2v", "resolution": "1080x1920",
        "seed": 730294, "max_regen": 3, "cost_estimate_usd": 0.40 },
      "prompt": "Extreme close-up of skilled hands sanding warm oak, fine dust floating in backlit golden-hour light, slow dolly-in, 85mm shallow depth of field, cinematic film grain, gentle halation, deep-navy shadows and warm-amber highlights.",
      "negative_prompt": "extra fingers, warped hands, style shift, jitter",
      "qa": { "attempts": 2,
        "scores": { "C1": 5, "C2": 5, "C3": 5, "C4": 4, "C5": 4, "C6": 5 },
        "weighted": 4.6, "verdict": "ACCEPT",
        "notes": "Attempt 1 hatte 6 Finger (C5=1); Fix: 'hands' enger geframed + Negative verstärkt. Attempt 2 sauber.",
        "accepted_asset": "renders/S01_a2.mp4" }
    },
    {
      "id": "S02", "beat": "Aufbau", "duration_s": 6,
      "intent": "Lena (Gründerin) blickt zufrieden auf ihr Werk — Vertrauen aufbauen.",
      "target_emotion": "Vertrauen",
      "photography": { "framing": "medium close-up", "camera_move": "static, slight breathing",
        "lens": "35mm", "lighting": "soft window key from left, warm ambient",
        "composition": "Lena screen-right, workshop bokeh left" },
      "continuity": { "prev": "S01", "next": "S03", "carry_first_frame": false },
      "consistency": { "characters": ["character_lena"],
        "reference_images": ["refs/lena_sheet_front.png", "refs/lena_sheet_3q.png", "refs/style_anchor_golden.png"],
        "hold_seed": true },
      "render_plan": { "engine": "kling-3.0", "mode": "i2v", "keyframe": "keyframes/S02_lena.png",
        "resolution": "1080x1920", "seed": 730294, "max_regen": 3, "cost_estimate_usd": 0.55 },
      "prompt": "Medium close-up of Lena, a woman in her early 40s (see reference), calm confident smile as she looks at finished woodwork, soft window key light from left, warm workshop bokeh, 35mm, shallow depth of field, cinematic warm-amber grade, subtle film grain.",
      "negative_prompt": "different face, age shift, deformed features, style shift, harsh light",
      "qa": { "attempts": 1,
        "scores": { "C1": 5, "C2": 4, "C3": 5, "C4": 5, "C5": 5, "C6": 4 },
        "weighted": 4.7, "verdict": "ACCEPT",
        "notes": "Character-ID + Keyframe hielten Lenas Gesicht exakt zum Sheet. Konsistenz C3=5.",
        "accepted_asset": "renders/S02_a1.mp4" }
    },
    {
      "id": "S03", "beat": "Peak → CTA", "duration_s": 5,
      "intent": "Fertiges Möbelstück im Raum, Logo-Reveal, Aufforderung.",
      "target_emotion": "Stolz",
      "photography": { "framing": "wide establishing", "camera_move": "slow crane-up",
        "lens": "24mm", "lighting": "golden-hour flooding through large window",
        "composition": "finished cabinet centered, negative space top for logo" },
      "continuity": { "prev": "S02", "next": null, "carry_first_frame": false },
      "consistency": { "characters": [], "reference_images": ["refs/style_anchor_golden.png"], "hold_seed": false },
      "render_plan": { "engine": "veo-3.1", "mode": "t2v", "resolution": "1080x1920",
        "seed": 481120, "max_regen": 3, "cost_estimate_usd": 0.40 },
      "prompt": "Wide establishing shot of a beautifully crafted oak cabinet in a sunlit modern workshop, golden-hour light flooding through a large window, slow crane-up revealing negative space at top for a logo, 24mm, cinematic warm grade, soft film grain, premium feel.",
      "negative_prompt": "clutter, style shift, blown highlights, warped geometry",
      "qa": { "attempts": 3,
        "scores": { "C1": 4, "C2": 5, "C3": 4, "C4": 3, "C5": 4, "C6": 4 },
        "weighted": 4.0, "verdict": "ACCEPT",
        "notes": "Crane-Move erzeugte anfangs Geometrie-Warp (C4=2→REGEN). Fix: 'slow, subtle crane' + Motion-Strength reduziert. Attempt 3 stabil, best-of akzeptiert.",
        "accepted_asset": "renders/S03_a3.mp4" }
    }
  ],
  "edit": {
    "order": ["S01", "S02", "S03"],
    "transitions": ["hard-cut", "hard-cut"],
    "color_continuity_pass": true,
    "audio": { "music": "warm-acoustic-uplift.mp3", "vo_from": "beatsheet.json", "captions": true },
    "final_gate": {
      "overall_scores": { "coherence": 5, "flow": 4, "emotion_arc": 5 },
      "director_verdict": "APPROVED",
      "known_limitations": ["S03 leichte Rest-Bewegungsunruhe im oberen Bildrand, unter Logo kaschiert"]
    }
  }
}
```

---

## Umsetzungs-Hinweise
- **Lens vs. Subagent:** R1–R5+R7 als sequentielle Lenses im Haupt-Thread; **R6 (QA) eigener Subagent, frischer Kontext** — nicht verhandelbar (echter Adversarial-Judge, das Muster eines adversarial reviewers).
- **State = `storyboard.json`:** einziger Wahrheits-Zustand; jede Phase liest/schreibt → resumierbar + auditierbar.
- **Terminierung Pflicht:** `max_regen`, Plateau-Delta, Budget-Cap. Restschwächen in `known_limitations` (45%-Disziplin).
- **Backend-agnostisch:** `render_plan.engine` abstrahiert das Modell → `scripts/video_gen.py`-Adapter; Backend-Ausfall = Producer-Fallback im selben JSON.

## Quellen
- [VideoScore2 (arXiv 2509.22799)](https://arxiv.org/html/2509.22799v1) — Basis der Rubrik §3 · [VideoScore (2406.15252)](https://arxiv.org/html/2406.15252v2) · [VideoJudge (2509.21451)](https://arxiv.org/pdf/2509.21451)
- [MovieAgent (GitHub)](https://github.com/showlab/MovieAgent) · [StoryAgent (2411.04925)](https://arxiv.org/pdf/2411.04925)
- [Long-Form AI Video Character Consistency 2026](https://www.aimagicx.com/blog/long-form-ai-video-character-consistency-guide-2026) · [AI Video Models Comparison 2026](https://opencreator.io/blog/ai-video-models-comparison-2026)
