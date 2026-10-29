---
description: Static-Sweep (MakerChecker mc-scan portiert) fuer UNGESCHUETZTE konsequenzielle Aktionen im EIGENEN Code (.py/.js) — Code-Exec (eval/exec), Shell-Injection (os.system/shell=True), Datei-Loeschung, destruktives Git — die keinen Guard (dry-run/confirm/force-check/temp-Pfad/kill-switch) tragen. Deny-by-default aufs eigene Arsenal. Read-only, advisory, aendert nichts. Detektor-/Guard-Dateien per Denylist ausgeschlossen. Trigger "/mc-scan", "ungeschuetzte aktionen im code", "unguarded consequential", "mc scan", "code audit gefaehrliche ops".
allowed-tools: Bash
argument-hint: "[pfad ...] [--top N] [--strict] [--json]"
---

# /mc-scan — ungeschuetzte konsequenzielle Aktionen im eigenen Code

Findet gefaehrliche Operationen ohne Gate in UNSEREM Code. Empfiehlt, aendert nichts.

## Lauf

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mc_scan.py $ARGUMENTS
```

## Kategorien
- **code-exec** (HIGH) — `eval(`/`exec(` (bare, nicht `.eval()`).
- **shell-injection** (HIGH) — `os.system`/`subprocess(..., shell=True)`/`os.popen`/`child_process.exec`.
- **file-deletion** (MED) — `rmtree`/`os.remove`/`.unlink`/`rm -rf`.
- **destructive-git** (MED) — force-push/`reset --hard`/`clean -fd`.

## Hard-Gate
⚠️ Dieses Tool macht viele subprocess/curl-Aufrufe by design — das ist legitim. Fund = SELBST-Gefahr
ohne Guard = **REVIEW**, nicht Kill. Guard erkannt bei: dry-run/confirm/force-check/temp-Pfad/kill-switch/test-Datei.
String-Literale/Regex/Detektor-Dateien (Muster=Daten) werden ausgeschlossen. HITL entscheidet. Ergaenzt
`skill_promote_gate.py` (das Skill/Agent-.md prueft; mc-scan prueft .py/.js-CODE).
