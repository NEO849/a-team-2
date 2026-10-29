---
name: remotion-video
description: >
  Code-deterministe Video-Erstellung mit Remotion (React → MP4) — der reproduzierbare,
  programmatische Gegenpol zu /video-move (generatives KI-Video). Für Demo-Videos
  (Hackathons, Produkt-Walkthroughs), animierte One-Pager/Marketing-Clips, datengetriebene
  Motion-Graphics, wo exakte versionierbare Kontrolle zählt statt KI-Sampling. Workflow
  (in dieser Umgebung verifiziert): npx create-video scaffold → React-Kompositionen bauen →
  npx remotion render → MP4 (nutzt eigene chrome-headless-shell + ffmpeg). ⚠ Lizenz: Remotion
  gratis für Teams bis 3 Personen, ab Unternehmensgröße kostenpflichtig (remotion.pro/license) —
  vor Firmeneinsatz prüfen. Für KI-generierte Shots/Voiceover siehe /video-move.
  Trigger "/remotion-video <idee>", "remotion <video>", "code-video <thema>",
  "demo-video bauen <projekt>", "react video <x>", "animiertes video <thema>".
---

# remotion-video — Video aus Code (React → MP4)

> Rolle: Motion-Engineer. Deterministisch/versionierbar — jeder Frame aus Code, kein KI-Sampling.
> Basiert auf remotion-dev/skills-Best-Practices; Pipeline in dieser Umgebung end-to-end verifiziert.

## Wann laden (vs. /video-move)
| Braucht… | Skill |
|---|---|
| Exakte, reproduzierbare, code-getriebene Animation (Text/Charts/Screencast-Overlays, Marketing-Clip, Demo) | **remotion-video** |
| Fotorealistische/kreative KI-generierte Shots, Voiceover-Vertonung | `/video-move` |
Beide kombinierbar: Remotion für die deterministische Hülle, /video-move-Assets als Einbettung.

## Verifizierte Pipeline
Voraussetzungen (in dieser Umgebung vorhanden): node 20, npx, ffmpeg; Remotion lädt seine eigene
chrome-headless-shell beim ersten `npm install`. **Netz nötig → im Vordergrund/mit Egress ausführen,
nicht in netzloser Sandbox** (sonst npm-Registry-Fehler).

```bash
# 1. Scaffold (einmal pro Projekt)
npx --yes create-video@latest --yes --blank --no-tailwind my-video
cd my-video && npm i          # zieht chrome-headless-shell (~92 MB) beim ersten Mal

# 2. Kompositionen bauen — React-Markup in src/ (Composition mit id, fps, Maßen, durationInFrames)
#    Vorschau (Studio, langlebiger Prozess): npx remotion studio --no-open

# 3. Verfügbare Kompositionen auflisten (liefert exakte IDs)
npx remotion compositions          # z.B.  MyComp   30   1280x720   60 (2.00 sec)

# 4. Rendern — EXAKTE Composition-ID übergeben (nicht raten; ID aus Schritt 3)
npx remotion render <CompId> out/video.mp4
#    Still:  npx remotion still <CompId> out/frame.png
```

Fallstrick (aus dem Spike gelernt): `npx remotion render` braucht die **echte Composition-ID**;
Fortschritts-/Bundling-Zeilen sind KEINE IDs. Immer erst `compositions` lesen, dann die ID rendern.

## Best Practices (Progressive Disclosure)
Video-first Layout & Textgrößen, Interaktivität (Studio-Edits schreiben zurück in Code), Tailwind,
Captions, Multimedia — diese leben in den offiziellen `remotion-dev/skills` Referenz-Skills
(remotion-markup, remotion-best-practices, remotion-interactivity). Bei tieferem Bedarf: dort nachlesen
(remotion.dev/docs). Hier bewusst nur der End-to-End-Renderpfad.

## Lizenz-Gate (⚠ vor Firmeneinsatz)
Remotion ist **gratis für Einzelpersonen und Teams bis 3**. Ab Unternehmensgröße kostenpflichtig
(remotion.pro/license). Für Solo-/Hackathon-/Eigengebrauch frei — bei kommerziellem Auftrag eines
größeren Teams Lizenz prüfen, bevor gerendert/ausgeliefert wird.

## Hard-Gates (Abschluss)
- Render-Ergebnis verifizieren, nicht behaupten: `file out/video.mp4` + Größe > 0 (frisch, dieser Turn).
- Netz-Schritte (`npm i`) im Vordergrund/mit Egress. Read-only-first bei fremden Assets.
- Siehe `_shared/hard-gates.md`.
