---
name: commit-archaeologist
description: >-
  Rekonstruiert aus lokaler Git-Historie, warum ein Code-Block oder eine Datei
  existiert: einführender Commit, spätere Änderungen, aktuelle Autoren (Blame
  getrennt von Historie), wiederkehrend mitgeänderte Companion-Files, und
  Intent-Hinweise aus Commit-Messages (Issue-Referenzen, Reverts, Workarounds,
  "temporary"/unfertige Marker). Rein lokal (git-Aufrufe), kein Netzwerk, kein
  Repo-Write. Nutzen VOR einem Rewrite/Refactor/riskanten Edit an fremdem oder
  altem Code, oder wenn die Frage "warum existiert das so" auftaucht — `git
  blame` nennt nur den letzten Autor, dieser Skill rekonstruiert den Grund.
  Trigger "warum existiert dieser code", "git archaeology", "commit geschichte
  erklären", "wer hat das eingeführt und warum", "/commit-archaeologist".
---

# commit-archaeologist — warum existiert dieser Code

> Rolle: Historiker, kein Orakel. Blame-Ownership ist kein Beweis für
> ursprüngliche Autorenschaft; wiederholtes Mitändern legt Kopplung nahe,
> beweist aber keine Abhängigkeit. Jede Schlussfolgerung über die reinen
> Fakten hinaus explizit als Inferenz kennzeichnen.

## Wann laden
Vor einem Rewrite/Refactor an unbekanntem/altem Code in diesem Repo, oder wenn
die Frage auftaucht, warum ein Workaround/eine ungewöhnliche Design-Entscheidung
so steht wie sie steht — als Vorstufe zu einem Source-Auditor/`/code-review`,
nicht als Ersatz dafür.

## Eingabe
Repo-Pfad + getrackter Dateipfad, optional eine Zeilen-Range für einen
aktuellen Block. Nur die fehlenden Werte nachfragen. Pfade relativ zum Repo,
Forward-Slashes. Keine Sibling-Repos scannen.

## Werkzeug
```bash
python3 scripts/archaeologist.py /pfad/zum/repo src/cache.py --lines 40-72 --json
```
Ohne `--lines`: komplette Datei-Historie. Mit Range: `git log -L` (Line-Log);
ohne Range: Datei-Historie mit Rename-Following. Read-only — bei ungültigem
Pfad/Range den Fehler melden und korrigierten Zielwert erfragen.

## PHASE 1 — JSON interpretieren
Vor der Interpretation `references/reading-git-history.md` lesen (Confidence-
Regeln gegen Blame-Ownership/Korrelations-/Message-Fehlschlüsse). Felder:
`region` (normalisierte Pfade/Modus/Range) · `introduced_by` (ältester Commit
der gewählten Historie) · `timeline` (chronologisch, Kategorie + geänderte
Dateien + erkannte Renames) · `co_changed` (Companion-Files ab Schwellwert) ·
`authors` (aktuelle Blame-Zeilen getrennt von historischer Commit-Zahl) ·
`intent_signals` (Issue-Refs, Reverts, Workarounds, "temporary"/unfertig-Marker).
Eine leere Signal-Liste heißt: die Messages sagen nichts — nicht, dass es
keinen Grund gab.

## PHASE 2 — Bericht "warum existiert das"
1. **Fazit zuerst** — 1-2 Sätze wahrscheinlichste Erklärung + Confidence-Label
   (hoch/mittel/niedrig).
2. **Ursprung** — Hash (kurz, aber eindeutig), Datum, Autor, Subject, Nachbar-
   Dateien, die den ursprünglichen Zweck klarer machen.
3. **Timeline** — chronologisch, mechanische Edits gruppieren, Reverts/Fixes/
   Workarounds aber einzeln erhalten.
4. **Companion-Files** — wiederholtes Mitändern als Kopplungs-Hinweis; eine
   einmalige Mitänderung nicht als Abhängigkeit werten.
5. **Intent-Evidenz** — kurze Commit-Subjects/Signalwörter zitieren; alles
   darüber Hinausgehende explizit als Inferenz kennzeichnen.
6. **Änderungsrisiko** — Constraints, Companion-Files und ungelöste "temporary"-
   Entscheidungen benennen, die vor einem Edit zu prüfen sind.

Volles JSON nur auf Nachfrage dumpen.

## Evidenz-Regeln
- Aktuelle Blame-Ownership ≠ ursprüngliche Autorenschaft.
- Der älteste gewählte Commit ist die Einführung der REGION, nicht zwingend der
  ersten Commit der Datei.
- Wiederholtes Mitändern legt Kopplung nahe, beweist keine Abhängigkeit.
- Commit-Kategorien sind Message-Heuristiken, keine verifizierten Issue-Typen.
- "Temporary"/"Workaround" sind starke Hinweise, aber nur der Message-Autor
  oder eine verlinkte Diskussion kann bestätigen, ob der Constraint noch gilt.
- Bei dünner Historie/vagen Messages: "die Historie zeigt"/"vermutlich" statt
  eine Design-Begründung zu erfinden.

## Hard-Gates
- read-only-first — das Skript ändert nie Working-Tree/Index/Commits/Branches.
- Code erst nach expliziter User-Nachfrage anfassen, nie im selben Zug wie
  die Archäologie.

## Herkunft
Adaptiert (unverändert kopiert, siehe `CREDITS.md`) aus
`Shubhamsaboo/awesome-llm-apps/agent_skills/commit-archaeologist`, sandbox-
geprüft 🟢 SAFE-ADOPT (2026-08-21, nur dieser Unterordner — nicht das Gesamt-Repo).
