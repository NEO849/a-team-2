#!/usr/bin/env python3
"""Slop-Detector — erkennt KI-Floskeln/"AI-slop" in Text (DE + EN).

Zwei Betriebsarten:

1) Stop-Hook (von Claude Code aufgerufen, wenn der Hauptagent fertig ist):
   stdin = JSON {transcript_path, stop_hook_active, ...}.
   Liest die LETZTE Assistant-Nachricht aus dem Transkript und bewertet sie.
   Verhalten ueber Umgebungsvariable SLOP_GUARD steuerbar:
       off      -> nichts tun
       warn     -> nur in ~/.claude/slop-detector.log protokollieren (default)
       enforce  -> bei Score >= THRESHOLD exit 2 + konkrete Liste an Claude
                   (Claude ueberarbeitet EINMAL; Loop-Schutz via stop_hook_active)

2) CLI (manuell / Slash-Command):
       slop-detector.py --file PFAD
       slop-detector.py --text "..."
       echo "..." | slop-detector.py --stdin
       slop-detector.py --selftest
   Gibt einen lesbaren Report (Score + Treffer) aus, exit 0.

FAIL-OPEN: jeder Fehler im Hook-Pfad => exit 0 (blockiert nie eine Antwort).

Designziel: hohe Praezision auf echte Floskeln, NICHT auf normalen
Fachtext. Strukturmerkmale (Em-Dash etc.) zaehlen nur schwach; das Gewicht
liegt auf eindeutigen Floskel-Phrasen. THRESHOLD verlangt mehrere distinkte
Treffer, damit ein nuechterner technischer Text nicht ausloest.
"""
import json
import os
import re
import sys

THRESHOLD = int(os.environ.get("SLOP_THRESHOLD", "6"))
MIN_CHARS = 280   # kurze Antworten / Tool-Turns ignorieren
LOGFILE = os.path.expanduser("~/.claude/slop-detector.log")

