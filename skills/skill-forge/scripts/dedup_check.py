#!/usr/bin/env python3
"""
dedup_check.py — Dedup-Gate für /skill-forge.

Vergleicht eine KANDIDATEN-Skill-Idee (Description/Trigger/Topic) gegen ALLE bestehenden
Skills unter ~/.claude/skills/ und meldet die ähnlichsten — damit NIE ein Duplikat von
z.B. mkt-akquise/humanize angelegt wird. Metrik = Containment-Koeffizient (Schnitt / kleinere
Menge) auf signifikanten Termen + geteilte Trigger-Tokens. Containment (nicht Jaccard), weil die
Frage lautet „ist der (kurze) Kandidat in einem (langen) bestehenden Skill enthalten?" — Jaccard
würde durch die viel längeren Bestands-Descriptions verwässert.

Nutzung:
    python3 dedup_check.py "<kandidaten-text: description oder topic + trigger>"
    echo "<text>" | python3 dedup_check.py -
    python3 dedup_check.py --file kandidat.md

Exit-Code: 0 immer (Berater, kein Blocker). Verdikt steht im Output:
    🔴 BLOCK  (Overlap ≥ 0.45 mit Bestehendem → NICHT neu anlegen, das existierende erweitern)
    🟡 PRÜFEN (0.25–0.45 → Abgrenzung in Description schärfen, Scope-Cross-Link setzen)
    🟢 FREI   (< 0.25 → echte Lücke, anlegen erlaubt)

stdlib-only, kein Netz.
"""
from __future__ import annotations
import os
import re
import sys
import glob

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
BLOCK_THRESHOLD = 0.55
REVIEW_THRESHOLD = 0.35

# DE+EN Stopwords + generische Skill-Vokabel (tragen keine Unterscheidung)
STOP = set("""
und oder aber der die das ein eine einen einer dem den des mit für aus von zu im in am an auf
ist sind war wird werden kann muss soll nicht kein keine nur auch als wie was wann wo wer wenn
bei nach vor über unter durch gegen ohne um bis per je pro dann sonst statt sowie bzw etc usw
the and for with from this that into out are was were will can must should not only also als
your you our their its his her <x> <target> <ziel> <frage> <name> <plan> <a> <b>
skill skills trigger triggers use used using nutze nutzt wann laden eingabe werkzeug hard gates
volltext siehe für via echte echt real user ohne kein keine
""".split())

TOKEN_RX = re.compile(r"[a-zäöüß0-9]{4,}", re.IGNORECASE)
TRIGGER_RX = re.compile(r'"([^"]{2,80})"')


def significant_terms(text: str) -> set[str]:
    toks = {t.lower() for t in TOKEN_RX.findall(text)}
    return {t for t in toks if t not in STOP}


def trigger_tokens(text: str) -> set[str]:
    out: set[str] = set()
    for phrase in TRIGGER_RX.findall(text):
        for t in TOKEN_RX.findall(phrase.lower()):
            if t not in STOP:
                out.add(t)
    return out


def frontmatter(md: str) -> str:
    """Description-Frontmatter (zwischen den ersten beiden ---) + erste Body-Zeilen."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", md, re.DOTALL)
    if not m:
        return md[:2000]
    fm, body = m.group(1), m.group(2)
    return fm + "\n" + body[:400]


def load_skills() -> list[tuple[str, str]]:
    out = []
    for path in sorted(glob.glob(os.path.join(SKILLS_DIR, "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(path))
        if name.startswith("_"):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                out.append((name, frontmatter(f.read())))
        except OSError:
            continue
    return out


def containment(a: set[str], b: set[str]) -> float:
    """Schnitt / kleinere Menge — misst, wie stark die kleinere Menge in der größeren aufgeht."""
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def score(cand_terms, cand_trig, other_text) -> float:
    o_terms = significant_terms(other_text)
    o_trig = trigger_tokens(other_text)
    term_c = containment(cand_terms, o_terms)
    # Trigger-Kollision = gleiche Auslöser → echtes Routing-Duplikat, hoch gewichtet
    trig_c = containment(cand_trig, o_trig)
    return round(0.7 * term_c + 0.3 * trig_c, 3)


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: dedup_check.py \"<kandidaten-text>\" | --file <p> | -", file=sys.stderr)
        return 0
    if args[0] == "--file":
        with open(args[1], encoding="utf-8") as f:
            cand = f.read()
    elif args[0] == "-":
        cand = sys.stdin.read()
    else:
        cand = " ".join(args)

    cand_terms = significant_terms(cand)
    cand_trig = trigger_tokens(cand)
    if not cand_terms:
        print("⚠ Kandidat leer/zu generisch — mehr Description/Trigger geben.")
        return 0

    ranked = sorted(
        ((score(cand_terms, cand_trig, txt), name) for name, txt in load_skills()),
        reverse=True,
    )
    top = ranked[:5]
    worst = top[0][0] if top else 0.0

    if worst >= BLOCK_THRESHOLD:
        verdict = f"🔴 BLOCK (Overlap {worst}) — NICHT neu anlegen; erweitere den bestehenden Skill."
    elif worst >= REVIEW_THRESHOLD:
        verdict = f"🟡 PRÜFEN (Overlap {worst}) — Abgrenzung in Description schärfen + Scope-Cross-Link setzen."
    else:
        verdict = f"🟢 FREI (Overlap {worst}) — echte Lücke, Anlage erlaubt."

    print(verdict)
    print("\nTop-5 ähnlichste bestehende Skills:")
    for s, name in top:
        flag = "  ← Kollision" if s >= REVIEW_THRESHOLD else ""
        print(f"  {s:>5}  /{name}{flag}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # Berater, nie hart failen
        print(f"⚠ dedup_check Fehler (fail-open): {e}", file=sys.stderr)
        sys.exit(0)
