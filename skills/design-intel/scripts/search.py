#!/usr/bin/env python3
"""design-intel search — dependency-free query over the local design corpus.

Domains: palette | font | ux | motion | style
Modes:   --domain <d> (ranked hits) | --design-system (aggregate a system)
Formats: ascii (default) | markdown | json
Dials:   --variance/--motion/--density 1-10 (bias --design-system output)

Discipline (do not remove):
  * 0 results are reported as 0 with an explicit fallback label — never fabricated.
  * A missing or empty data file is a HARD ERROR ("DATA BROKEN"), never a silent
    empty result. (Harvested from task-observer: an empty read over a populated
    source is a broken command until proven otherwise.)
"""
import argparse, json, os, re, sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FILES = {
    "palette": "palettes.json",
    "font":    "fonts.json",
    "ux":      "ux-guidelines.json",
    "motion":  "motion.json",
    "style":   "styles.json",
}
STOP = {"a","an","the","for","of","to","and","or","with","in","on","my","me",
        "design","ui","ux","app","site","page","website","need","want","make","build","that","this"}

def load(domain):
    path = os.path.join(DATA_DIR, FILES[domain])
    if not os.path.exists(path):
        sys.exit(f"DATA BROKEN — expected {FILES[domain]} at {os.path.normpath(path)}, file missing")
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        sys.exit(f"DATA BROKEN — {FILES[domain]} does not parse: {e}")
    if not isinstance(data, list) or not data:
        sys.exit(f"DATA BROKEN — {FILES[domain]} present but holds no entries")
    return data

def tokens(text):
    return [t for t in re.split(r"[^a-z0-9]+", (text or "").lower()) if t and t not in STOP]

def haystack(item):
    """(weighted terms) -> dict token->weight for one corpus item."""
    w = {}
    def add(vals, weight):
        for v in vals:
            for t in tokens(v):
                w[t] = max(w.get(t, 0), weight)
    add(item.get("keywords", []), 3)
    add(item.get("product_types", []), 2)
    add([item.get("name", ""), item.get("category", ""), item.get("tier", ""), item.get("display", ""), item.get("body", ""), item.get("mono", "")], 2)
    add([item.get("reasoning", ""), item.get("when", ""), item.get("rule", "")], 1)
    return w

def score(item, qtokens, boosts=None):
    w = haystack(item)
    s = sum(w.get(t, 0) for t in qtokens)
    if boosts:
        for t, b in boosts.items():
            if t in w:
                s += b
    # House-style bias is ONLY a tiebreak among real matches — it must never lift a
    # zero-match item above 0, or a nonsense query would falsely report a match
    # instead of the honest fallback.
    if s > 0 and item.get("house_default"):
        s += 0.5
    return s

def rank(domain, query, n=5, boosts=None):
    data = load(domain)
    qt = tokens(query)
    scored = sorted(((score(it, qt, boosts), it) for it in data), key=lambda x: (-x[0], x[1].get("name", x[1].get("id",""))))
    return qt, scored[:n]

def default_item(domain):
    """The honest fallback for a 0-match query: the house-style default if the
    corpus marks one, else the first entry in file order — never the alphabetically
    first, which would misrepresent an arbitrary pick as 'the default'."""
    data = load(domain)
    for it in data:
        if it.get("house_default"):
            return it
    return data[0]

# ---------- rendering ----------
def label(it):
    return it.get("name") or it.get("display") or it.get("id")

def line(it, domain):
    if domain == "palette":
        c = it["colors"]; return f"  {label(it):22} [{it['mode']}] bg {c['bg']}  accent {c['accent']}  — {it['reasoning']}"
    if domain == "font":
        return f"  {label(it):22} display={it['display']} / body={it['body']} / mono={it['mono']}  — {it['reasoning']}"
    if domain == "ux":
        return f"  [{it['category']}] {it['rule']}\n      ✗ {it['anti']}"
    if domain == "motion":
        return f"  {label(it):22} ({it['tier']}) — {it['when']}"
    if domain == "style":
        return f"  {label(it):22} — {it['when']}"
    return f"  {label(it)}"

def print_domain(domain, query, qt, hits, fmt):
    top = hits[0][0] if hits else 0
    if fmt == "json":
        print(json.dumps({"domain": domain, "query": query, "matched": top > 0,
                          "results": [it for s, it in hits if s > 0] or ([hits[0][1]] if hits else [])}, indent=2)); return
    if top <= 0:
        print(f"NO MATCH for '{query}' in domain '{domain}'. "
              f"Fallback = generic default below (label it as a default, not a database match):")
        hits = [(0, default_item(domain))]
    hdr = f"── {domain.upper()} — query: {query!r} (tokens: {', '.join(qt) or '—'})"
    print(hdr)
    for s, it in hits:
        if s <= 0 and top > 0:
            continue
        print(line(it, domain))

def dials_boosts(variance):
    if variance is None: return None
    if variance <= 3:  return {t: 2 for t in ("minimal","refined","clean","restrained")}
    if variance >= 8:  return {t: 2 for t in ("brutalist","bold","bento","cinematic","edgy")}
    return None

