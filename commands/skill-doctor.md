---
description: Advisory Rightsizing-Audit der Skill-Library gegen die 6 Claude-5 Context-Engineering-Shifts. Rankt Skills als KANDIDATEN fürs Kürzen/Splitten mit sichtbarer Evidenz (LONG_NO_REFS, EXAMPLE_HEAVY, RULE_DENSE, REPETITION, DESC_BLOAT) + Token-Budget. Read-only, blockt NIE, ändert nichts. Kein Auto-Trim — Eval-Neutralität je Skill selbst prüfen. Abgrenzung — das Hard-Gate ist validate_skills.py. Trigger "/skill-doctor", "rightsize skills", "welche skills sind zu lang", "skill audit".
allowed-tools: Bash
argument-hint: "[--top N] [--json] [--commands]"
---

# /skill-doctor — Rightsizing-Audit (advisory)

Rankt die Skill-Library gegen die 6 Context-Engineering-Shifts für Claude-5. Empfiehlt, entscheidet nichts.

## Lauf

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/skill_doctor.py $ARGUMENTS
```

## Was du siehst
- Library-Footprint (Token, on-demand) + Anzahl Skills mit Findings.
- Top-N Kandidaten, gerankt nach Priorität, je Fund mit **roher Evidenz** und Punkten.
- Codes: `LONG_NO_REFS` (splitten → references/) · `OVER_BODY_BUDGET` (>500 Z.) · `EXAMPLE_HEAVY`
  (Interface-Design statt Beispiel-Wand) · `RULE_DENSE` (Urteil zulassen) · `REPETITION` · `DESC_BLOAT`.

## Hard-Gate
⚠️ KANDIDATEN, keine Anweisung. Vor dem Kürzen eines Skills Eval-Neutralität selbst prüfen (die „>80%
gekürzt"-Zahl ist Claude-5-kalibriert — nicht cargo-culten).
Compliance-Gate (Pass/Fail): `${CLAUDE_PLUGIN_ROOT}/scripts/skills/validate_skills.py`.
