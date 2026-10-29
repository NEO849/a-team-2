#!/usr/bin/env python3
"""
skill_promote_gate.py — Shadow-Mode + Red-Team-Gate VOR dem Promoten EIGENER Skills/Agenten.

PORT von Anthropics AI-native SDLC (Blog 2026-07-21): shadow-mode + red-teaming für neue Agenten VOR
Full-Release. Lücke: externe Tools werden separat geprüft — für eigene neue Skills/Agenten gab es
nur `validate_skills.py` (Compliance) + Two-Claude-Loop. Dieses Gate ergänzt den Red-Team-Layer.

Bündelt: (a) validate_skills.py [Compliance] · (b) skill_doctor.py [Rightsizing] ·
(c) STATISCHER RED-TEAM-SCAN (bilingual, whole-dir inkl. references/+scripts/, Proximity-Gates) ·
(d) Manuelle Checkliste (Shadow-Dry-Run, Deep-Review High-Privilege).

⚠️ EHRLICHKEIT: statisches Scannen von NL-Markdown ist prinzipiell umgehbar (Synonyme/Obfuskation). Dieses
Gate ist die deterministische ERSTE Linie + Zwang zur Checkliste — KEIN Beweis der Sicherheit. Die echte
Absicherung High-Privilege-Artefakte ist die gelistete Deep-Review (adversarial reviewer/Red-Team) + Shadow-Run.
Der Scan zielt auf SELBST-Gefahr (folgt untrusted Instruktionen / exfiltriert / destruktiv / ungated outward),
NICHT auf „Agent erwähnt Angriffstechnik".

Verdict: HOLD bei ≥1 BLOCK oder validate-ERROR; sonst PROMOTE (Notes bei WARN).
Read-only, stdlib-only. Default exit 0 (advisory); `--strict` → exit 1 bei HOLD.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
SKILLS_DIR = HOME / ".claude" / "skills"
AGENTS_DIR = HOME / ".claude" / "agents"
COMMANDS_DIR = HOME / ".claude" / "commands"
VALIDATE = HOME / ".claude" / "scripts" / "skills" / "validate_skills.py"
DOCTOR = HOME / ".claude" / "scripts" / "skills" / "skill_doctor.py"

SIDE_EFFECT_TOOLS = {"bash", "write", "edit", "notebookedit"}
FETCH_TOOLS = {"webfetch", "websearch", "firecrawl", "fetch"}
MAX_SUBFILE = 200_000
MAX_SUBFILES = 60

# Proximity-Wörter (NAHE am Treffer prüfen, nicht „irgendwo im Body")
GATE_WORDS = re.compile(r"user[- ]?ok|freigab|\bdraft\b|entwurf|confirm|bestätig|review|"
                        r"_shared/hard-gates|read-only|nur nach|mit ok|explizit erlaub", re.I)
NEG_ADJ = re.compile(r"\b(never|nie|niemals|redact|redigier|do not|don'?t|kein|ohne)\b", re.I)

# Bilinguale Selbst-Gefahr-Muster (EN+DE). Nur UNZWEIDEUTIGE Gefahr ist BLOCK — kontextabhängige
# (Secret/Outward/Submit) bleibt WARN, weil in Security-Tools legitim (sonst FP-Explosion).
# INJECTION nutzt OBEY-Verben (nicht Prozess-Verben wie extract/analyze) + STARK-externe Quelle.
_OBEY = (r"follow|obey|comply|execute|carry out|act on|honou?r|do what|do whatever|"
         r"befolge|folge\b|führe .{0,15}aus|umsetze|beachte .{0,10}anweis")
_EXT_SRC = (r"fetched|scraped|downloaded|untrusted|user-supplied|the fetched|abgerufen\w*|"
            r"eingelesen\w*|externen inhalt|geladenen inhalt|response body|the web page|the scraped")
_INJ_A = re.compile(
    rf"\b({_OBEY})\b.{{0,120}}"
    r"\b(instruction|command|directive|anweisung|befehl|weisung|inhalt|content)\w*\b.{0,120}"
    r"\b(from|in|within|contained|gemäß|laut|aus (der|dem)|von (der|dem))\b.{0,80}"
    rf"\b({_EXT_SRC})\b", re.I | re.S)
# Path B: starkes Obey-Signal (gemäß/laut/entsprechend/according|based) + externe Quelle nah beieinander.
_INJ_B = re.compile(
    rf"\b(gemäß|laut|entsprechend|according to|based on|as per|per the)\b.{{0,40}}"
    rf"\b({_EXT_SRC})\b|\b({_OBEY})\b.{{0,40}}\b({_EXT_SRC})\b", re.I | re.S)
_DESTRUCT = re.compile(
    r"rm\s+-rf?\s+(~/?\*|/\*|~(?![\w/])|/(?![\w])|\$HOME\b)"     # rm -rf auf BARE home-dir bzw. filesystem-root * (nicht ~/spez/pfad)
    r"|rm\s+-rf?\s+~?/?\.(ssh|aws|gnupg)\b"                      # rm der Credential-Dirs
    r"|:\(\)\s*\{\s*:\s*\|\s*:"                                  # fork bomb
    r"|chmod\s+-R\s+0?777\s+/"
    r"|dd\s+[^\n]*of=/dev/sd|>\s*/dev/sd"                        # WRITE auf Rohdatenträger = wipe (dd if= = imaging, ok)
    r"|base64\s+(-d|--decode)[^\n]*\|\s*(ba)?sh"                 # obfuskiert→shell
    r"|(python3?|perl|ruby)\s+-c[^\n]*base64|exec\([^)]*base64|os\.system\([^)]*base64"  # obfuskiert→exec
    r"|curl\s[^\n|]*\|\s*(ba)?sh|wget\s[^\n|]*\|\s*(ba)?sh"      # pipe-to-shell
    r"|eval\([^)]*base64", re.I)
_SECRET = re.compile(
    r"\b(echo|print|output|reveal|leak|dump|display|paste|send|post|exfil\w*|"
    r"gib|verschick\w*|sende|übermittle|maile|weiterleite)\b[^\n]{0,25}"
    r"\b(secret|token|password|passwort|api[_-]?key|credential|zugangsschl\w*|"
    r"private[_-]?key|\.env|/\.aws|/\.ssh)\w*\b", re.I)
_OUTWARD = re.compile(
    r"\b(send_mail|mailbox_send|create_draft|send[_ ]?message|slack|tweet|"
    r"push_notification|notify\w*|post to|webhook|discord|sendmail|maile|verschick\w*|poste)\b|"
    r"curl[^\n]*smtps?://|\bsmtps?://", re.I)
_SUBMIT = re.compile(r"\b(submit|einreichen|deploy|merge|publish|veröffentlich\w*|force[- ]?push)\b", re.I)


def split_frontmatter(txt: str):
    if txt.startswith("---"):
        parts = txt.split("---", 2)
        if len(parts) == 3:
            return parts[1], parts[2]
    return "", txt


def _tool_grants(fm: str):
    """Alle Frontmatter-Keys, die wie Tool-Grants aussehen → (Tool-Set, wildcard?).
    Fängt auch nicht-Standard-Keys (permitted_tools/tools-allowed/allow)."""
    toks, wildcard = set(), False
    for m in re.finditer(r"^([\w-]*(?:tool|allow)[\w-]*):\s*(.+)$", fm, re.I | re.M):
        raw = m.group(2).strip()
        if "*" in raw:
            wildcard = True
        for t in re.split(r"[,\s]+", raw.strip("[]")):
            t = t.strip("'\"").lower()
            if t and t != "*":
                toks.add(t)
    return toks, wildcard


def _scan_text(md: Path, is_skill: bool) -> str:
    """Voller Prüftext: SKILL.md + references/ + scripts/ (schließt referenced-file-Payload-Lücke)."""
    parts = [md.read_text(encoding="utf-8", errors="replace")]
    if is_skill:
        n = 0
        for sub in ("references", "scripts"):
            p = md.parent / sub
            if p.is_dir():
                for f in sorted(p.rglob("*")):
                    if n >= MAX_SUBFILES:
                        break
                    try:
                        if f.is_file() and f.stat().st_size < MAX_SUBFILE:
                            parts.append(f.read_text(encoding="utf-8", errors="replace")); n += 1
                    except Exception:
                        pass
    return "\n".join(parts)


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _near(text: str, pos: int, rx: re.Pattern, window: int = 160) -> bool:
    return bool(rx.search(text[max(0, pos - window):pos + window]))


def redteam_scan(fm: str, scan_text: str, is_agent: bool):
    findings = []
    grants, wildcard = _tool_grants(fm)
    side_effect = bool(grants & SIDE_EFFECT_TOOLS)
    fetch = bool(grants & FETCH_TOOLS)
    has_disable = bool(re.search(r"disable-model-invocation:\s*true", fm, re.I))

    def add(sev, code, pos, why):
        findings.append((sev, code, _line_of(scan_text, pos) if pos else 0, why))

    # ── BLOCK-Tier: unzweideutige Gefahr (near-zero FP auf legitime Skills) ──
    m = _INJ_A.search(scan_text) or _INJ_B.search(scan_text)
    if m:
        add("BLOCK", "INJECTION_SURFACE", m.start(),
            "gehorcht Instruktionen aus externem/eingelesenem Inhalt → Instruction-Hijack")
    m = _DESTRUCT.search(scan_text)
    if m:
        add("BLOCK", "DESTRUCTIVE", m.start(),
            "selbst-destruktiver/obfuskierter Shell-Befehl (rm -rf ~//, pipe-to-shell, base64|sh, disk-wipe)")
    if wildcard:
        add("BLOCK", "WILDCARD_TOOL_GRANT", 0,
            "Wildcard-Tool-Grant (*) — ein neuer Skill/Agent braucht nie alle Tools (Least-Privilege)")

    # ── WARN-Tier: kontextabhängig (in Security-Tools legitim → menschliches Review, kein Auto-HOLD) ──
    secret_pos = [m.start() for m in _SECRET.finditer(scan_text)
                  if not NEG_ADJ.search(scan_text[max(0, m.start() - 12):m.start()])]
    outward_pos = [m.start() for m in _OUTWARD.finditer(scan_text)]
    if secret_pos:
        add("WARN", "SECRET_OUTPUT", secret_pos[0],
            "Secret/Token-Ausgabe/-Versand → prüfen ob legitim (Validierung) vs. Exfiltration")
    if outward_pos:
        gated = _near(scan_text, outward_pos[0], GATE_WORDS)
        add("WARN", "OUTWARD_INITIATION", outward_pos[0],
            "outward-Kommunikation" + (" (Gate nahebei)" if gated else " ohne nahes Gate")
            + " → Agent-zu-Agent/Human-Grenze prüfen (muss orchestrator-/User-gated sein)")
    for m in _SUBMIT.finditer(scan_text):
        if not _near(scan_text, m.start(), GATE_WORDS):
            add("WARN", "AUTO_SUBMIT_UNGATED", m.start(),
                "Submit/Deploy/Merge-Verb ohne nahes Gate-Wort (User-OK/draft/Freigabe) — prüfen")
            break
    # Multi-Signal-Eskalation: Secret-Ausgabe UND outward-Versand NAHE beieinander (≤200 Zeichen =
    # eine Operation) = Exfil-Pipeline → BLOCK. Proximity verhindert FP auf Agenten, die beides nur
    # in getrennten Sektionen erwähnen (OSINT: Secrets finden ≠ Secrets versenden).
    if secret_pos and outward_pos and min(abs(s - o) for s in secret_pos for o in outward_pos) <= 200:
        add("BLOCK", "EXFIL_PIPELINE", 0,
            "Secret-Ausgabe UND outward-Versand NAHE beieinander → Exfiltrations-Pipeline (Multi-Signal)")

    if fetch and side_effect:
        add("WARN", "FETCH_PLUS_EXEC", 0,
            f"Fetch- {sorted(grants & FETCH_TOOLS)} + Side-Effect-Tools {sorted(grants & SIDE_EFFECT_TOOLS)} "
            "→ ingest+exec-Fläche: sicherstellen, dass NIE eingelesenem Inhalt gehorcht wird")
    elif side_effect and not is_agent and not has_disable:
        add("INFO", "SIDE_EFFECT_NO_DISABLE", 0,
            f"Side-Effect-Tools {sorted(grants & SIDE_EFFECT_TOOLS)} ohne disable-model-invocation")
    if (side_effect or _SUBMIT.search(scan_text)) and not GATE_WORDS.search(scan_text):
        add("WARN", "MISSING_HARDGATES", 0,
            "Side-Effect-/Submit-Fläche ohne jeden Hard-Gate-Bezug (read-only/User-OK/_shared/hard-gates)")
    return findings


def _run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return p.returncode, p.stdout + p.stderr
    except Exception as e:
        return None, f"(konnte nicht laufen: {e})"


def resolve(target: str):
    p = Path(target)
    if p.is_file() and p.suffix == ".md":
        return p, ("/agents/" in str(p.resolve()))
    if p.is_dir():
        for c in ("SKILL.md", "skill.md"):
            if (p / c).is_file():
                return p / c, False
    for cand, is_agent in ((SKILLS_DIR / target / "SKILL.md", False),
                           (AGENTS_DIR / f"{target}.md", True),
                           (COMMANDS_DIR / f"{target}.md", False)):
        if cand.is_file():
            return cand, is_agent
    return None, False


def main() -> int:
    ap = argparse.ArgumentParser(description="Shadow/Red-Team-Gate vor Promotion eigener Skills/Agenten (read-only).")
    ap.add_argument("target", help="Skill-/Agent-/Command-Name oder Pfad zur .md/Skill-Dir")
    ap.add_argument("--strict", action="store_true", help="exit 1 bei HOLD (CI/Pre-Promote)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    md, is_agent = resolve(args.target)
    if not md:
        print(f"skill-promote-gate: '{args.target}' nicht gefunden.", file=sys.stderr)
        return 0
    txt = md.read_text(encoding="utf-8", errors="replace")
    fm, _ = split_frontmatter(txt)
    is_skill = md.name.lower() == "skill.md"
    disp = md.parent.name if is_skill else md.stem
    kind = "Agent" if is_agent else ("Skill" if is_skill else "Command")
    scan_text = _scan_text(md, is_skill)

    v_errors = 0
    if is_skill:
        _, vout = _run([sys.executable, str(VALIDATE), str(md.parent)])
        v_errors = len(re.findall(r"\[ERROR\]", vout)) if vout else 0
    doctor_prio = None
    if is_skill:
        _, dout = _run([sys.executable, str(DOCTOR), "--json"])
        try:
            for r in json.loads(dout).get("reports", []):
                if r.get("skill") == md.parent.name:
                    doctor_prio = r.get("priority"); break
        except Exception:
            pass

    findings = redteam_scan(fm, scan_text, is_agent)
    blocks = [f for f in findings if f[0] == "BLOCK"]
    warns = [f for f in findings if f[0] == "WARN"]
    hold = bool(blocks) or v_errors > 0
    verdict = "HOLD" if hold else ("PROMOTE-WITH-NOTES" if warns else "PROMOTE")

    if args.json:
        print(json.dumps({
            "target": str(md), "kind": kind, "verdict": verdict,
            "validate_errors": v_errors, "doctor_priority": doctor_prio,
            "findings": [{"severity": s, "code": c, "line": ln, "why": w} for s, c, ln, w in findings],
        }, ensure_ascii=False, indent=2))
        return 1 if (hold and args.strict) else 0

    icon = {"HOLD": "🛑", "PROMOTE-WITH-NOTES": "🟡", "PROMOTE": "🟢"}[verdict]
    print(f"╭─ skill-promote-gate — Shadow/Red-Team VOR Promotion ({kind}: {disp}) ─╮")
    print(f"│ {icon} VERDICT: {verdict}")
    print(f"│ Compliance (validate_skills): {v_errors} ERROR"
          + (f"  ·  Rightsizing-Prio (skill_doctor): {doctor_prio}" if doctor_prio is not None else ""))
    print("╰" + "─" * 78 + "╯")
    if not findings:
        print("Red-Team-Scan: keine Selbst-Gefahr-Muster.")
    for sev, code, ln, why in sorted(findings, key=lambda f: {"BLOCK": 0, "WARN": 1, "INFO": 2}[f[0]]):
        print(f"  [{sev}] {code}{f' (Z.{ln})' if ln else ''}: {why}")
    print("\nManuelle Pre-Promotion-Schritte (SDLC — vom Lead auszuführen, nicht auto):")
    print("  □ Shadow-Dry-Run: neuen Skill erst mit `disable-model-invocation:true`/nur manuell an ≥2")
    print("    repräsentativen Fällen beobachten, BEVOR die Auto-Invocation frei ist.")
    grants, wc = _tool_grants(fm)
    if is_agent or wc or (grants & (SIDE_EFFECT_TOOLS | FETCH_TOOLS)):
        print("  □ Deep-Red-Team (High-Privilege): adversarial reviewer/Red-Team-Review — statischer Scan ist")
        print("    nur erste Linie und umgehbar; exec/outward/fetch-Fähigkeit braucht menschliches Urteil.")
    print("  □ Bug-class→Skill-Patch: fand der Shadow-Run/Review eine Lücke → als Fix zurück in Skill/CLAUDE.md.")
    print("\n→ Agent-zu-Agent-Grenze: `_orchestration.md` · Hard-Gates: `_shared/hard-gates.md` · voll: --json")
    return 1 if (hold and args.strict) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"skill-promote-gate: interner Fehler (read-only, nichts geändert): {e}", file=sys.stderr)
        sys.exit(0)