def motion_tier(m):
    if m is None: return "standard"
    return "subtle" if m <= 3 else ("complex" if m >= 8 else "standard")

def density_tokens(d):
    if d is None or 4 <= d <= 7:
        return ("standard", "--space-1:8px --space-2:16px --space-3:24px --space-4:32px --space-6:48px --space-8:64px")
    if d <= 3:
        return ("spacious", "--space-1:12px --space-2:24px --space-3:36px --space-4:48px --space-6:72px --space-8:96px")
    return ("dense", "--space-1:4px --space-2:8px --space-3:12px --space-4:16px --space-6:24px --space-8:32px")

def design_system(query, project, variance, motion, density, fmt):
    boosts = dials_boosts(variance)
    _, pal = rank("palette", query, 1, boosts)
    _, fon = rank("font", query, 1, boosts)
    _, sty = rank("style", query, 1, boosts)
    qt, ux = rank("ux", query, 5)
    tier = motion_tier(motion)
    mot = [(s, it) for s, it in rank("motion", query, 20)[1] if it["tier"] == tier][:3]
    dens_name, dens_scale = density_tokens(density)
    fallback = (pal[0][0] <= 0)

    if fallback:
        P, F, S = default_item("palette"), default_item("font"), default_item("style")
    else:
        P, F, S = pal[0][1], fon[0][1], sty[0][1]
    if fmt == "json":
        print(json.dumps({
            "project": project, "query": query, "matched": not fallback,
            "dials": {"variance": variance, "motion_tier": tier, "density": dens_name},
            "palette": P, "font": F, "style": S,
            "motion_presets": [it for _, it in mot],
            "ux_focus": [it for s, it in ux if s > 0][:5],
            "spacing_scale": dens_scale,
        }, indent=2)); return

    title = f"DESIGN SYSTEM — {project or query}"
    print("═" * len(title)); print(title); print("═" * len(title))
    if fallback:
        print("(!) No strong keyword match — this system is the house default, not a database hit. Adjust the query for a tighter fit.")
    print(f"Dials: variance={variance if variance is not None else '—'}  motion-tier={tier}  density={dens_name}\n")
    c = P["colors"]
    print(f"● PALETTE  {label(P)} [{P['mode']}]")
    print(f"    bg {c['bg']}  surface {c['surface']}  border {c['border']}  text {c['text']}  muted {c['muted']}")
    print(f"    accent {c['accent']}  accent2 {c['accent2']}  ok {c.get('success','')}  warn {c.get('warning','')}  danger {c.get('danger','')}")
    print(f"    → {P['reasoning']}\n    ✗ {P['anti']}\n")
    print(f"● TYPE     {label(F)}")
    print(f"    display {F['display']} · body {F['body']} · mono {F['mono']}  (Google Fonts: {F.get('google_fonts')})")
    print(f"    → {F['reasoning']}\n    · {F['pairing_note']}\n")
    print(f"● STYLE    {label(S)}")
    print(f"    {S['when']}")
    print(f"    signatures: {', '.join(S['signatures'])}\n    ✗ {S['anti']}\n")
    print(f"● MOTION   tier={tier}")
    for _, it in mot:
        print(f"    {label(it):20} — {it['when']}")
    if not mot:
        print("    (no preset in tier)")
    print(f"\n● SPACING  ({dens_name})\n    {dens_scale}\n")
    print("● UX FOCUS (top rules for this brief)")
    shown = [it for s, it in ux if s > 0][:5] or [it for _, it in ux][:3]
    for it in shown:
        print(f"    [{it['category']}] {it['rule']}")

def main():
    ap = argparse.ArgumentParser(description="design-intel corpus search")
    ap.add_argument("query", help="2-5 meaningful terms + one constraint")
    ap.add_argument("--domain", choices=list(FILES))
    ap.add_argument("--design-system", action="store_true")
    ap.add_argument("-p", "--project", default="")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--variance", type=int)
    ap.add_argument("--motion", type=int)
    ap.add_argument("--density", type=int)
    ap.add_argument("-f", "--format", choices=["ascii", "markdown", "json"], default="ascii")
    a = ap.parse_args()
    fmt = "ascii" if a.format == "markdown" else a.format  # markdown ≈ ascii here; json is machine-readable

    if a.design_system:
        design_system(a.query, a.project, a.variance, a.motion, a.density, fmt); return
    if not a.domain:
        # auto-detect: run all domains, show the single best hit per domain
        print("(no --domain given — showing best hit per domain; pass --domain to go deep)\n")
        for d in FILES:
            _, hits = rank(d, a.query, 1)
            if hits and hits[0][0] > 0:
                print(f"[{d}] {label(hits[0][1])}")
        print("\nUse --domain <palette|font|ux|motion|style> or --design-system for full output.")
        return
    qt, hits = rank(a.domain, a.query, a.n, dials_boosts(a.variance))
    print_domain(a.domain, a.query, qt, hits, fmt)

if __name__ == "__main__":
    main()
