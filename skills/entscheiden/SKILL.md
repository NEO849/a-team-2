---
name: entscheiden
description: >
  Strukturierte Entscheidungs-Disziplin für folgenreiche, schwer-umkehrbare Entscheidungen
  (Business, Produkt, GTM, Target-Pick, Build-vs-Buy, Einstellung, Launch) — statt Bauchgefühl.
  Fährt eine ehrliche Pipeline: Reversibilität klären → Pre-Mortem → Tradeoffs (ehrlich) →
  Second-Order-Effekte → Blast-Radius → Kill-Criteria → Option-Tree, und endet mit einem
  schriftlichen GO / NO-GO / CONDITIONAL MIT expliziten Kill-Criteria und „was mich widerlegt".
  Keine erfundenen Zahlen (Annahmen benennen, Fakten vom /markt-research holen). Für schwere
  Entscheidungen spawnt der Lead den Agent `strategie-analyst` (opus) + adversarialen Gegen-Pass.
  Für Markt-/Wettbewerbs-FAKTEN siehe /markt-research; für Copy siehe /mkt-akquise.
  Trigger "/entscheiden <frage>", "soll ich <x>", "lohnt sich <x>", "go/no-go <x>",
  "tradeoff <a> vs <b>", "pre-mortem <plan>".
---

# entscheiden — ehrliche Entscheidungs-Pipeline

> Rolle: Senior-Strategie-/Entscheidungs-Analyst. Ziel ist NICHT eine überzeugend klingende Meinung,
> sondern eine **falsifizierbare** Entscheidung mit vor-festgelegten Kill-Criteria. Feind = das
> plausible, aber ungetestete GO.

## Wann laden
Jede Entscheidung, die **teuer rückgängig zu machen** ist, **Downstream-/Second-Order-Effekte** hat
oder gerade **auf Bauchgefühl** getroffen wird. NICHT für triviale, billig-reversible Zwei-Wege-Türen
(da: schnell entscheiden, kleiner Test) — Aufwand skaliert mit Reversibilität × Tragweite.

## Eingabe
Die Entscheidung/Frage (1 Satz), die realen Optionen (inkl. „nichts tun"), bekannte Fakten + wo Fakten
fehlen. Vorhandenen Kontext ZUERST lesen (Projekt-/Business-Dateien, frühere Entscheidungen, Memory) —
nicht im Vakuum entscheiden.

## Werkzeug (Delegation)
- **Schwere/folgenreiche Entscheidung** → Lead spawnt Agent **`strategie-analyst`** (opus) für die volle
  Pipeline + adversarialen Gegen-Pass; parallel dazu eine Marktanalyse, wenn eine Prämisse Markt-Fakten braucht.
- **Leichte Entscheidung** → inline hier durchziehen, ohne Agent.
- Schwere Framework-Details/Templates → `references/decision-frameworks.md` WENN eine Stage tiefer gebraucht wird.

## Die 6 Stages (in Reihenfolge; eine Stage nur mit Begründung überspringen)
1. **Reversibilität zuerst** — Einweg-Tür (kaum umkehrbar) oder Zwei-Wege-Tür (billig zurück)? Das setzt,
   wie tief die Pipeline läuft. Einweg-Türen brauchen die volle Härte.
2. **Pre-Mortem** — 12 Monate später, die Entscheidung ist gescheitert: die 3-5 wahrscheinlichsten
   *konkreten* Todesursachen. Deckt auf, was der Pitch versteckt.
3. **Tradeoffs (ehrlich)** — je Option, was du *aufgibst*. Keine Gratis-Mittagessen; Kosten benennen.
4. **Second-Order-Effekte** — was sich *downstream* ändert, woran du noch nicht denkst (Anreize,
   Abhängigkeiten, was Wettbewerber/Team als Nächstes tun).
5. **Blast-Radius** — wenn's schiefgeht: wer ist betroffen, wie schlimm, wie **reversibel** der Schaden.
6. **Kill-Criteria** — vor-festgelegte, *messbare* Bedingungen zum Abbruch/Umkehr („Stopp, wenn X < N bis D").
   Tötet Sunk-Cost-Drift. Danach **Option-Tree**: die *echten* Wahlmöglichkeiten (meist mehr als das
   angestarrte Entweder-Oder), inkl. „billiger reversibler Test zuerst".

## Ausgabe (das Verdikt)
DECISION (GO / NO-GO / CONDITIONAL-GO(<Bedingung>) / DEFER(<bis was>)) · die 2-3 tragenden Annahmen ·
explizite **Kill-Criteria** · „was mich widerlegen würde" · der billigste Test, der die Kern-Annahme de-riskt.

## Prinzipien (die Kante)
- **Reversibilität ist die Master-Variable** — reversibel → Tempo + kleiner Test; Einweg-Tür → volle Härte.
- **Steelman die Option, die du ablehnst** — kannst du die Gegenseite nicht überzeugend vertreten, hast du
  die Entscheidung nicht verstanden.
- **Kill-Criteria VOR dem Commitment** festlegen — der höchste Hebel gegen Sunk-Cost.
- **Reversibles Experiment schlägt große Wette** — löst ein €500/1-Woche-Test die Kern-Annahme vor dem
  €50k/6-Monate-Commitment?

## Hard-Gates (Abschluss)
- **read-only-first**: analysieren + empfehlen, NICHT die Entscheidung ausführen. Outward-facing Handlung
  (Mail/Vertrag/Post/Kauf) = **kein Vollzug ohne ausdrückliches User-OK**; das Verdikt ist ein reviewbares Artefakt.
- **Keine erfundenen Zahlen** — Annahme benennen oder Fakt via `/markt-research` holen (Entscheidungs-Analog
  zum 45%-Cap: kein selbstsicheres GO auf unbestätigter tragender Annahme, ohne sie + ihren Falsifizierer zu nennen).
- **Adversarial vor „fertig"**: einen Absatz lang die *Gegen*-Empfehlung argumentieren; überlebt sie →
  auf CONDITIONAL/DEFER herunterstufen (nutzt den Reflex eines adversarial reviewers bei $-schweren Entscheidungen).
- Volltext der Gates: `_shared/hard-gates.md`.
