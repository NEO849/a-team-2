#!/usr/bin/env python3
"""
skill_audit.py — Paired-Trajectory-Audit für SCORER-LOSE Skills (no-scorer-Branch von /skill-harden).

Die meisten unserer Skills (recon-jagd, dork-sweep, OSINT) haben KEIN automatisches Pass/Fail — PACE/#6 allein
kann sie nicht anfassen. SkillAudit (arxiv 2606.14239, KEIN Repo → nur Methodik portiert): dieselbe Aufgabe MIT
und OHNE den Kandidaten-Edit laufen, die Divergenz IST das Signal. Ein Judge urteilt je Paar drei-wege:
`helped` / `hurt` / `inert`.

Dieses Skript AGGREGIERT die (vom Judge produzierten) Drei-Wege-Verdikte deterministisch — es ersetzt NICHT das
Judge-Urteil. Zwei Bausteine:
  1. Mapping auf paired outcomes → REUSE des #6-PACE-Gates (skill_harden_gate.eprocess): helped=neu-gewinnt [0,1],
     hurt=alt-gewinnt [1,0], inert=konkordant [1,1] (keine Info). So nutzt der ganze Skill-Evolutions-Cluster EINE
     anytime-valide Akzeptanzregel — kein Selbst-p-hacking, auch scorer-los.
  2. RSEA-Vet-Filter (arxiv 2606.28374, ASSUMED): ein Self-Evolution-„Win auf dem EINEN Benchmark, wo es hilft" ist
     unbewiesen. Wenn PACE ACCEPT sagt, aber alle `helped`-Fälle DIESELBE Task-Klasse teilen → NEEDS-BROADER-COVERAGE
     (nicht akzeptieren, breiter validieren).

⚠ MAGE-Caveat (arxiv 2607.11944, ASSUMED): held-out-Gate (#6) + grow-and-refine + paired-audit (#7) interagieren
NICHT-additiv — beim Ablatieren EINZELN testen, nicht blind stapeln. read-only, stdlib-only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

# #6-PACE-Gate wiederverwenden (eine valide Akzeptanzregel für den ganzen Cluster)
_spec = importlib.util.spec_from_file_location("pace", str(Path(__file__).parent / "skill_harden_gate.py"))
pace = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(pace)

_MAP = {"helped": [0, 1], "hurt": [1, 0], "inert": [1, 1]}   # → [old_ok, new_ok] fürs paired-Gate

# 5 Vergleichs-Linsen (kompakt statt 12 verbatim — Repo unbekannt), die der Judge je with/without-Paar anlegt:
LENSES = ["correctness (falsche/erfundene Fakten?)", "completeness (mehr echte Surface/Treffer?)",
          "efficiency (weniger Schritte/Token fürs gleiche Ergebnis?)", "no-regression (bricht nichts Bisheriges?)",
          "hallucination (Skill verleitet zu Behauptungen ohne Beleg?)"]


def audit(records, alpha=0.05, min_classes=2, max_pairs=200):
    """records: [{"verdict": helped|hurt|inert, "task_class": "..."}]. Deterministische Aggregation."""
    paired, bad = [], []
    for r in records:
        v = str(r.get("verdict", "")).lower()
        if v not in _MAP:
            bad.append(v); continue
        paired.append(_MAP[v])
    pace_r = pace.eprocess(paired, alpha=alpha, max_pairs=max_pairs)
    counts = Counter(str(r.get("verdict", "")).lower() for r in records)
    helped_classes = {r.get("task_class", "?") for r in records if str(r.get("verdict", "")).lower() == "helped"}
    coverage_ok = len(helped_classes) >= min_classes
    verdict = pace_r["verdict"]
    note = pace_r["reason"]
    # RSEA: ACCEPT nur mit Klassen-Breite; sonst single-benchmark-win = unbewiesen
    if verdict == "ACCEPT" and not coverage_ok:
        verdict = "NEEDS-BROADER-COVERAGE"
        note = (f"RSEA: 'helped' nur in {len(helped_classes)} Task-Klasse(n) (<{min_classes}) → single-benchmark-win, "
                "unbewiesen. Breitere with/without-Fälle sammeln, dann erneut.")
    return {
        "verdict": verdict, "note": note,
        "counts": {"helped": counts.get("helped", 0), "hurt": counts.get("hurt", 0), "inert": counts.get("inert", 0)},
        "helped_task_classes": sorted(helped_classes), "coverage_ok": coverage_ok,
        "pace": {k: pace_r[k] for k in ("verdict", "e_new", "e_old", "threshold", "discordant")},
        "unparsed": bad,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Scorer-loser Paired-Trajectory-Audit (aggregiert Judge-Verdikte, read-only).")
    ap.add_argument("records", nargs="?", help='JSON: [{"verdict":"helped|hurt|inert","task_class":"x"}, ...]. Sonst stdin.')
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--min-classes", type=int, default=2, help="RSEA: min. distinkte 'helped'-Klassen für ACCEPT")
    ap.add_argument("--lenses", action="store_true", help="die Judge-Vergleichs-Linsen ausgeben")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.lenses:
        print("Judge-Linsen je with/without-Paar (Verdikt helped/hurt/inert):")
        for l in LENSES:
            print(f"  • {l}")
        return 0
    try:
        recs = json.loads(args.records or sys.stdin.read())
        assert isinstance(recs, list)
    except Exception as e:
        print(f'skill_audit: JSON [{{"verdict":...,"task_class":...}}] erwartet: {e}', file=sys.stderr)
        return 0
    r = audit(recs, alpha=args.alpha, min_classes=args.min_classes)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2)); return 0
    icon = {"ACCEPT": "🟢", "REJECT": "🔴", "CONTINUE": "🟡", "NEEDS-BROADER-COVERAGE": "🟠"}[r["verdict"]]
    c = r["counts"]
    print(f"{icon} SkillAudit (scorer-los): {r['verdict']}")
    print(f"   helped={c['helped']} · hurt={c['hurt']} · inert={c['inert']} · "
          f"helped-Klassen={len(r['helped_task_classes'])} · E_new={r['pace']['e_new']}/{r['pace']['threshold']}")
    print(f"   {r['note']}")
    print("   ⚠ MAGE: #6-Gate + paired-audit nicht-additiv — einzeln ablatieren, nicht blind stapeln.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"skill_audit: Fehler: {e}", file=sys.stderr)
        sys.exit(0)