# (regex, gewicht, label) — re.I, re.M. Gewicht 3 = starkes Tell, 1 = schwach.
PHRASES = [
    # --- Englisch: klassische LLM-Tells ---
    (r"\bit'?s not just\b.{0,40}\bit'?s\b", 3, "antithesis: 'not just X, it's Y'"),
    (r"\bnot only\b.{0,40}\bbut also\b", 2, "antithesis: 'not only ... but also'"),
    (r"\bin (?:today'?s|the) (?:fast-paced|ever-(?:evolving|changing)|digital)\b", 3, "phrase: 'in today's fast-paced'"),
    (r"\bit'?s (?:important|worth) (?:to note|noting)\b", 2, "filler: 'it's important to note'"),
    (r"\b(?:in|to) (?:conclusion|summary|summary,)\b", 2, "filler: 'in conclusion/summary'"),
    (r"\b(?:furthermore|moreover|additionally),", 1, "connector overuse"),
    (r"\b(?:delve|delving) into\b", 3, "buzzword: 'delve into'"),
    (r"\b(?:tapestry|symphony|realm|landscape) of\b", 2, "metaphor cliche"),
    (r"\bnavigat(?:e|ing) the (?:complexit|landscape|world)\w*", 3, "phrase: 'navigate the complexities'"),
    (r"\b(?:a )?testament to\b", 2, "phrase: 'a testament to'"),
    (r"\bplays? a (?:crucial|vital|pivotal|key) role\b", 2, "phrase: 'plays a crucial role'"),
    (r"\bwhen it comes to\b", 1, "filler: 'when it comes to'"),
    (r"\b(?:game-?changer|cutting-?edge|state-of-the-art|next level)\b", 2, "hype adjective"),
    (r"\b(?:seamless(?:ly)?|robust|leverage|unlock|unleash|elevate|supercharge|harness the power)\b", 1, "buzzword"),
    (r"\brest assured\b", 2, "reassurance filler"),
    (r"\bi hope this helps\b", 3, "closing pleasantry: 'I hope this helps'"),
    (r"\b(?:feel free to|let me know if you|don'?t hesitate to)\b", 2, "closing pleasantry"),
    (r"\blet'?s (?:dive (?:in|into)|get started|buckle up)\b", 2, "intro filler"),
    (r"\bas an ai(?: language model)?\b", 3, "AI self-reference"),
    (r"\bneedless to say\b", 1, "filler"),
    (r"\bthat being said\b", 1, "filler"),
    # --- Deutsch: aequivalente Tells ---
    (r"\bes ist (?:wichtig|erwaehnenswert)(?:,| zu beachten| anzumerken)", 2, "Floskel: 'es ist wichtig zu beachten'"),
    (r"\bes sei (?:darauf hingewiesen|angemerkt)\b", 2, "Floskel: 'es sei darauf hingewiesen'"),
    (r"\b(?:zusammenfassend|abschliessend|abschließend) (?:lässt sich|kann man|bleibt)\b", 2, "Floskel: 'zusammenfassend lässt sich'"),
    (r"\bin der heutigen (?:schnelllebigen|digitalen|vernetzten)\b", 3, "Floskel: 'in der heutigen schnelllebigen'"),
    (r"\btauchen wir ein\b|\blass(?:en sie)? uns eintauchen\b", 3, "Floskel: 'tauchen wir ein'"),
    (r"\bim (?:bereich|reich) (?:der|des|von)\b", 1, "Floskel: 'im Bereich der'"),
    (r"\bspielt eine (?:entscheidende|zentrale|wichtige|wesentliche) rolle\b", 2, "Floskel: 'spielt eine entscheidende Rolle'"),
    (r"\b(?:nahtlos|robust|bahnbrechend|wegweisend|zukunftsweisend)\b", 1, "Buzzword (DE)"),
    (r"\bauf (?:das|ein) (?:nächste[s]?|neue[s]?) (?:level|niveau)\b", 2, "Hype: 'auf das nächste Level'"),
    (r"\bich hoffe,? (?:das|dies) hilft\b", 3, "Schluss-Floskel: 'ich hoffe das hilft'"),
    (r"\b(?:zöger(?:e|n sie)? nicht|melde dich gern|lass(?:en sie)? es mich wissen)\b", 2, "Schluss-Floskel (DE)"),
    (r"\bnicht nur\b.{0,40}\bsondern auch\b", 2, "Antithese: 'nicht nur ... sondern auch'"),
    (r"\bes ist (?:erwaehnenswert|hervorzuheben)\b", 2, "Floskel (DE)"),
    (r"\bselbstverständlich\b", 1, "Floskel: 'selbstverständlich'"),
    (r"\bletztendlich\b|\bim wesentlichen\b|\bdarüber hinaus\b|\bdes weiteren\b", 1, "Konnektor-Floskel (DE)"),
    (r"\bein wahre[rs]?\b|\bwahre[rs]? (?:game-?changer|kunstwerk|meisterwerk)\b", 2, "Hype (DE)"),
]
_COMPILED = [(re.compile(p, re.I | re.M), w, lbl) for p, w, lbl in PHRASES]

# Emoji-Bereiche fuer "Emoji-Bullet"-Struktur-Heuristik.
_EMOJI = re.compile(
    r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF✨✅⭐]"
)


def score_text(text):
    """Gibt (score, hits) zurueck. hits = Liste (label, count, weight)."""
    hits = []
    score = 0
    for rx, weight, label in _COMPILED:
        n = len(rx.findall(text))
        if n:
            capped = min(n, 3)          # eine Floskel sammelt nicht unbegrenzt
            score += weight * capped
            hits.append((label, n, weight))

    words = max(1, len(text.split()))

    # Strukturmerkmal: Em-Dash-Ueberschuss (schwaches Tell)
    emdash = text.count("—")
    if emdash >= 4 and emdash > words / 120:
        score += 2
        hits.append(("Em-Dash-Ueberschuss (%d)" % emdash, emdash, 2))

    # Strukturmerkmal: viele Emoji-eingeleitete Aufzaehlungspunkte
    emoji_bullets = len(re.findall(r"(?m)^\s*(?:[-*•]\s*)?(?=\S)" +
                                   _EMOJI.pattern, text))
    if emoji_bullets >= 3:
        score += 2
        hits.append(("Emoji-Bullet-Liste (%d)" % emoji_bullets, emoji_bullets, 2))

    return score, hits


def verdict(score):
    if score >= THRESHOLD:
        return "SLOP"
    if score >= 3:
        return "grenzwertig"
    return "sauber"


def render_report(text, score, hits):
    out = ["Slop-Score: %d  (Schwelle %d -> %s)" % (score, THRESHOLD, verdict(score))]
    if hits:
        out.append("Treffer:")
        for label, n, w in sorted(hits, key=lambda h: -h[1] * h[2]):
            out.append("  [%+d] %s  x%d" % (w, label, n))
    else:
        out.append("Keine Floskel-Muster gefunden.")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Stop-Hook-Pfad
