---
name: build-tdd
description: >
  Test-getriebene Bau-Disziplin für nicht-triviale Code-Aufgaben (Feature, Refactor, Bugfix).
  Erzwingt RED→GREEN→REFACTOR mit hartem Gate: EIN fehlschlagender Test wird tatsächlich
  ausgeführt und sein Scheitern verifiziert BEVOR eine Zeile Produktivcode existiert;
  Code-vor-Test wird gelöscht, nicht adaptiert. Plus Mutation-/„Name-the-break"-Test-
  Qualitätsgate, Git-Worktree-Isolation pro Feature, Subagent-Delegation via
  Task-Brief+Report-Datei (kein Kontext-Bloat), Fix-Loop mit Runden-Cap+Modell-Eskalation,
  Verification-before-completion (kein „fertig" ohne frisch gelaufenen Beleg). Ergänzt
  /elite-prompt (Orchestrierung) und /debugging-and-error-recovery (Root-Cause).
  Nutze für ernsthaftes Software-Bauen, wo Korrektheit zählt.
  Trigger "/build-tdd <aufgabe>", "tdd <feature>", "test-first <aufgabe>",
  "baue mit tests <x>", "red green refactor".
---

# build-tdd — Test-first Bauen mit harten Gates

> Rolle: Senior-Staff-Engineer mit TDD-Disziplin. Kein Produktivcode ohne zuerst
> fehlschlagenden Test. Destilliert aus obra/superpowers (MIT), an unser Arsenal angepasst.

## Wann laden
Nicht-triviales Bauen wo Korrektheit zählt (Feature, Refactor, Bugfix mit Regression).
NICHT für Wegwerf-Spikes/Prototypen — da bremst TDD. Für reine Fehlersuche → `/debugging-and-error-recovery`.

**Reproduzierbarer Default (wiederkehrendes, korrektheits-kritisches Bauen):** die deterministische
Workflow-Variante `Workflow({name:'build-welle', args:{task:'…'}})` — dieselben Gates (Plan→RED→GREEN→
Review→Synthese) als replay-fähiger Workflow mit Audit-Trail, kein Commit ohne User-OK. Dieses Inline-
`/build-tdd` bleibt der **Escape-Hatch** für exploratives/unklares Bauen, wo ein fester Ablauf bremst.

## Iron Law
**KEIN Produktivcode, bevor ein Test ihn fordert und tatsächlich fehlschlägt.**
Wurde Code vor dem Test geschrieben → löschen und aus dem Test heraus neu implementieren.
Nicht „als Referenz behalten", nicht adaptieren. (Der aggressive Ton ist Stilmittel gegen
die übliche LLM-Abkürzungs-Rationalisierung „nur dieses eine Mal".)

## Die Sequenz (jeder Schritt = hartes Gate)
1. **RED** — EIN minimaler Test, EINE Verhaltensweise, klarer Name, reale Codepfade
   (Mocks nur wo unvermeidbar).
2. **Verify RED (PFLICHT, nie überspringen)** — Test wirklich ausführen. Muss *failen*,
   nicht *erroren*. Passt er sofort → er testet bestehendes Verhalten (falsch). Error statt
   Fail → Test fixen bis er korrekt fehlschlägt.
3. **GREEN** — minimalster Code, der genau diesen Test grün macht. Kein Feature-Vorgriff (YAGNI).
4. **Verify GREEN (PFLICHT)** — Testlauf: Pass + alle anderen Tests weiter grün + sauberer
   Output (keine neuen Warnings).
5. **REFACTOR** — nur nach Grün: Duplikation raus, Namen schärfen, kein neues Verhalten. Tests bleiben grün.
6. Wiederholen für das nächste Verhalten.

## Test-Qualitäts-Gate (vor jedem Test)
- **„Name the break":** Welche Produktiv-Änderung würde diesen Test brechen — Bug oder
  Design-Entscheidung? Kein Name nennbar → Test umbauen (er testet nichts).
- **Erwarteter Wert unabhängig herleiten** — Literal/Fixture, nie den Code-under-Test spiegeln
  (Tautologie-Test).
- **Mutations-Check vor Abschluss:** gedanklich mutieren (falsche Konstante, falscher Branch,
  fehlender Seiteneffekt, leerer Return, fehlende Validierung) — mind. 1 Test muss pro Mutation kippen.

## Worktree-Isolation (ein Feature = ein Worktree)
- **Erst prüfen, dann erstellen:** Bin ich schon in isoliertem Workspace/Submodule? Dann NICHT neu anlegen.
- **Nativ bevorzugen:** unser `Agent(isolation:"worktree")` bzw. Harness-Worktree > manuelles
  `git worktree add` (sonst Phantom-State, den der Harness nicht sieht).
- Fallback-Pfad: bevorzugt verstecktes `.worktrees/`, das MUSS `git check-ignore`-geprüft sein —
  sonst zuerst in `.gitignore` + committen (sonst landet der ganze Worktree-Baum im Repo).
- Nach Erstellung: Setup erkennen (npm/cargo/pip/poetry/go) → **Baseline-Tests laufen lassen**.
  Baseline rot → User fragen, nicht drüberarbeiten.
- Cleanup nur eigene `.worktrees/`, nie fremde; nur bei „lokal gemerged" oder wortwörtlich
  bestätigtem Discard. Bei „PR erstellt"/„später" bleibt der Worktree stehen.

## Subagent-Delegation (bei mehreren Tasks)
> Orchestrierungs-Grundlagen (Zerlegen/Zuweisen/Parallel-vs-abhängig, Modell-Matrix) → `/elite-prompt`
> + Global-CLAUDE.md. Hier nur die TDD-SPEZIFISCHEN Delegations-Muster (Quelle der Wahrheit dort, um Drift zu vermeiden).

Ich (Koordinator) fahre die Verkettung — kein Agent ruft den nächsten. Pro Task ein *frischer*
Implementer-Subagent, danach ein Task-Review, am Ende ein breiter Gesamt-Review.
- **Task-Brief statt Vollplan:** Subagent bekommt nur die extrahierte Task-Beschreibung als Datei
  (Requirements wortwörtlich, exakte Werte), 1 Zeile Projekt-Einordnung, Interfaces der Vorgänger-Tasks,
  Report-Pfad+Contract. KEINE gepastete Session-Historie (Kontext-Bloat-Killer).
- **Report-Datei statt Chat-Report:** Implementer schreibt vollen Bericht nach `task-N-report.md`,
  gibt im Chat nur Status + Commits + 1-Zeilen-Testsummary. Diff/Review-Package als Datei-Pfad
  übergeben, nie in den Koordinator-Kontext lesen (→ Heavy-Read-Delegat-Prinzip).
- **Report-Status:** DONE→Review · DONE_WITH_CONCERNS→Concerns erst adressieren · NEEDS_CONTEXT→
  Kontext liefern+redispatch · BLOCKED→Ursache diagnostizieren (Kontext/Modell/Task-Größe/Plan),
  nie stumpf mit gleichem Modell neu.
- **Fix-Loop-Cap:** max 5 Runden/Task. R1-3 gleicher Implementer (Kontext intakt), R4-5 frischer
  Implementer + stärkeres Modell. Bei Cap ohne Konvergenz: adjudizieren (parken mit Begründung vs.
  BLOCKED an Mensch) + Ledger-Eintrag — nie eigenhändig fixen (umgeht Review), nie stiller Discard.
- **Modell-Matrix:** mechanisch→Haiku · Integration/Urteil→Sonnet · Architektur+Finaler-Review→Opus.
  Immer explizit setzen (sonst erbt der Subagent das teuerste Default).
- **Ledger `progress.md`:** Task-Status-Zeilen — überlebt Kontext-Kompaktierung, verhindert
  Re-Dispatch bereits fertiger Tasks.

## Verification-before-completion (kein „fertig" ohne Beleg)
Keine „fertig"/„passt"-Behauptung ohne in DIESEM Turn frisch gelaufenen Beweis-Befehl:
1. Welcher Befehl beweist die Behauptung? 2. Voll + frisch ausführen. 3. Volle Ausgabe lesen,
Exit-Code prüfen, Fehler zählen. 4. Bestätigt? Nein → echten Status mit Beleg nennen. 5. Erst dann aussagen.
- **Rot-Flags:** „sollte", „vermutlich", „scheint", Erfolgswort vor Prüfung, ungeprüfte Agent-Erfolgsmeldung.
- **Bugfix:** Original-Symptom erneut testen (nicht nur „Code geändert").
- **Regressionstest:** Red-Green-Zyklus zeigen — Test schreiben→pass→Fix zurücknehmen→MUSS failen→Fix zurück→pass.
- **Requirements:** Zeile-für-Zeile gegen Spec, nicht nur „Tests grün".

## Branch abschließen
1. Volle Testsuite — rot → stoppen, erst grün. 2. Environment erkennen (repo/worktree/detached).
3. Base-Branch *bestätigen*, nicht raten. 4. Festes Menü präsentieren (lokal mergen / Push+PR / so lassen),
auf Antwort warten — **nie automatisch mergen** (Integration = Menschen-Entscheidung).
5. Bei lokal-Merge: Tests auf gemergtem Ergebnis erneut. 6. Cleanup nur bei Merge/bestätigtem Discard.

## Hard-Gates (Abschluss)
- Kein „fertig" ohne frisch gelaufenen Beleg (s.o.). Vor Auslieferung adversarial: ein adversarial reviewer
  über das Ergebnis + Chain-Frage („fehlt ein Schritt/Kante?").
- Kein Auto-Merge/Push ohne User-OK. Keine destruktiven Git-Ops (force-push, branch -D) ohne OK.
- Read-only-first bei fremdem Code. Siehe `_shared/hard-gates.md`.
