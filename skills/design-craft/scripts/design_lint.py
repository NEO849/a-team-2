#!/usr/bin/env python3
"""design_lint.py — advisory Anti-Slop-Detektor für UI-Dateien (stdlib-only).

Greppt geänderte Frontend-Dateien nach den MASCHINELL ZÄHLBAREN Anti-Slop-Tells aus
design-craft/references/craft-floor.md + motion-craft/references/forbidden.md.
Bewusst hochpräzise Regelmenge (keine False-Positive-Flut). ADVISORY: meldet, blockt NIE (Exit 0).

Nutzung:
    python3 design_lint.py <datei-oder-verzeichnis> [...]      # menschenlesbar
    python3 design_lint.py --json <pfad> [...]                 # JSON
    echo '<pfad>' | python3 design_lint.py --stdin             # ein Pfad je Zeile (Hook-Modus)

Als PostToolUse-Hook (opt-in, pro Projekt) siehe den Kommentar am Dateiende.
"""
import sys
import re
import json
from pathlib import Path

UI_EXT = {".tsx", ".jsx", ".ts", ".js", ".css", ".scss", ".sass",
          ".html", ".htm", ".vue", ".svelte", ".astro"}
SKIP_DIR = {"node_modules", "dist", "build", ".next", ".git", "out", "vendor", "coverage"}

# Premium-Consumer-Palette-Bann (craft-floor.md §2) — exakte Hex-Familien
BANNED_HEX = {
    "#f5f1ea", "#f7f5f1", "#fbf8f1", "#efeae0", "#ece6db", "#faf7f1", "#e8dfcb",
    "#b08947", "#b6553a", "#9a2436", "#9c6e2a", "#bc7c3a", "#7d5621",
    "#1a1714", "#1a1814", "#1b1814",
}

# (rule_id, severity, compiled_regex, message)
RULES = [
    ("em-dash", "warn", re.compile(r"[—–]"),
     "Em-/En-Dash im sichtbaren UI verboten (craft-floor §1) -> Punkt/Komma/Klammer/Bindestrich"),
    ("transition-all", "warn", re.compile(r"transition\s*:\s*all\b"),
     "`transition: all` -> exakte Properties benennen (forbidden.md)"),
    ("scale-zero", "warn", re.compile(r"scale\(\s*0(?:\.0+)?\s*\)"),
     "`scale(0)`-Entrance -> scale(0.95) + opacity:0 (motion-tables §4)"),
    ("ease-in", "info", re.compile(r"\bease-in\b(?!-out)"),
     "`ease-in` auf UI startet langsam -> ease-out / starke Custom-Kurve (motion-tables §5)"),
    ("scroll-listener", "warn", re.compile(r"addEventListener\(\s*['\"]scroll['\"]"),
     "Scroll-Listener -> scroll-driven CSS / Motion useScroll / GSAP ScrollTrigger (forbidden.md)"),
    ("scrollY-state", "info", re.compile(r"\bwindow\.scrollY\b"),
     "`window.scrollY` (oft in State) -> Motion useMotionValue/useTransform (forbidden.md)"),
    ("gradient-text", "warn", re.compile(r"background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text"),
     "Gradient-Text-Muster -> Betonung aus Gewicht/Größe (craft-floor §1)"),
    ("outline-none", "info", re.compile(r"outline\s*:\s*(?:none|0)\b"),
     "`outline:none` -> :focus-visible-Ersatz nötig (a11y, visual-preflight G)"),
    ("banned-serif", "info", re.compile(r"Fraunces|Instrument[_ ]Serif"),
     "Fraunces/Instrument-Serif als Default gebannt (craft-floor §3) -> begründen oder rotieren"),
    ("h-screen", "info", re.compile(r"\bh-screen\b"),
     "`h-screen` -> min-h-[100dvh] (craft-floor §4)"),
]

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")


def iter_files(paths):
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for f in path.rglob("*"):
                if f.is_file() and f.suffix.lower() in UI_EXT \
                        and not any(part in SKIP_DIR for part in f.parts) \
                        and ".min." not in f.name:
                    yield f
        elif path.is_file() and path.suffix.lower() in UI_EXT:
            yield path


def scan_file(f):
    findings = []
    try:
        text = f.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [{"file": str(f), "line": 0, "rule": "read-error",
                 "severity": "info", "msg": str(e)}]
    for lineno, line in enumerate(text.splitlines(), 1):
        for rule_id, sev, rx, msg in RULES:
            if rx.search(line):
                findings.append({"file": str(f), "line": lineno, "rule": rule_id,
                                 "severity": sev, "msg": msg})
        for hx in HEX_RE.findall(line):
            if hx.lower() in BANNED_HEX:
                findings.append({"file": str(f), "line": lineno, "rule": "banned-palette",
                                 "severity": "warn",
                                 "msg": f"Gebannte Premium-Consumer-Palette {hx} (craft-floor §2) -> Palette rotieren"})
    return findings


def main(argv):
    as_json = "--json" in argv
    use_stdin = "--stdin" in argv
    args = [a for a in argv if not a.startswith("--")]
    if use_stdin:
        args += [ln.strip() for ln in sys.stdin if ln.strip()]
    if not args:
        print("usage: design_lint.py [--json] [--stdin] <datei-oder-verzeichnis> ...", file=sys.stderr)
        return 0  # advisory: nie hart fehlschlagen

    all_findings = []
    for f in iter_files(args):
        all_findings.extend(scan_file(f))

    if as_json:
        print(json.dumps({"findings": all_findings, "count": len(all_findings)}, ensure_ascii=False, indent=2))
        return 0

    if not all_findings:
        print("design-lint: keine zählbaren Anti-Slop-Tells gefunden.")
        return 0
    order = {"warn": 0, "info": 1}
    all_findings.sort(key=lambda x: (order.get(x["severity"], 2), x["file"], x["line"]))
    print(f"design-lint (advisory): {len(all_findings)} Hinweis(e) — blockt nicht.\n")
    for x in all_findings:
        tag = "WARN" if x["severity"] == "warn" else "info"
        print(f"  [{tag}] {x['file']}:{x['line']}  {x['rule']}: {x['msg']}")
    print("\nManuell prüfen (nicht auto-detektierbar): Eyebrow-Count, Layout-Familien-Varianz, "
          "Bento-Cell-Count, echte Bilder, Motion-Motiv, Browser-Surfaces. -> /design-review")
    return 0


# ── PostToolUse-Hook (opt-in, pro Projekt) ────────────────────────────────
# In .claude/settings.json des Projekts:
#   "hooks": { "PostToolUse": [ {
#     "matcher": "Write|Edit",
#     "hooks": [ { "type": "command",
#       "command": "jq -r '.tool_input.file_path // empty' | grep -Ei '\\.(tsx|jsx|ts|js|css|scss|html|vue|svelte|astro)$' | python3 ${CLAUDE_SKILL_DIR}/scripts/design_lint.py --stdin" } ] } ] }
# Advisory: gibt Hinweise aus, blockt nie (wie mc-scan).
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