# ----------------------------------------------------------------------------
def last_assistant_text(path):
    parts = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") != "assistant":
            continue
        content = (ev.get("message") or {}).get("content") or []
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                parts.append(c.get("text", ""))
        if parts:
            break
    return "\n".join(parts)


def log_line(msg):
    try:
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def run_hook():
    mode = os.environ.get("SLOP_GUARD", "warn").lower()
    if mode == "off":
        sys.exit(0)
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if data.get("stop_hook_active"):   # Loop-Schutz: schon einmal ueberarbeitet
        sys.exit(0)
    path = data.get("transcript_path") or ""
    if not path or not os.path.exists(path):
        sys.exit(0)
    try:
        text = last_assistant_text(path)
    except Exception:
        sys.exit(0)
    if len(text) < MIN_CHARS:
        sys.exit(0)

    score, hits = score_text(text)
    if score < THRESHOLD:
        sys.exit(0)

    summary = ", ".join("%s(x%d)" % (h[0], h[1]) for h in hits[:6])
    log_line("[slop] score=%d mode=%s :: %s" % (score, mode, summary))

    if mode == "enforce":
        sys.stderr.write(
            "Slop-Detector: die letzte Antwort enthaelt KI-Floskeln "
            "(Score %d/%d). Bitte EINMAL knapp ueberarbeiten und die folgenden "
            "Muster entfernen:\n%s\n" % (score, THRESHOLD, render_report(text, score, hits))
        )
        sys.exit(2)
    sys.exit(0)


# ----------------------------------------------------------------------------
# Selbsttest
# ----------------------------------------------------------------------------
SELFTEST_CLEAN = (
    "Befund: Der Guard nutzt globale Regex, die einen Payload auch innerhalb "
    "eines Flags fangen. Luecken: find -delete auf Root, chmod -R auf /etc, "
    "shred auf Geraete. Ich habe die Faelle in die Selbsttest-Batterie "
    "aufgenommen und alle 40 laufen gruen. Naechster Schritt: Stop-Hook "
    "verdrahten. Risiko: bei zu niedriger Schwelle koennten lange Fachtexte "
    "ausloesen, daher Schwelle 6 und Treffer-Cap pro Muster."
)
SELFTEST_SLOP = (
    "In der heutigen schnelllebigen digitalen Welt spielt Sicherheit eine "
    "entscheidende Rolle. Es ist wichtig zu beachten, dass dieser nahtlose, "
    "robuste Ansatz wahrlich bahnbrechend ist. Tauchen wir ein: It's not just "
    "a guard, it's a game-changer. Let's delve into the realm of robust, "
    "cutting-edge tooling. Ich hoffe, das hilft — zoegere nicht, dich zu melden!"
)


def run_selftest():
    fails = 0
    sc, _ = score_text(SELFTEST_CLEAN)
    if sc >= THRESHOLD:
        print("FAIL clean: Score %d >= Schwelle %d (sollte sauber sein)" % (sc, THRESHOLD))
        fails += 1
    else:
        print("OK clean: Score %d < %d" % (sc, THRESHOLD))
    sc2, hits2 = score_text(SELFTEST_SLOP)
    if sc2 < THRESHOLD:
        print("FAIL slop: Score %d < Schwelle %d (sollte ausloesen)" % (sc2, THRESHOLD))
        fails += 1
    else:
        print("OK slop:  Score %d >= %d  (%d Muster)" % (sc2, THRESHOLD, len(hits2)))
    print("%s" % ("ALLE OK" if not fails else "FEHLER"))
    return 1 if fails else 0


def main():
    args = sys.argv[1:]
    if not args:
        run_hook()                 # default: Stop-Hook-Modus
        return
    if "--selftest" in args:
        sys.exit(run_selftest())
    text = None
    if "--file" in args:
        with open(args[args.index("--file") + 1], encoding="utf-8", errors="replace") as f:
            text = f.read()
    elif "--text" in args:
        text = args[args.index("--text") + 1]
    elif "--stdin" in args:
        text = sys.stdin.read()
    if text is None:
        print("Nutzung: slop-detector.py [--file F | --text T | --stdin | --selftest]")
        sys.exit(0)
    score, hits = score_text(text)
    print(render_report(text, score, hits))
    sys.exit(0)


if __name__ == "__main__":
    main()
