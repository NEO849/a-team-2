#!/usr/bin/env python3
"""
skill_doctor.py — ADVISORY Rightsizing-Audit der Skill-Library.

Portiert Anthropics „/doctor"-Idee + die 6 Context-Engineering-Shifts für Claude-5
(https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models,
2026-07-24) auf unsere ~70 Skills. Der Audit RANKT Kandidaten fürs Rightsizing gegen die
Shifts und zeigt PRO Fund die rohe Evidenz (keine Black-Box-Gewichte) — er entscheidet NICHTS
und ändert NICHTS.

Abgrenzung: `validate_skills.py` ist das Hard-GATE (Frontmatter/Caps/broken-links, exit 0/1).
Dieser hier ist der ADVISORY-Layer darüber — blockt NIE (exit 0), empfiehlt nur.

⚠️ HONEST-CATCH (aus dem Backlog): Die Anthropic-Guidance ist für Claude-5-Gen kalibriert; die
„>80% gekürzt ohne Eval-Verlust" NICHT cargo-culten. Das hier sind KANDIDATEN — Eval-Neutralität
je Skill selbst prüfen VOR dem Kürzen. Ein hoher Score heißt „anschauen", nicht „automatisch kürzen".

Read-only. stdlib-only. `--json` für Maschinen-Output, `--top N`, `--commands` (auch Slash-Commands).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
COMMANDS_DIR = Path.home() / ".claude" / "commands"

# Schwellen (kalibriert an unserem AUTHORING.md: Body <500 hart, Progressive Disclosure > ~200)
BODY_HARD = 500          # über dem Body-Budget aus AUTHORING.md
SPLIT_HINT = 200         # ab hier lohnt Progressive Disclosure zu erwägen
DESC_SOFT = 800          # Description nähert sich dem 1024-Cap
EXAMPLE_HINT = 6         # viele Code/Beispiel-Blöcke → Kandidat "examples→interface"
RULE_COUNT_HINT = 25     # viele Hart-Direktiven …
RULE_DENSITY_HINT = 15   # … UND hohe Dichte (pro 100 Zeilen) → "rules→judgement"
DUP_HINT = 3             # ≥ N wiederholte Sinn-Zeilen → "repetition"

_DIRECTIVE = re.compile(
    r"\b(MUST|SHALL|ALWAYS|NEVER|MANDATORY|REQUIRED|DO NOT|DON'?T|"
    r"IMMER|NIEMALS|NIE|VERBOTEN|PFLICHT|ZWINGEND|MUSS|DARF NICHT|KEINE?)\b", re.I)
_FENCE = re.compile(r"^\s*```")
_EXAMPLE_WORD = re.compile(r"\b(for example|beispiel|z\.\s?b\.|e\.g\.|example:)\b", re.I)
_MDLINK = re.compile(r"\]\(([^)]+\.md)\)")


def split_frontmatter(txt: str):
    """(frontmatter, body). Robust: kein/kaputtes Frontmatter → ('', txt)."""
    if txt.startswith("---"):
        parts = txt.split("---", 2)
        if len(parts) == 3:
            return parts[1], parts[2]
    return "", txt


def _description(fm: str) -> str:
    """Description-Wert (auch YAML-Block-Skalar `>` / `|`) grob extrahieren."""
    lines = fm.split("\n")
    for i, l in enumerate(lines):
        m = re.match(r"^description:\s*(.*)$", l)
        if not m:
            continue
        head = m.group(1).strip()
        if head in (">", "|", ">-", "|-", ">+", "|+"):    # Block-Skalar → Folgezeilen sammeln
            block = []
            for j in range(i + 1, len(lines)):
                if lines[j].strip() != "" and re.match(r"^\S", lines[j]):
                    break
                block.append(lines[j].strip())
            return " ".join(b for b in block if b)
        return head.strip("'\"")
    return ""


def _has_progressive_disclosure(body: str, skill_dir: Path) -> bool:
    """Nutzt der Skill Referenz-Auslagerung? references/-Dir, relative .md-Links, oder .md-Geschwister."""
    if (skill_dir / "references").is_dir():
        return True
    if _MDLINK.search(body):
        return True
    try:
        siblings = [p for p in skill_dir.glob("*.md") if p.name.lower() != "skill.md"]
        if siblings:
            return True
    except Exception:
        pass
    return False


def _dup_lines(body: str) -> int:
    """Anzahl distinkter Sinn-Zeilen, die ≥2× vorkommen (Redundanz-Signal)."""
    norm = []
    for l in body.split("\n"):
        s = re.sub(r"\s+", " ", l.strip().lower())
        if len(s) > 25 and not s.startswith(("#", "|", "```", ">")):
            norm.append(s)
    return sum(1 for _, c in Counter(norm).items() if c >= 2)


def audit_skill(skill_md: Path):
    """Eine SKILL.md → Metriken + gerankte Findings. Reine Funktion, read-only, crasht nicht."""
    try:
        txt = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"skill": skill_md.parent.name, "error": str(e), "priority": 0, "findings": []}

    fm, body = split_frontmatter(txt)
    body_lines = body.count("\n") + 1
    tokens = len(txt) // 4                                  # grobe Kontext-Kosten-Schätzung
    desc_len = len(_description(fm))
    has_pd = _has_progressive_disclosure(body, skill_md.parent)
    fences = sum(1 for l in body.split("\n") if _FENCE.match(l))
    example_blocks = fences // 2 + len(_EXAMPLE_WORD.findall(body))
    directives = len(_DIRECTIVE.findall(body))
    density = round(directives / body_lines * 100, 1) if body_lines else 0.0
    dups = _dup_lines(body)

    findings = []   # (points, code, evidence) — Punkte SICHTBAR, keine Black-Box
    # Shift 3: all-upfront → progressive disclosure (der stärkste Rightsizing-Hebel)
    if body_lines > SPLIT_HINT and not has_pd:
        findings.append((5, "LONG_NO_REFS",
                         f"{body_lines} Zeilen, KEINE Referenz-Auslagerung → in references/ splitten"))
    elif body_lines > BODY_HARD:
        findings.append((3, "OVER_BODY_BUDGET", f"{body_lines} > {BODY_HARD} Zeilen (Body-Budget)"))
    elif body_lines > SPLIT_HINT:
        findings.append((2, "LONG", f"{body_lines} Zeilen — Progressive Disclosure erwägen"))
    # Shift 2: examples → interface-design (nur bei substanziellen Skills — kurze
    # Tool-Wrapper haben legitim mehrere Invocation-Fences, das ist kein Rightsizing-Problem)
    if example_blocks > EXAMPLE_HINT and body_lines > 150:
        pts = 3 if example_blocks > EXAMPLE_HINT * 2 else 2
        findings.append((pts, "EXAMPLE_HEAVY",
                         f"{example_blocks} Code/Beispiel-Blöcke → Interface-Design statt Beispiel-Wand"))
    # Shift 1: rules → judgement
    if directives > RULE_COUNT_HINT and density > RULE_DENSITY_HINT:
        findings.append((2, "RULE_DENSE",
                         f"{directives} Hart-Direktiven ({density}/100 Z.) → Urteil zulassen, nur load-bearing behalten"))
    # Shift 4: repeat → consolidate
    if dups >= DUP_HINT:
        findings.append((min(dups, 3), "REPETITION", f"{dups} wiederholte Sinn-Zeilen → konsolidieren"))
    # Shift 5: description bloat (nähert sich Cap / Methodik-Prosa)
    if desc_len > DESC_SOFT:
        findings.append((1, "DESC_BLOAT", f"description {desc_len} Zeichen (Cap 1024) → Methodik in Body"))

    return {
        "skill": skill_md.parent.name,
        "path": str(skill_md),
        "lines": body_lines, "tokens": tokens, "desc_len": desc_len,
        "has_progressive_disclosure": has_pd, "example_blocks": example_blocks,
        "directives": directives, "directive_density": density, "dup_lines": dups,
        "priority": sum(p for p, _, _ in findings),
        "findings": [{"points": p, "code": c, "evidence": e} for p, c, e in findings],
    }


def collect(skills_dir: Path, commands_dir: Path, do_commands: bool):
    out = []
    if skills_dir.is_dir():
        for d in sorted(skills_dir.iterdir()):
            if d.name.startswith((".", "_")) or not d.is_dir():
                continue
            for cand in ("SKILL.md", "skill.md"):
                if (d / cand).is_file():
                    out.append(d / cand); break
    if do_commands and commands_dir.is_dir():
        for f in sorted(commands_dir.glob("*.md")):
            out.append(f)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Advisory Rightsizing-Audit der Skill-Library (read-only).")
    ap.add_argument("--json", action="store_true", help="Maschinen-Output")
    ap.add_argument("--top", type=int, default=15, help="Top-N Kandidaten im Report (Default 15)")
    ap.add_argument("--commands", action="store_true", help="auch ~/.claude/commands/*.md auditen")
    ap.add_argument("--skills-dir", default=str(SKILLS_DIR))
    args = ap.parse_args()

    targets = collect(Path(args.skills_dir), COMMANDS_DIR, args.commands)
    reports = [audit_skill(p) for p in targets]
    reports.sort(key=lambda r: (-r.get("priority", 0), -r.get("lines", 0)))

    total_tokens = sum(r.get("tokens", 0) for r in reports)
    flagged = [r for r in reports if r.get("priority", 0) > 0]
    top5_tokens = sum(r.get("tokens", 0) for r in sorted(reports, key=lambda r: -r.get("tokens", 0))[:5])

    if args.json:
        print(json.dumps({
            "summary": {"skills": len(reports), "flagged": len(flagged),
                        "total_tokens_est": total_tokens, "top5_tokens_est": top5_tokens},
            "reports": reports}, ensure_ascii=False, indent=2))
        return 0

    print("╭─ skill-doctor — ADVISORY Rightsizing-Audit (blockt nie; du entscheidest je Skill) ─╮")
    print(f"│ {len(reports)} Skills · ~{total_tokens:,} Token Library-Footprint (on-demand geladen, nicht dauer-resident)")
    print(f"│ {len(flagged)} mit Kandidat-Findings · Top-5-schwerste ~{top5_tokens:,} Token (Last, wenn gleichzeitig getriggert)")
    print("│ ⚠️ Kandidaten, KEINE Anweisung. Eval-Neutralität je Skill prüfen VOR Kürzen (nicht 80% cargo-culten).")
    print("╰" + "─" * 84 + "╯")
    shown = [r for r in reports if r.get("priority", 0) > 0][:args.top]
    if not shown:
        print("\n✅ Kein Skill über den Rightsizing-Schwellen. Library ist rund.")
    for i, r in enumerate(shown, 1):
        pd = "refs✓" if r["has_progressive_disclosure"] else "keine-refs"
        print(f"\n{i:>2}. {r['skill']}  [Prio {r['priority']}]  "
              f"{r['lines']}Z · ~{r['tokens']}tok · {pd} · {r['example_blocks']}bsp · "
              f"{r['directives']}dir({r['directive_density']}/100)")
        for f in r["findings"]:
            print(f"     +{f['points']} {f['code']}: {f['evidence']}")
    print(f"\n→ Volle Daten: --json  |  Autoren-Standard: _shared/AUTHORING.md  |  Hard-Gate: validate_skills.py")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"skill-doctor: interner Fehler (read-only, nichts geändert): {e}", file=sys.stderr)
        sys.exit(0)     # advisory: niemals als Fehler-Gate crashen
