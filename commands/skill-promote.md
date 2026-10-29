---
description: Shadow-Mode + Red-Team-Gate VOR Freigabe eines EIGENEN neuen Skills/Agenten (die SDLC-Lücke für eigene neue Skills; externe Tools werden separat geprüft). Bündelt Compliance (validate_skills) + Rightsizing (skill_doctor) + statischen Red-Team-Scan (Injection-Fläche, Outward-Initiation, ungated Submit, Broad-Tool-Grant, Secret-Output) → Verdict PROMOTE/HOLD + manuelle Checkliste (Shadow-Dry-Run, Deep-Review). Read-only, ändert nichts. Trigger "/skill-promote <name>", "promote skill", "red-team meinen skill", "darf der skill live", "shadow gate <agent>".
allowed-tools: Bash
argument-hint: "<skill-/agent-/command-name oder pfad> [--strict] [--json]"
---

# /skill-promote — Pre-Promotion Shadow/Red-Team-Gate

Prüft ein EIGENES neues Skill/Agent/Command VOR der Freigabe. Empfiehlt, ändert nichts.

## Lauf

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/skill_promote_gate.py $ARGUMENTS
```

## Verdict
- 🟢 **PROMOTE** — sauber. · 🟡 **PROMOTE-WITH-NOTES** — WARNs, prüfen. · 🛑 **HOLD** — BLOCK/ERROR, erst fixen.
- Red-Team-Codes: `INJECTION_SURFACE` (folgt untrusted Instruktionen = BLOCK) · `OUTWARD_INITIATION` ·
  `AUTO_SUBMIT_UNGATED` · `BROAD_TOOL_GRANT` · `SECRET_OUTPUT` · `MISSING_HARDGATES`.

## Hard-Gate
HOLD = **nicht freigeben**. Für High-Privilege-Agenten (exec/outward) zusätzlich ein unabhängiges
Deep-Review durch einen adversarial-skeptischen Reviewer + Shadow-Dry-Run
(`disable-model-invocation:true`, ≥2 Fälle) vor Auto-Invocation.
Dieses Gate prüft EIGENEN Code; für das Vetten von FREMDEM/Drittanbieter-Code braucht es ein
separates Sandbox-/Vetting-Verfahren.
