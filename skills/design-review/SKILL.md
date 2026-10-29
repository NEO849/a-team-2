---
name: design-review
description: >-
  Adversariale VISUELLE Qualitäts-Kritik einer gebauten UI/Animation vor dem Ausliefern — die HÄRTEN-Stufe
  der Design-Familie. Fährt eine mechanische ~60-Punkt-Pre-Flight (zählbare Anti-Slop-Gates), eine
  Batched-Screenshot-Verifikation (build → einmal inspizieren Desktop+Mobile → in einem Batch fixen →
  ≤1 Bestätigungsrunde → stoppen) und ein Audit-first-Redesign-Protokoll. Ergänzt die Text-Taste-Skills
  (humanize/slop-check/hype-check prüfen Prosa, DIES prüft Layout/Farbe/Typo/Motion/Browser-Surfaces) und
  design-craft/motion-craft (die bauen). Für Skill-Qualität statt UI-Qualität siehe skill-doctor/skill-harden.
  Kein Auto-Fix ohne dass die Findings zuerst berichtet werden. Trigger "/design-review", "review dieses ui",
  "ist das design slop", "visual critique <x>", "pre-flight <seite>", "härte das design".
---

# design-review — die letzte Instanz vor „fertig"

> Rolle: **Skeptischer Design-Director + QA-Lead**. Aufgabe ist DISprove: das Design als Slop entlarven und
> nur durchlassen, was die mechanische Pre-Flight und die Auge-Prüfung übersteht. Keine Höflichkeit — Findings.

## Wann laden
Nach dem Bau durch `design-craft`/`motion-craft`, vor jeder Auslieferung. Oder wenn ein bestehendes UI
sich „irgendwie generisch" anfühlt und du wissen willst warum. Für die reine *Text*-Qualität → `slop-check`/`humanize`.

## Werkzeug
- **Mechanische Pre-Flight** (die ~60 Binär-Gates, viele zählbar) → `references/visual-preflight.md`.
- **Anti-Slop-Wahrheitsquelle** (die Regeln dahinter) → Skill `design-craft`, Datei craft-floor.md.
- **Browser-Surface-Check** (das häufigst-übersehene Craft-Signal) → `references/browser-surfaces.md`.
- **Detektor** (zählbare Tells automatisch): `python3 ../design-craft/scripts/design_lint.py <pfade>` — advisory, blockt nicht.
- **Screenshots:** im Projekt-Track via `claude-in-chrome`/`playwright`-MCP oder dem lokalen Chrome; bei Artifacts der gerenderte Zustand.

## Ablauf

### 1. Mechanische Pre-Flight (billig, zuerst)
`design_lint.py` über die geänderten UI-Dateien laufen, dann `visual-preflight.md` Box für Box.
Jede rote Box ist ein Finding mit Datei/Ort + der Alternative aus `craft-floor.md`. Kein „sieht gut aus"-Wischiwaschi.

### 2. Batched-Verifikation (nicht in einer Schleife)
Die Decke deckt den ganzen Zyklus, nicht jede Mikro-Edit: **voll bauen → EINMAL inspizieren in einer
gebatchten Runde (Desktop UND Mobile zusammen, ein Render) → alles was sie zeigt in EINEM Batch fixen →
mit höchstens EINER weiteren Runde bestätigen → aufhören zu polieren.** Open-ended Self-QA verbrennt Budget.

### 2b. 5-Dim-Selbstkritik (Hausmethode)
Zusätzlich zur mechanischen Pre-Flight die benannte 5-Dim-Selbstkritik durchlaufen (Memory
`reference-design-5dim-selfcritique`) — pro Dimension: passt es zum Kontext, was ist die konkrete Schwäche, ein Fix:
Hierarchie&Fokus · Typografie&Rhythmus · Farbe&Kontrast · Raum&Dichte · Konsistenz&Detail. Kein „fertig", bevor jede
Dimension einmal kritisch lief und der schwächste Punkt gefixt ist.

### 3. Adversariale Linse (das echte Härten)
Frag aktiv gegen das Design:
- Sieht *irgendein* Element wie ein AI-Default aus (Purple-Mesh-Hero, 3 gleiche Cards, Glass-Deko, Inter+slate-900)?
- Was ist der **eine** Grund, warum diese Seite auffällt — und hält der einer skeptischen Zweitmeinung stand?
- Chain-Frage: gibt es *einen* mutigen Move (Typo-Moment, Bild, Motion-Beat), der sie von „solide" auf „einprägsam" hebt?
- Ist die committete Welt konsequent durchgezogen, oder ist es Politur auf einem Default?

### 4. Redesign-Modus (falls zutreffend, audit-first)
Modus erkennen (Greenfield / Redesign-Preserve / Redesign-Overhaul), bei Mehrdeutigkeit **einmal** fragen.
**Vor dem Anfassen auditieren:** Brand-Tokens, IA, Content-Blöcke, zu-bewahrende vs. zu-entfernende Muster,
die *bestehenden* Dial-Werte als Startpunkt ableiten, **SEO-Baseline** (SEO-Migration = #1-Redesign-Risiko).
Was ändert sich **nie still:** URLs, Nav-Labels, Formularfeld-Namen, Logo, Legal/Cookie-Copy, Analytics-Events.
Modernisierungs-Hebel in Prioritätsreihenfolge: Typografie → Spacing → Farbe → Motion → Hero-Rekomposition → Block-Ersatz.

## Output
Findings zuerst berichten (Ort + Regel + Fix), dann — nur wenn der User Auto-Fix will — in einem Batch anwenden.
Verdict je Finding: BLOCK / FIX / OK. Kein „fertig" solange eine BLOCK-Box offen ist.

## Hard-Gates (Abschluss)
- **read-only-first:** erst inspizieren/berichten, dann (auf OK) fixen. Findings sind reviewbare Artefakte, kein Auto-Fix-Trigger.
- Batched-Verify statt endloser Schleife (Budget-Disziplin).
- Ehrlich über das, was nur am Auge/Gerät entscheidbar ist — nicht glattbügeln.

*Synthese aus impeccable (Batched-Verify, Redesign-Audit) + taste-skill (Pre-Flight) + emil (review-animations). Credits: `CREDITS.md`.*
