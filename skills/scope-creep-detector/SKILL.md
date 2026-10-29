---
name: scope-creep-detector
description: >-
  Prüft einen Git-Diff (working tree, staged, Branch-vs-Base oder gespeicherte
  Diff-Datei) gegen eine erklärte Ein-Satz-Absicht und erkennt Scope-Creep:
  unrelated Files, neue Dependencies, öffentliche API-Renames, Config-/CI-Edits,
  überdimensionierte Hunks, reine Formatierungs-Änderungen. Gibt pro auffälliger
  Datei eine Keep/Split/Justify-Empfehlung. Rein lokal (git-Aufrufe), kein
  Netzwerk, kein Repo-Write. Macht die CLAUDE.md-Kernregel "chirurgische
  Änderungen, kein Drive-by-Refactor" automatisiert prüfbar statt nur Prinzip —
  nutzen VOR jedem `git add`/Commit/PR bei einer nicht-trivialen Änderung, und
  immer wenn `/code-review`/`/simplify` einen zu breiten Diff moniert.
  Trigger "scope creep check", "ist dieser diff zu breit", "pr scope prüfen",
  "hab ich mehr angefasst als nötig", "/scope-creep-detector".
---

# scope-creep-detector — Diff gegen erklärte Absicht prüfen

> Rolle: nüchterner Diff-Prüfer. Der Klassifikator liefert **Triage-Evidenz**,
> keinen Beweis für Autorenabsicht — die Keep/Split/Justify-Bewertung bleibt
> Urteilssache und gehört in den Bericht, nicht ins Skript.

## Wann laden
Vor jedem Commit/PR einer nicht-trivialen Änderung, oder wenn der User fragt
"ist der Diff zu breit" / "hab ich zu viel angefasst". Ergänzt `/code-review`
und `/simplify` (die auf Bugs/Cleanup prüfen, nicht auf Scope-Treue).

## Eingabe
Eine Ein-Satz-Absicht (`--intent "fix null dereference in parser"`) — konkret,
nicht generisch. Ohne Absicht fällt das Skript auf den Branch-Namen zurück;
ist der generisch/detached, erst nach der Absicht fragen, bevor Relatedness
bewertet wird.

## Werkzeug
```bash
python3 scripts/scope_creep.py --repo /pfad/zum/repo \
  --intent "fix null dereference in parser" --json
```
Varianten: `--staged` (Staged-Diff), `--base main` (Branch-vs-Merge-Base),
`--diff datei.diff` oder `--diff -` (stdin, z. B. `git diff --staged | … --diff -`).
`--hunk-threshold` nur mit dokumentiertem Grund ändern — nie nur um eine Warnung
verschwinden zu lassen.

## PHASE 1 — JSON interpretieren
Vor jeder Empfehlung `references/scope-signals.md` lesen (Signal-Definitionen,
Schwellwerte, Grenzen). Felder: `in_scope` (Pfad/Intent-Overlap) ·
`likely_creep` (kein Overlap + Signal) · `new_deps` · `api_renames` ·
`config_edits` · `stats` (Churn, Subsystem-Anzahl, übergroße Hunks,
Formatierungs-only-Files). Ein leeres Array ist auch ein Ergebnis — "kein
Signal erkannt" sagen, nicht "Diff ist garantiert im Scope".

## PHASE 2 — Keep/Split/Justify je Eintrag in `likely_creep`
1. **Keep** — Pfad ist für die Absicht nötig, Verbindung ist direkt (1 Satz
   Begründung).
2. **Split** — kann unabhängig landen, gehört zu anderem Subsystem, oder bringt
   eine nicht nötige Dependency/API-Rename/Config-Edit/großen Hunk mit. Dateien/
   Hunks für die Folge-Änderung benennen.
3. **Justify** — cross-cutting Edit lässt sich nicht sicher trennen. Das
   Invariant/den Build-Constraint benennen, der es erzwingt, plus Reviewer-Risiko.

Bei Unklarheit eher **Split** empfehlen. Ein Overlap-Score von 0 beweist nicht,
dass eine Datei unrelated ist — Pfad-Vokabular ist ein billiger, deterministischer
Proxy, kein Urteil.

## PHASE 3 — Bericht
1. Absicht + Diff-Quelle
2. Berührte Dateien/Subsysteme, Additions/Deletions gesamt
3. In-Scope-Änderungen
4. Likely-Creep mit Signal-Beleg
5. Keep/Split/Justify-Tabelle
6. Vorschlag für Folge-Gruppierung (falls sinnvoll)

Datei-Pfade und Hunk-Header konkret benennen. Bei einem übergroßen gemischten
Hunk: das Skript kann ihn nicht automatisch splitten — den kleinsten kohärenten
Einzel-Edit beschreiben. **Vor jedem Split/Revert/Staging/Commit erst fragen.**

## Hard-Gates
- read-only-first — das Skript ändert nie Working-Tree/Index/Commits/Branches.
- Kein automatischer Split/Revert/Commit ohne explizites User-OK.
- Klassifikator = Evidenz, nicht Beweis — Formulierung entsprechend vorsichtig.

## Herkunft
Adaptiert (unverändert kopiert, siehe `CREDITS.md`) aus
`Shubhamsaboo/awesome-llm-apps/agent_skills/scope-creep-detector`, sandbox-
geprüft 🟢 SAFE-ADOPT (2026-08-21, nur dieser Unterordner — nicht das Gesamt-Repo).
