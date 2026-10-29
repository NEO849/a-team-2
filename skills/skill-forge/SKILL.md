---
name: skill-forge
description: >
  Katalog→Skill-Fabrik mit Dedup-Gate — verwandelt eine Skill-IDEE (aus einem Prompt-Katalog,
  einem Marktplatz-Fund oder einem eigenen Bedarf) in einen spec-konformen SKILL.md-Entwurf,
  ABER erst nachdem ein Dedup-Gate geprüft hat, dass wir die Fähigkeit nicht schon haben. Kern-Regel:
  ein Arsenal wird nicht durch MEHR Skills besser, sondern durch gemessen-fehlende — jeder redundante
  Trigger verwässert das Routing (Description-Budget, Kollision). Läuft: Dedup-Check (Containment gegen
  alle bestehenden Skills) → nur bei 🟢/🟡 weiter → Entwurf nach eigenem Autoren-Standard → Linter grün →
  Two-Claude-Loop. Für das Vetten von Fremdcode/Drittanbieter-Skills braucht es ein separates
  Sandbox-/Vetting-Verfahren — hier nicht enthalten.
  Trigger "/skill-forge <idee>", "skill bauen für <x>", "katalog adoptieren <x>", "lohnt sich ein skill für <x>",
  "dedup-check <idee>".
---

# skill-forge — nur gemessen-fehlende Skills anlegen

> Rolle: Skill-Kurator mit Anti-Wildwuchs-Disziplin. Ziel: das Arsenal *scharf* halten. Ein Katalog
> mit 80 Einzeiler-Prompts ist kein Upgrade — er ist Input für ein Gate, das nur echte Lücken schließt.

## Wann laden
Immer wenn eine Skill-Idee auftaucht (Prompt-Katalog, Marktplatz, „bau doch einen Skill für X") — VOR
dem Anlegen. Verhindert Duplikate von `mkt-akquise`/`humanize`/`entscheiden` etc. und Routing-Verwässerung.

## Eingabe
Die Skill-Idee als Text: geplante Description + geplante Trigger-Phrasen (oder mind. Thema + 2-3 Trigger).
Je konkreter, desto schärfer das Dedup-Urteil.

## Werkzeug (Skript zuerst — deterministisch)
**Führe aus:** `python3 ${CLAUDE_SKILL_DIR}/scripts/dedup_check.py "<idee + trigger>"`
(oder `--file <p>` / `-` für stdin). Gibt ein Verdikt + Top-5-ähnlichste Skills (Containment-Score):
- **🔴 BLOCK (≥0.55)** → NICHT neu anlegen. Den genannten bestehenden Skill *erweitern* (references/Body),
  nicht duplizieren. Ende.
- **🟡 PRÜFEN (0.35–0.55)** → Grenzfall. Nur weiter, wenn du die Abgrenzung in EINEM Satz sagen kannst;
  dann Description-Abgrenzung + Scope-Cross-Link (`für X siehe /anderer-skill`) zwingend setzen.
- **🟢 FREI (<0.35)** → echte Lücke, weiter zum Entwurf.

## PHASE 1 — Dedup-Gate (Pflicht, zuerst)
Skript laufen lassen. Bei 🔴 hier stoppen und dem User den bestehenden Skill nennen (+ was ihm ggf. fehlt,
als Erweiterungs-Vorschlag). Kein Entwurf hinter einem BLOCK.

## PHASE 2 — Entwurf nach Standard
Erst jetzt SKILL.md schreiben, strikt nach deinem eigenen Autoren-Standard (lege einen an, falls noch
keiner existiert):
- `name` == Verzeichnis, `^[a-z0-9-]+$`, Verb-Substantiv, keine Reserved-Words (`claude`/`anthropic`).
- `description` **≤1024 Zeichen**: Haupt-Use-Case (was+wann) zuerst → Abgrenzung/Cross-Links → 3-5 Trigger
  als wörtliche Zitate am Ende. Keine Methodik-Prosa in der Description.
- Body **<500 Zeilen**: Rollen-Blockquote → `## Wann laden` → `## Eingabe` → `## Werkzeug` →
  `## PHASE 0..N` → `## Hard-Gates`. Schwere Matrizen in eine eigene Referenz-Datei auslagern (eine Ebene tief).
- Deterministische Arbeit → Skript (kostet keinen Kontext), nicht Prosa.
- Hard-Gates-Keywords inline (read-only-first, kein Submit/Commit ohne User-OK).
- Autonom triggern: braucht der neue Skill Auto-Routing ohne Tippen → prüfe, ob dein Setup eine eigene
  Intent-Routing-Konfiguration hat, und ergänze sie dort (sonst greift nur Description-Matching).
- **Falls dein Setup einen Capability-Manifest/Index führt:** nach dem Anlegen aktualisieren, damit der
  neue Skill dort bekannt ist.

## PHASE 3 — Härten vor „fertig"
- **Fremdcode?** Enthält die Idee ein fremdes Tool/Repo/Skript → ZUERST in einer isolierten Sandbox
  (Statik + optional Detonation) vetten, bevor irgendetwas davon in den Skill wandert. Untrusted-Code
  nie blind übernehmen.
- **Linter:** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/validate_skills.py` MUSS 0 ERROR sein.
- **Promote-Gate (Shadow + Red-Team, Pflicht vor Freigabe eigener Skills/Agenten):**
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/skills/skill_promote_gate.py <name>` — bündelt Compliance + Rightsizing +
  statischen Red-Team-Scan (Injection-Fläche, Outward-Initiation, ungated Submit, Broad-Grant, Secret-Output).
  **HOLD = nicht freigeben**, erst fixen. Für High-Privilege-Agenten (exec/outward) zusätzlich ein
  unabhängiges Deep-Review durch einen adversarial-skeptischen Reviewer + Shadow-Dry-Run
  (`disable-model-invocation:true`, an ≥2 Fällen beobachten) BEVOR die Auto-Invocation frei ist.
- **Bug-class→Skill-Patch (geschlossene Schleife):** findet der Shadow-Run/Review eine Lücke → als Fix
  zurück in den Skill bzw. dein Projekt-Setup, nicht nur als Notiz irgendwo verloren gehen lassen.
- **Ships der Skill CODE (.py/.js)?** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/mc_scan.py <pfad>` — findet ungeschützte
  konsequenzielle Ops (eval/exec, shell=True, Datei-Löschung, destruktives Git). HIGH-Funde vor Freigabe gaten.
- **Two-Claude-Loop:** Ein Fresh-Context muss (a) aus der gekürzten Description korrekt triggern UND
  (b) die Aufgabe allein aus der dünnen SKILL.md lösen. Sonst nachschärfen.

## Hard-Gates (Abschluss)
- **read-only-first**: Dedup + Entwurf sind lokale Artefakte; kein Commit/Install ohne User-OK.
- **Kein BLOCK-Override ohne begründete Abgrenzung** — 🔴 heißt erweitern, nicht duplizieren
  (erst kontrollieren, ob die Fähigkeit schon existiert, bevor neu angelegt wird).
- **Fremdcode nie ohne isoliertes Vetting.** Kein Auto-Install/Commit ohne User-OK.
