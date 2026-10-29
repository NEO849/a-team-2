#!/usr/bin/env python3
"""Regenerate references/quick-reference.md from data/ux-guidelines.json (single source of truth)."""
import json, os
base=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
d=json.load(open(os.path.join(base,"data","ux-guidelines.json"),encoding="utf-8"))
cats={}
[cats.setdefault(r["category"],[]).append(r) for r in d]
order=["accessibility","touch","performance","style","layout","typography","animation","forms","navigation","charts"]
pr={r["category"]:r["priority"] for r in d}
out=["# design-intel — UX Quick-Reference (Volltext)","",
     "> Generiert aus `data/ux-guidelines.json` (Single Source of Truth). Neu erzeugen: `python3 scripts/gen_quickref.py`.",
     "> Nur bei Bedarf laden; für gezielte Abfrage `search.py --domain ux \"<problem>\"`.",""]
for c in order:
    if c not in cats: continue
    out.append(f"## {pr[c]}. {c.capitalize()}  ({len(cats[c])} Regeln)")
    for r in cats[c]:
        out.append(f"- **{r['id']}** — {r['rule']}")
        out.append(f"  - ✗ Anti-Pattern: {r['anti']}")
    out.append("")
open(os.path.join(base,"references","quick-reference.md"),"w",encoding="utf-8").write("\n".join(out))
print("regenerated:", len(d), "rules")
