---
name: skill-harden
description: >-
  Die fehlende 3. Saeule des Skill-Lifecycles — haertet einen BESTEHENDEN Skill
  aus ECHTEN Outcomes (nicht create, nicht import, nicht audit). Behandelt die
  SKILL.md als trainierbaren Zustand: ein bounded add/delete/replace-Edit wird nur
  akzeptiert, wenn er auf held-out-Faellen anytime-valid besser ist — via PACE-
  e-process (testing-by-betting), NICHT dem naiven "iff besser" (das p-hackt sich
  selbst). Kandidaten aus einem eigenen Gap-Tracking (wiederholtes Scheitern/fehlende Faehigkeit)
  oder gemeldeter Schwaeche; HITL vor Commit. CREATE→/skill-forge,
  AUDIT→/skill-doctor, RELEASE→/skill-promote.
  Trigger "/skill-harden <skill>", "skill haerten <name>", "skill aus outcomes verbessern",
  "harden existing skill", "skill-schwaeche fixen <name>".
allowed-tools: Bash, Read, Edit, Grep, Glob
---

# /skill-harden — bestehenden Skill aus echten Outcomes haerten (3. Saeule)

> Prinzip: ein Skill wird nicht durch Bauchgefuehl besser, sondern durch einen Edit, der auf
> held-out-Faellen **anytime-valid** gewinnt. Der Agent darf sich NICHT selbst p-hacken.

## Wann laden
Ein bestehender Skill scheitert wiederholt an derselben Klasse, oder dein eigenes
Gap-Tracking flaggt ihn, oder du meldest eine Schwaeche.
Abgrenzung: CREATE→`/skill-forge` · IMPORT→`/skill-scout` · AUDIT/rightsize→`/skill-doctor` · RELEASE→`/skill-promote`.

## PHASE 0 — Kandidat + Baseline
- Ziel-Skill lesen. Belege sammeln: die konkreten Faelle, in denen er scheiterte (aus eigenem
  Gap-Tracking, Session-Verlauf, oder vom User). Diese werden der **held-out-Satz** — echte Outcomes, nicht erfunden.
- Formuliere die Schwaeche als testbare Klasse ("Skill X uebersieht Fall-Typ Y").

## PHASE 1 — Bounded Edit (genau EINER)
- Schlage GENAU einen begrenzten Edit vor: **add** (eine Regel/Referenz) · **delete** (eine tote/schaedliche Zeile) ·
  **replace** (eine Formulierung). Unbounded Umbau = reject-buffer (kein kontrollierter Test moeglich).
- Alt-Version (Ist) und Neu-Version (mit Edit) bereithalten.

## PHASE 2 — Held-out-Paare (old vs new)
- Fuer JEDEN held-out-Fall: wie verhaelt sich der Skill ALT vs NEU? Ergebnis je Fall als Paar `[old_ok, new_ok]`
  (bool: hat er den Fall korrekt behandelt?) — oder Score `[old_score, new_score]`. NIE am selben Satz "tunen und
  wieder messen" (das ist das p-hacking, das PACE verhindert).

## PHASE 2b — Scorer-loser Branch (SkillAudit, #7) — für Skills OHNE binäres Pass/Fail
Recon/OSINT/dork-sweep u.ä. haben keinen automatischen Score → PHASE 2 nicht anwendbar. Stattdessen:
- Dieselbe repräsentative Aufgabe **mit** und **ohne** den Edit laufen (paired trajectory); die Divergenz IST das Signal.
- Ein Judge urteilt je Paar drei-wege `helped/hurt/inert` entlang der Linsen: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/skill_audit.py --lenses`
  (correctness · completeness · efficiency · no-regression · hallucination).
- Verschiedene **Task-Klassen** abdecken (nicht 7× denselben Fall) — sonst greift der RSEA-Filter.
- Aggregieren: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/skill_audit.py '[{"verdict":"helped","task_class":"x"}, …]'`
  → mappt auf denselben PACE-Gate (helped=neu-gewinnt), PLUS RSEA: **ACCEPT nur mit ≥2 helped-Klassen** (sonst
  `NEEDS-BROADER-COVERAGE` = single-benchmark-win, unbewiesen). Ergebnis fließt wie PHASE 3.

## PHASE 3 — PACE-Akzeptanz-Gate (Pflicht — nicht das naive `>`)
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/skill_harden_gate.py '[[old,new],[old,new],...]'
```
- **ACCEPT** (E_new ≥ 1/alpha): der Edit ist anytime-valid besser → weiter zu PHASE 4.
- **REJECT**: neu schlechter ODER genug getestet ohne Signal → **reject-buffer** (Edit NICHT anwenden; notieren).
- **CONTINUE**: mehr held-out-Faelle noetig → sammeln, erneut. NIE bei CONTINUE/REJECT trotzdem committen.

## PHASE 4 — HITL + Regression
- Nur bei ACCEPT: Edit anwenden (`Edit`), dann `validate_skills.py` (0 ERROR) + `skill_promote_gate.py <skill>`
  (Red-Team) + `skill_doctor.py` (kein neuer Rightsizing-Fund). **User bestaetigt** vor Commit (kein Auto-Commit).
- Bug-class→patch-Schleife: der held-out-Beleg wandert als Lehre in die Skill/Memory.

## Hard-Gates (Abschluss)
- **PACE-Gate ist Pflicht** — kein "sieht besser aus"-Commit; kein naives `>` (Selbst-p-hacking).
- **held-out ≠ Tuning-Satz** — nie am selben Satz optimieren und akzeptieren.
- **read-only-first · HITL vor Commit · Reject→reject-buffer.**
- Ehrlich: SkillOpts +19–24pp sind Frontier-Modell-Zahlen — der Wert ist der MECHANISMUS (kontrollierte Akzeptanz),
  nicht die Zahl.
- **MAGE-Caveat (#7):** held-out-Gate (PHASE 3) + scorer-loser Audit (PHASE 2b) interagieren nicht-additiv —
  beim Ändern der Loop EINZELN ablatieren, nicht blind stapeln. **RSEA:** ein Win nur auf der einen Klasse, für die
  der Edit gebaut wurde, ist unbewiesen (→ NEEDS-BROADER-COVERAGE).
