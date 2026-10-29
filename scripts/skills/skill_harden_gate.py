#!/usr/bin/env python3
"""
skill_harden_gate.py — PACE anytime-valid Akzeptanz-Gate fuers Skill-Hardening (3. Saeule).

Die fehlende 3. Saeule: /skill-forge (CREATE) + /skill-scout (IMPORT) + /skill-doctor (AUDIT) — hier
HARDEN eines BESTEHENDEN Skills aus echten Outcomes. SkillOpt behandelt eine SKILL.md als trainierbaren
Zustand (bounded add/delete/replace-Edit) und akzeptiert naiv "commit iff held-out-Score strikt besser".

PACE (arxiv 2606.08106) beweist: dieses naive `>` ist UNKONTROLLIERTES adaptives Multiple-Testing — wer
viele Edits gegen DENSELBEN held-out-Satz testet und die behaelt, die "besser" waren, ueberangepasst den
Satz → **der Agent p-hackt sich selbst**. Ersatz: ein ANYTIME-VALID e-process (testing-by-betting) auf den
diskordanten Paaren (paired-McNemar). Die False-Accept-Rate ist per Ville-Ungleichung durch die Schwelle
1/alpha kontrolliert — EGAL wie viele Edits/Peeks man macht. Genau das fixt SkillOpts naiven Schritt.

Modell: paired outcomes (old_ok, new_ok) je held-out-Fall. Diskordant = old != new. X=1 wenn NEU gewinnt
(new_ok & !old_ok), 0 wenn ALT gewinnt. Betting-Martingal E_new = prod(1 + lam*(2X-1)) mit PREDICTABLE
(nur-Vergangenheit) lam. Symmetrisch E_old fuer "neu ist schlechter".

Verdikt: ACCEPT (E_new >= 1/alpha) · REJECT (E_old >= 1/alpha, neu schlechter — ODER max_pairs ohne Accept →
reject-buffer, KEIN naives `>`) · CONTINUE (mehr held-out-Faelle noetig). read-only, stdlib-only.
"""
from __future__ import annotations

import argparse
import json
import sys

LAM_CAP = 0.9


def _sign(old, new):
    """+1 wenn neu gewinnt, -1 wenn alt gewinnt, 0 wenn konkordant/gleich/nicht-parsebar.
    Akzeptiert bool (korrekt/falsch) oder numerische Scores (hoeher=besser)."""
    try:
        o, n = float(old), float(new)
    except (TypeError, ValueError):
        return 0                       # nicht-parsebar → keine Information (skip)
    if n > o:
        return 1
    if o > n:
        return -1
    return 0


def eprocess(paired, alpha=0.05, max_pairs=200):
    """PACE e-process auf den diskordanten Paaren. Gibt Verdikt-Dict zurueck."""
    thr = 1.0 / alpha
    E_new = E_old = 1.0
    wins = n = 0                       # wins = #neu-gewinnt (nur Vergangenheit fuer lam)
    traj = []
    verdict = "CONTINUE"
    for old, new in paired:
        s = _sign(old, new)
        if s == 0:
            continue                   # konkordant → keine Information
        x = 1 if s > 0 else 0
        # PREDICTABLE plug-in lam aus BISHERIGEN diskordanten Paaren (nur Vergangenheit → gueltig)
        phat = (wins / n) if n > 0 else 0.5
        lam_new = max(0.0, min(LAM_CAP, 2.0 * (phat - 0.5)))     # wette auf NEU, wenn Vergangenheit fuer neu spricht
        lam_old = max(0.0, min(LAM_CAP, 2.0 * (0.5 - phat)))     # symmetrisch: wette auf ALT
        E_new *= (1.0 + lam_new * (2 * x - 1))
        E_old *= (1.0 + lam_old * (1 - 2 * x))
        n += 1
        wins += x
        traj.append(round(E_new, 4))
        if E_new >= thr:
            verdict = "ACCEPT"; break
        if E_old >= thr:
            verdict = "REJECT"; break
        if n >= max_pairs:
            verdict = "REJECT"; break   # genug getestet, kein anytime-valides Signal → reject-buffer
    return {
        "verdict": verdict, "e_new": round(E_new, 4), "e_old": round(E_old, 4),
        "threshold": round(thr, 2), "discordant": n, "new_wins": wins,
        "reason": {
            "ACCEPT": "neu ist anytime-valid besser (E_new >= 1/alpha)",
            "REJECT": ("neu ist schlechter (E_old >= 1/alpha)" if E_old >= thr
                       else "max_pairs erreicht ohne Signal → reject-buffer (kein naives >)"),
            "CONTINUE": "noch kein Signal — mehr held-out-Faelle noetig",
        }[verdict],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="PACE anytime-valid Akzeptanz-Gate fuers Skill-Hardening (read-only).")
    ap.add_argument("paired", nargs="?", help="JSON: [[old,new], ...] (bool/Score je held-out-Fall). Sonst stdin.")
    ap.add_argument("--alpha", type=float, default=0.05, help="False-Accept-Ziel (Default 0.05 → Schwelle 20)")
    ap.add_argument("--max-pairs", type=int, default=200)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        raw = args.paired or sys.stdin.read()
        paired = json.loads(raw)
        assert isinstance(paired, list)
    except Exception as e:
        print(f"skill_harden_gate: Eingabe JSON [[old,new],...] erwartet: {e}", file=sys.stderr)
        return 0
    r = eprocess(paired, alpha=args.alpha, max_pairs=args.max_pairs)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    icon = {"ACCEPT": "🟢", "REJECT": "🔴", "CONTINUE": "🟡"}[r["verdict"]]
    print(f"{icon} PACE-Gate: {r['verdict']} — {r['reason']}")
    print(f"   E_new={r['e_new']} · E_old={r['e_old']} · Schwelle={r['threshold']} · "
          f"diskordant={r['discordant']} · neu-gewinnt={r['new_wins']}")
    print("   (anytime-valid: gueltig auch bei vielen getesteten Edits — kein Selbst-p-hacking)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"skill_harden_gate: Fehler: {e}", file=sys.stderr)
        sys.exit(0)
