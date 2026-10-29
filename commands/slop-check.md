---
description: Prüft Text (oder die letzte Antwort) auf KI-Floskeln / AI-Slop
---

Prüfe Text auf KI-Floskeln mit dem Slop-Detector.

Vorgehen:
1. Wenn Argumente/Text übergeben wurden ($ARGUMENTS), schreibe sie in eine
   temporäre Datei und prüfe sie:
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/slop-detector.py --file <tmpfile>`
2. Wenn kein Text übergeben wurde, prüfe deine eigene letzte ausführliche
   Antwort in dieser Session, indem du sie in eine tmp-Datei schreibst und den
   Detector darauf laufen lässt.
3. Gib den Report (Score + Treffer) wieder und nenne — falls Score ≥ Schwelle —
   konkret, welche Formulierungen man streichen/ersetzen sollte. Knapp.

Der Detector ist read-only und ändert nichts.

4. OPTIONAL — qualitativer Layer (ergänzt den Muster-Score um das, was Regex nicht
   sieht). Nur auf Wunsch oder bei Grenzfällen: bewerte den Text 1–10 je Dimension
   und nenne die schwächste zuerst. <35/50 → überarbeiten.

   | Dimension | Frage |
   |-----------|-------|
   | Directness | Aussagen oder Ankündigungen? |
   | Rhythm | Variiert oder metronomisch (gleiche Satzlängen)? |
   | Trust | Respektiert die Leser-Intelligenz (kein Hand-Holding)? |
   | Authenticity | Klingt menschlich? |
   | Density | Ist etwas kürzbar? |

   Der Muster-Score (Schritt 1–3) fängt Floskeln; dieser Layer fängt Struktur/Ton.
   Für den aktiven Rewrite → `/humanize`. (5-Dim-Rubrik adaptiert aus stop-slop, MIT.)
