#!/usr/bin/env python3
"""
mc_scan.py — Static-Sweep fuer UNGESCHUETZTE konsequenzielle Aktionen im EIGENEN Code.

PORT der MakerChecker-`mc scan`-Idee (nicht deren Code): findet konsequenzielle Operationen in UNSEREN
eigenen Scripts/Hooks (.py/.js) — Code-Ausfuehrung, Shell-Injection, Datei-Loeschung, destruktives Git —
die KEINEN Guard tragen (kein dry-run/confirm/force-check/temp-Pfad/kill-switch). Deny-by-default-Denken
auf unser Arsenal angewandt: eine gefaehrliche Operation ohne Gate ist ein Review-Kandidat.

⚠️ Advisory, read-only, blockt/aendert NICHTS. Dieses Tool macht viele subprocess/curl-Aufrufe by design —
das ist fuer sich genommen LEGITIM. Der Scan zielt auf SELBST-gefaehrliche Muster (loescht/exect auf UNSEREM
System ohne Guard), NICHT auf "ruft ein Tool extern auf". Guarded-Fund = INFO, unguarded = WARN.

Guard = eines der folgenden in der Naehe (±GUARD_WINDOW Zeilen) oder dateiweit: dry_run/dry-run, --confirm,
--force + not-force-check, AGENT_STOP/kill_switch, input()/user-ok, tempfile/scratchpad/logs-Pfad, test_-Datei.

stdlib-only. CLI: `mc_scan.py [pfad ...]` (Default: ~/.claude/scripts + ~/.claude/hooks). `--json`, `--strict` (exit 1 bei unguarded), `--top N`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HOME = Path.home()
DEFAULT_ROOTS = [HOME / ".claude" / "scripts", HOME / ".claude" / "workflows"]
SKIP_DIRS = {".venv", "node_modules", "__pycache__", "_archive", ".git", "site-packages", "dist", "build"}
# Detektor-/Guard-Dateien: enthalten gefaehrliche Muster BEWUSST als Daten (Regex/Testfaelle/Messages) →
# ihr Scan waere reines Selbst-Rauschen. Das ist ihr Job, nicht ein ungeschuetzter Op.
DENYLIST = {"bash-safety-guard.py", "mc_scan.py", "prompt_prefilter.py", "injection_scanner.py",
            "scope_authz_gate.py", "skill_promote_gate.py", "scope_guard.py", "steer.py"}
GUARD_WINDOW = 8
MAX_FILE = 400_000
# Zeilen, die Muster DEFINIEREN statt Ops auszufuehren (Regex/Detektion) → keine echte Operation
_DATALINE = re.compile(r"re\.(compile|search|match|finditer|sub|split)\b|\.(search|match|finditer)\s*\(")

# (category, [regex], beschreibung, severity_if_unguarded)
_CATS = [
    ("code-exec", [re.compile(r"(?<![\w.])(eval|exec)\s*\(")],   # bare eval(/exec(, nicht .eval() (z.B. torch)
     "eval/exec — dynamische Code-Ausfuehrung", "HIGH"),
    ("shell-injection", [
        re.compile(r"\bos\.system\s*\("),
        re.compile(r"subprocess\.(run|call|Popen|check_output|check_call)\s*\([^)]*shell\s*=\s*True", re.I),
        re.compile(r"\bos\.popen\s*\("),
        re.compile(r"child_process\.exec(Sync)?\s*\("),
    ], "Shell mit shell=True / os.system / exec — Injection-Flaeche", "HIGH"),
    ("file-deletion", [
        re.compile(r"shutil\.rmtree\s*\("),
        re.compile(r"\bos\.(remove|unlink)\s*\("),
        re.compile(r"\.unlink\s*\("),
        re.compile(r"\bfs\.(rm|unlink|rmdir)(Sync)?\s*\("),
        re.compile(r"\brm\s+-rf?\b"),
    ], "Datei-Loeschung", "MED"),
    ("destructive-git", [
        re.compile(r"git\s+push\b[^\n]*(--force\b|-f\b|--hard\b)", re.I),
        re.compile(r"git\s+reset\s+--hard", re.I),
        re.compile(r"git\s+clean\s+-[a-z]*[fd]", re.I),
        re.compile(r"git\s+checkout\s+--\s+\.", re.I),
    ], "destruktives Git (force-push/reset --hard/clean)", "MED"),
]

_GUARD = re.compile(
    r"dry[_-]?run|--confirm\b|\bconfirm\b|AGENT_STOP|kill_switch|input\s*\(|user[_ -]?ok|"
    r"if\s+not\s+force|require.{0,10}force|approval|approved|--yes\b|getpass|are you sure|bestaetig|freigab", re.I)
_TEMPPATH = re.compile(r"/tmp/|tempfile|scratchpad|/logs?/|TemporaryDirectory|mkdtemp|NamedTemporary", re.I)


def _iter_files(roots):
    for root in roots:
        root = Path(root)
        if root.is_file() and root.suffix in (".py", ".js"):
            yield root; continue
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix in (".py", ".js") and not any(d in p.parts for d in SKIP_DIRS):
                yield p


def _quoted(line: str, pos: int) -> bool:
    """Steht die Fundstelle in einem String-Literal? (ungerade Quote-Zahl davor) → Muster-Daten, keine Op."""
    pre = line[:pos]
    return (pre.count('"') % 2 == 1) or (pre.count("'") % 2 == 1)


def scan_file(path: Path):
    if path.name in DENYLIST:
        return []                                         # Detektor-Datei: enthaelt Muster als Daten
    try:
        if path.stat().st_size > MAX_FILE:
            return []
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    text = "\n".join(lines)
    file_guarded = bool(_GUARD.search(text)) or path.name.startswith("test_")
    findings = []
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("*"):
            continue                                      # Kommentare/Doku ignorieren
        if _DATALINE.search(line):
            continue                                      # Regex-/Detektions-Zeile, keine echte Op
        for cat, rxs, desc, sev in _CATS:
            m = next((mm for rx in rxs for mm in [rx.search(line)] if mm), None)
            if m:
                if _quoted(line, m.start()) or path.name.startswith("test_"):
                    break                                 # String-Literal/Testfixture = Muster-Daten, keine Op → naechste Zeile
                lo, hi = max(0, i - GUARD_WINDOW), min(len(lines), i + GUARD_WINDOW + 1)
                window = "\n".join(lines[lo:hi])
                local_guard = bool(_GUARD.search(window))
                temp_ctx = bool(_TEMPPATH.search(window))
                guarded = local_guard or temp_ctx or (file_guarded and cat in ("file-deletion", "destructive-git"))
                findings.append({
                    "file": str(path), "line": i + 1, "category": cat, "desc": desc,
                    "severity": sev, "guarded": guarded,
                    "guard": ("temp-path" if temp_ctx else "local" if local_guard else
                              "file-level" if guarded else "NONE"),
                    "snippet": line.strip()[:100],
                })
                break
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Static-Sweep: ungeschuetzte konsequenzielle Aktionen im eigenen Code (read-only).")
    ap.add_argument("paths", nargs="*", help="Dateien/Verzeichnisse (Default: ~/.claude/scripts + workflows)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--strict", action="store_true", help="exit 1 wenn ungeschuetzte HIGH-Funde")
    args = ap.parse_args()

    roots = [Path(p) for p in args.paths] if args.paths else DEFAULT_ROOTS
    all_f = []
    for f in _iter_files(roots):
        all_f.extend(scan_file(f))

    unguarded = [f for f in all_f if not f["guarded"]]
    unguarded.sort(key=lambda f: ({"HIGH": 0, "MED": 1}.get(f["severity"], 2), f["file"]))
    hi_unguarded = [f for f in unguarded if f["severity"] == "HIGH"]

    if args.json:
        import json
        print(json.dumps({"scanned": len({f["file"] for f in all_f}), "total": len(all_f),
                          "unguarded": len(unguarded), "high_unguarded": len(hi_unguarded),
                          "findings_unguarded": unguarded}, ensure_ascii=False, indent=2))
        return 1 if (args.strict and hi_unguarded) else 0

    from collections import Counter
    by_cat = Counter(f["category"] for f in unguarded)
    print("╭─ mc-scan — ungeschuetzte konsequenzielle Aktionen im eigenen Code (read-only, advisory) ─╮")
    print(f"│ {len({f['file'] for f in all_f})} Dateien · {len(all_f)} konsequenzielle Ops · "
          f"{len(all_f)-len(unguarded)} guarded · {len(unguarded)} UNGUARDED ({len(hi_unguarded)} HIGH)")
    print("│ ⚠️ Dieses Tool macht viele externe Aufrufe by design — das ist legitim. Fund = SELBST-Gefahr ohne Guard = REVIEW.")
    print(f"│    Detektor-/Guard-Dateien (Muster=Daten) per Denylist ausgeschlossen: {', '.join(sorted(DENYLIST))}")
    print("╰" + "─" * 88 + "╯")
    if by_cat:
        print("  Unguarded je Kategorie: " + " · ".join(f"{k}={v}" for k, v in by_cat.most_common()))
    for f in unguarded[:args.top]:
        rel = f["file"].replace(str(HOME), "~")
        print(f"\n  [{f['severity']}] {f['category']}  {rel}:{f['line']}")
        print(f"     {f['snippet']}")
    if not unguarded:
        print("\n✅ Keine ungeschuetzten konsequenziellen Aktionen gefunden.")
    print(f"\n→ --json fuer Details · Guard = dry-run/confirm/force-check/temp-Pfad/kill-switch · HITL entscheidet")
    return 1 if (args.strict and hi_unguarded) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"mc_scan: Fehler (read-only, nichts geaendert): {e}", file=sys.stderr)
        sys.exit(0)
